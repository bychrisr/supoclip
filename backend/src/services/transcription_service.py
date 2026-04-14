"""
Hybrid transcription service: Gemini (primary) → AssemblyAI (fallback).

Provider selection is determined at startup via health check and cached in
TranscriptionService._gemini_available. Call TranscriptionService.run_health_check()
during application lifespan to initialize the flag.
"""

import json
import logging
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

TRANSCRIPTION_PROMPT = """Transcribe this audio completely and accurately.

Return ONLY a valid JSON object with this exact format, no other text:
{
  "words": [
    {"text": "word", "start_ms": 0, "end_ms": 400},
    {"text": "next", "start_ms": 420, "end_ms": 800}
  ],
  "full_text": "complete transcript text here"
}

Rules:
- Include every spoken word
- start_ms and end_ms are in milliseconds from the beginning of this audio chunk
- Be as accurate as possible with timing
- Do not add commentary, markdown, or code blocks — return raw JSON only"""

CHUNK_DURATION_SECONDS = 420  # 7 minutes per chunk


class TranscriptionService:
    _gemini_available: bool = False
    _health_check_done: bool = False

    @staticmethod
    def _resolve_gemini_model(llm_config: Optional[str]) -> str:
        """
        Derives the raw Gemini model name from config.llm.
        config.llm format: 'google-gla:gemini-3-flash-preview'
        Returns: 'gemini-3-flash-preview'
        Falls back to 'gemini-1.5-flash' if not a Google model.
        """
        if llm_config and llm_config.startswith("google-gla:"):
            return llm_config.split(":", 1)[1]
        return "gemini-1.5-flash"

    @classmethod
    async def run_health_check(cls) -> bool:
        """
        Run at startup. Tests Gemini with a simple ping and sets _gemini_available.
        Must be awaited inside the application lifespan coroutine.
        """
        from ..config import Config

        config = Config()

        if not config.google_api_key:
            logger.info(
                "[TranscriptionService] No GOOGLE_API_KEY — using AssemblyAI"
            )
            cls._gemini_available = False
            cls._health_check_done = True
            return False

        try:
            from google import genai

            client = genai.Client(api_key=config.google_api_key)
            model_name = cls._resolve_gemini_model(config.llm)
            # Simple ping to verify the key is valid
            client.models.generate_content(
                model=model_name,
                contents="ping",
            )
            cls._gemini_available = True
            cls._health_check_done = True
            logger.info(
                "[TranscriptionService] Gemini health check passed — using Gemini for transcription"
            )
            return True
        except Exception as exc:
            cls._gemini_available = False
            cls._health_check_done = True
            logger.warning(
                "[TranscriptionService] Gemini health check failed: %s — falling back to AssemblyAI",
                exc,
            )
            return False

    @classmethod
    def transcribe(cls, video_path: Path, speech_model: str = "best") -> str:
        """
        Transcribe video/audio. Returns formatted transcript string with timestamps.
        Also writes transcript cache to .transcript_cache.json beside the video file.

        Tries Gemini first (if available from health check), falls back to AssemblyAI.
        """
        logger.info(
            "[TranscriptionService] transcribe start: path=%s gemini_available=%s",
            video_path,
            cls._gemini_available,
        )

        if cls._gemini_available:
            try:
                return cls._transcribe_with_gemini(video_path)
            except Exception as exc:
                logger.error(
                    "[TranscriptionService] Gemini transcription failed, falling back to AssemblyAI: %s",
                    exc,
                )

        return cls._transcribe_with_assemblyai(video_path, speech_model)

    # -------------------------------------------------------------------------
    # Audio helpers
    # -------------------------------------------------------------------------

    @classmethod
    def _extract_audio_ogg(cls, video_path: Path, output_path: Path) -> None:
        """Extract audio from video to OGG (mono, 16 kHz) using ffmpeg."""
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-vn",
            "-c:a",
            "libvorbis",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-q:a",
            "4",
            str(output_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                f"ffmpeg audio extraction failed: {result.stderr}"
            )
        logger.debug(
            "[TranscriptionService] audio extracted to %s", output_path
        )

    @classmethod
    def _get_audio_duration_seconds(cls, audio_path: Path) -> float:
        """Get audio duration in seconds using ffprobe."""
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(audio_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffprobe failed: {result.stderr}")
        return float(result.stdout.strip())

    @classmethod
    def _chunk_audio(cls, audio_path: Path, chunks_dir: Path) -> list[Path]:
        """Split audio into chunks of CHUNK_DURATION_SECONDS seconds."""
        output_pattern = str(chunks_dir / "chunk_%03d.ogg")
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(audio_path),
            "-f",
            "segment",
            "-segment_time",
            str(CHUNK_DURATION_SECONDS),
            "-c:a",
            "libvorbis",
            "-q:a",
            "3",
            output_pattern,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg chunking failed: {result.stderr}")

        chunks = sorted(chunks_dir.glob("chunk_*.ogg"))
        if not chunks:
            raise RuntimeError("No audio chunks generated")
        logger.debug(
            "[TranscriptionService] chunked into %d parts", len(chunks)
        )
        return chunks

    # -------------------------------------------------------------------------
    # Gemini path
    # -------------------------------------------------------------------------

    @classmethod
    def _call_gemini_transcribe(
        cls, audio_path: Path, chunk_offset_ms: int = 0
    ) -> dict:
        """Send a single audio chunk to Gemini and parse word-level transcript."""
        from google import genai
        from google.genai import types
        from ..config import Config

        config = Config()
        client = genai.Client(api_key=config.google_api_key)
        audio_bytes = audio_path.read_bytes()

        audio_part = types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/ogg",
        )

        language_hint = (config.transcription_language_hint or "").strip().lower()
        prompt = TRANSCRIPTION_PROMPT
        if language_hint and language_hint not in {"auto", "none"}:
            prompt = (
                "The audio language is Brazilian Portuguese (pt-BR). "
                "Preserve Portuguese spelling and punctuation.\n\n"
                + TRANSCRIPTION_PROMPT
            )

        response = client.models.generate_content(
            model=cls._resolve_gemini_model(config.llm),
            contents=[audio_part, prompt],
        )

        raw = response.text.strip()

        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1]
            if raw.endswith("```"):
                raw = raw.rsplit("```", 1)[0]

        data = json.loads(raw)

        # Apply chunk offset to all timestamps
        if chunk_offset_ms > 0:
            for word in data.get("words", []):
                word["start_ms"] = word.get("start_ms", 0) + chunk_offset_ms
                word["end_ms"] = word.get("end_ms", 0) + chunk_offset_ms

        return data

    @classmethod
    def _transcribe_with_gemini(cls, video_path: Path) -> str:
        """Transcribe using Gemini. Extracts audio, chunks if needed, merges results."""
        logger.info(
            "[TranscriptionService] Gemini transcription: %s", video_path
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            ogg_path = tmp / "audio.ogg"

            cls._extract_audio_ogg(video_path, ogg_path)
            duration = cls._get_audio_duration_seconds(ogg_path)
            logger.info(
                "[TranscriptionService] audio duration: %.1fs", duration
            )

            all_words: list[dict] = []
            full_text_parts: list[str] = []

            if duration <= CHUNK_DURATION_SECONDS:
                # Single chunk — process directly
                data = cls._call_gemini_transcribe(ogg_path)
                all_words = data.get("words", [])
                full_text_parts = [data.get("full_text", "")]
            else:
                # Multiple chunks
                chunks_dir = tmp / "chunks"
                chunks_dir.mkdir()
                chunk_paths = cls._chunk_audio(ogg_path, chunks_dir)

                offset_ms = 0
                for i, chunk_path in enumerate(chunk_paths):
                    logger.info(
                        "[TranscriptionService] transcribing chunk %d/%d (offset=%dms)",
                        i + 1,
                        len(chunk_paths),
                        offset_ms,
                    )
                    data = cls._call_gemini_transcribe(
                        chunk_path, chunk_offset_ms=offset_ms
                    )
                    all_words.extend(data.get("words", []))
                    full_text_parts.append(data.get("full_text", ""))
                    offset_ms += int(CHUNK_DURATION_SECONDS * 1000)

            full_text = " ".join(p for p in full_text_parts if p)

            # Write cache in the same format as AssemblyAI so subtitle
            # generation (load_cached_transcript_data) works transparently.
            cache_data = {
                "words": [
                    {
                        "text": w["text"],
                        "start": w["start_ms"],
                        "end": w["end_ms"],
                        "confidence": 1.0,
                    }
                    for w in all_words
                ],
                "text": full_text,
            }
            cache_path = video_path.with_suffix(".transcript_cache.json")
            with open(cache_path, "w") as f:
                json.dump(cache_data, f)
            logger.info(
                "[TranscriptionService] cached %d words to %s",
                len(all_words),
                cache_path,
            )

            return cls._format_transcript_string(cache_data["words"])

    # -------------------------------------------------------------------------
    # Shared formatting
    # -------------------------------------------------------------------------

    @classmethod
    def _format_transcript_string(cls, words: list[dict]) -> str:
        """
        Format word list into the [MM:SS - MM:SS] segment format expected by
        the AI analysis step.
        """
        # Local import to avoid circular dependency with video_utils
        from ..video_utils import format_ms_to_timestamp

        formatted_lines: list[str] = []
        current_segment: list[str] = []
        current_start: Optional[int] = None
        segment_word_count = 0
        max_words_per_segment = 8

        for word in words:
            if current_start is None:
                current_start = word["start"]

            current_segment.append(word["text"])
            segment_word_count += 1

            is_sentence_end = word["text"].endswith((".", "!", "?"))
            if (
                segment_word_count >= max_words_per_segment
                or is_sentence_end
            ):
                start_time = format_ms_to_timestamp(current_start)
                end_time = format_ms_to_timestamp(word["end"])
                formatted_lines.append(
                    f"[{start_time} - {end_time}] {' '.join(current_segment)}"
                )
                current_segment = []
                current_start = None
                segment_word_count = 0

        if current_segment and current_start is not None:
            start_time = format_ms_to_timestamp(current_start)
            end_time = format_ms_to_timestamp(words[-1]["end"])
            formatted_lines.append(
                f"[{start_time} - {end_time}] {' '.join(current_segment)}"
            )

        result = "\n".join(formatted_lines)
        logger.info(
            "[TranscriptionService] formatted transcript: %d segments, %d chars",
            len(formatted_lines),
            len(result),
        )
        return result

    # -------------------------------------------------------------------------
    # AssemblyAI fallback path
    # -------------------------------------------------------------------------

    @classmethod
    def _transcribe_with_assemblyai(
        cls, video_path: Path, speech_model: str = "best"
    ) -> str:
        """Transcribe using AssemblyAI (fallback). Mirrors original logic from video_utils.py."""
        import assemblyai as aai
        from ..config import Config

        # Local imports to avoid circular dependency with video_utils
        from ..video_utils import format_ms_to_timestamp, cache_transcript_data

        config = Config()
        logger.info(
            "[TranscriptionService] AssemblyAI transcription: %s", video_path
        )

        aai.settings.api_key = config.assembly_ai_api_key

        transcriber = aai.Transcriber()

        speech_model_value = aai.SpeechModel.best
        if speech_model == "nano":
            speech_model_value = aai.SpeechModel.nano

        language_hint = (config.transcription_language_hint or "").strip().lower()
        language_code = (
            language_hint if (language_hint and language_hint not in {"auto", "none"}) else None
        )

        config_obj = aai.TranscriptionConfig(
            speaker_labels=False,
            punctuate=True,
            format_text=True,
            speech_model=speech_model_value,
            language_code=language_code,
        )

        logger.info("[TranscriptionService] Starting AssemblyAI transcription")
        transcript = transcriber.transcribe(str(video_path), config=config_obj)

        if transcript.status == aai.TranscriptStatus.error:
            logger.error(
                "[TranscriptionService] AssemblyAI failed: %s", transcript.error
            )
            raise Exception(
                f"AssemblyAI transcription failed: {transcript.error}"
            )

        formatted_lines: list[str] = []
        if transcript.words:
            logger.info(
                "[TranscriptionService] Processing %d words from AssemblyAI",
                len(transcript.words),
            )

            current_segment: list[str] = []
            current_start: Optional[int] = None
            segment_word_count = 0
            max_words_per_segment = 8

            for word in transcript.words:
                if current_start is None:
                    current_start = word.start
                current_segment.append(word.text)
                segment_word_count += 1

                if (
                    segment_word_count >= max_words_per_segment
                    or word.text.endswith(".")
                    or word.text.endswith("!")
                    or word.text.endswith("?")
                ):
                    start_time = format_ms_to_timestamp(current_start)
                    end_time = format_ms_to_timestamp(word.end)
                    formatted_lines.append(
                        f"[{start_time} - {end_time}] {' '.join(current_segment)}"
                    )
                    current_segment = []
                    current_start = None
                    segment_word_count = 0

            if current_segment and current_start is not None:
                start_time = format_ms_to_timestamp(current_start)
                end_time = format_ms_to_timestamp(transcript.words[-1].end)
                formatted_lines.append(
                    f"[{start_time} - {end_time}] {' '.join(current_segment)}"
                )

        cache_transcript_data(video_path, transcript)

        result = "\n".join(formatted_lines)
        logger.info(
            "[TranscriptionService] AssemblyAI done: %d segments", len(formatted_lines)
        )
        return result
