"""
Hybrid transcription service: Gemini (primary) → AssemblyAI (fallback).
Supports Dynamic User-specific API Keys and asynchronous processing.
"""

import json
import logging
import subprocess
import tempfile
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List
from sqlalchemy import select

from ..config import Config
from ..models import User

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
        """Derives the raw Gemini model name from config.llm."""
        if llm_config and llm_config.startswith("google-gla:"):
            return llm_config.split(":", 1)[1]
        return "gemini-2.5-flash"

    @classmethod
    async def run_health_check(cls) -> bool:
        """Tests Gemini with a simple ping and sets _gemini_available."""
        config = Config()
        if not config.google_api_key:
            cls._gemini_available = False
            cls._health_check_done = True
            return False

        try:
            from google import genai
            client = genai.Client(api_key=config.google_api_key)
            model_name = cls._resolve_gemini_model(config.llm)
            client.models.generate_content(model=model_name, contents="ping")
            cls._gemini_available = True
            cls._health_check_done = True
            logger.info("[TranscriptionService] Gemini health check passed")
            return True
        except Exception as exc:
            cls._gemini_available = False
            cls._health_check_done = True
            logger.warning(f"[TranscriptionService] Gemini health check failed: {exc}")
            return False

    @classmethod
    async def transcribe(cls, db, video_path: Path, user_id: Optional[str] = None, speech_model: str = "best") -> str:
        """
        Transcribe video/audio with dynamic key support and async flow.
        Prioritizes User-specific API Keys from DB.
        """
        config = Config()
        user_google_key = None
        user_assembly_key = None
        
        if user_id:
            logger.info(f"🔍 [Transcription] Fetching custom keys for user {user_id}")
            result = await db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if user:
                user_google_key = user.google_api_key
                user_assembly_key = user.assembly_ai_api_key
                if user_google_key: logger.info("💎 [Auth] Using user Google API key")
                if user_assembly_key: logger.info("💎 [Auth] Using user AssemblyAI API key")

        # Try Gemini Path
        if cls._gemini_available or user_google_key:
            try:
                target_key = user_google_key or config.google_api_key
                return await cls._transcribe_with_gemini(video_path, api_key=target_key)
            except Exception as exc:
                logger.error(f"❌ [Transcription] Gemini failed: {exc}. Falling back to AssemblyAI.")

        # Fallback to AssemblyAI
        target_aai_key = user_assembly_key or config.assembly_ai_api_key
        return await cls._transcribe_with_assemblyai(video_path, speech_model, api_key=target_aai_key)

    # -------------------------------------------------------------------------
    # Audio helpers (unchanged but called via await run_in_thread)
    # -------------------------------------------------------------------------

    @classmethod
    async def _transcribe_with_gemini(cls, video_path: Path, api_key: str) -> str:
        """Transcribe using Gemini with provided API key."""
        from ..video_utils import run_in_thread
        
        logger.info(f"🚀 [Transcription] Starting Gemini flow for {video_path.name}")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            ogg_path = tmp / "audio.ogg"

            await run_in_thread(cls._extract_audio_ogg, video_path, ogg_path)
            duration = await run_in_thread(cls._get_audio_duration_seconds, ogg_path)
            
            all_words: list[dict] = []
            full_text_parts: list[str] = []

            if duration <= CHUNK_DURATION_SECONDS:
                data = await cls._call_gemini_transcribe(ogg_path, api_key=api_key)
                all_words = data.get("words", [])
                full_text_parts = [data.get("full_text", "")]
            else:
                chunks_dir = tmp / "chunks"
                chunks_dir.mkdir()
                chunk_paths = await run_in_thread(cls._chunk_audio, ogg_path, chunks_dir)

                offset_ms = 0
                for i, chunk_path in enumerate(chunk_paths):
                    logger.info(f"⏳ [Transcription] Processing chunk {i+1}/{len(chunk_paths)}")
                    data = await cls._call_gemini_transcribe(chunk_path, chunk_offset_ms=offset_ms, api_key=api_key)
                    all_words.extend(data.get("words", []))
                    full_text_parts.append(data.get("full_text", ""))
                    offset_ms += int(CHUNK_DURATION_SECONDS * 1000)

            full_text = " ".join(p for p in full_text_parts if p)
            cache_data = {
                "words": [{"text": w["text"], "start": w["start_ms"], "end": w["end_ms"], "confidence": 1.0} for w in all_words],
                "text": full_text,
            }
            
            cache_path = video_path.with_suffix(".transcript_cache.json")
            with open(cache_path, "w") as f:
                json.dump(cache_data, f)
            
            return cls._format_transcript_string(cache_data["words"])

    @classmethod
    async def _call_gemini_transcribe(cls, audio_path: Path, chunk_offset_ms: int = 0, api_key: str = None) -> dict:
        """Send a single audio chunk to Gemini."""
        from google import genai
        from google.genai import types
        config = Config()
        client = genai.Client(api_key=api_key)
        
        audio_bytes = audio_path.read_bytes()
        audio_part = types.Part.from_bytes(data=audio_bytes, mime_type="audio/ogg")

        prompt = TRANSCRIPTION_PROMPT
        if config.transcription_language_hint == "pt":
            prompt = "Language: pt-BR. " + TRANSCRIPTION_PROMPT

        response = client.models.generate_content(
            model=cls._resolve_gemini_model(config.llm),
            contents=[audio_part, prompt],
        )

        raw = response.text.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0]

        data = json.loads(raw)
        if chunk_offset_ms > 0:
            for word in data.get("words", []):
                word["start_ms"] += chunk_offset_ms
                word["end_ms"] += chunk_offset_ms
        return data

    @classmethod
    async def _transcribe_with_assemblyai(cls, video_path: Path, speech_model: str, api_key: str) -> str:
        """Transcribe using AssemblyAI with provided API key."""
        import assemblyai as aai
        from ..video_utils import format_ms_to_timestamp, cache_transcript_data, run_in_thread
        config = Config()
        
        logger.info(f"🚀 [Transcription] Starting AssemblyAI flow (Key: {api_key[:8]}...)")
        aai.settings.api_key = api_key
        transcriber = aai.Transcriber()

        config_obj = aai.TranscriptionConfig(
            speaker_labels=False, punctuate=True, format_text=True,
            speech_models=["universal-3-pro"],
            language_code="pt" if config.transcription_language_hint == "pt" else None
        )

        transcript = await run_in_thread(transcriber.transcribe, str(video_path), config=config_obj)

        if transcript.status == aai.TranscriptStatus.error:
            logger.error(f"❌ [AssemblyAI] Error: {transcript.error}")
            raise Exception(f"AssemblyAI failed: {transcript.error}")

        # Formatting logic (keep original MM:SS format)
        words = transcript.words
        formatted_lines = []
        if words:
            current_segment, current_start, segment_word_count = [], None, 0
            for word in words:
                if current_start is None: current_start = word.start
                current_segment.append(word.text)
                segment_word_count += 1
                if segment_word_count >= 8 or word.text.endswith((".", "!", "?")):
                    formatted_lines.append(f"[{format_ms_to_timestamp(current_start)} - {format_ms_to_timestamp(word.end)}] {' '.join(current_segment)}")
                    current_segment, current_start, segment_word_count = [], None, 0
        
        cache_transcript_data(video_path, transcript)
        return "\n".join(formatted_lines)

    @classmethod
    def _extract_audio_ogg(cls, video_path: Path, output_path: Path) -> None:
        cmd = ["ffmpeg", "-y", "-i", str(video_path), "-vn", "-c:a", "libvorbis", "-ac", "1", "-ar", "16000", "-q:a", "4", str(output_path)]
        subprocess.run(cmd, capture_output=True, check=True)

    @classmethod
    def _get_audio_duration_seconds(cls, audio_path: Path) -> float:
        cmd = ["ffprobe", "-v", "-show_entries", "format=duration", "-of", "csv=p=0", str(audio_path)]
        return float(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip())

    @classmethod
    def _chunk_audio(cls, audio_path: Path, chunks_dir: Path) -> list[Path]:
        output_pattern = str(chunks_dir / "chunk_%03d.ogg")
        cmd = ["ffmpeg", "-y", "-i", str(audio_path), "-f", "segment", "-segment_time", str(CHUNK_DURATION_SECONDS), "-c:a", "libvorbis", "-q:a", "3", output_pattern]
        subprocess.run(cmd, capture_output=True, check=True)
        return sorted(chunks_dir.glob("chunk_*.ogg"))

    @classmethod
    def _format_transcript_string(cls, words: list[dict]) -> str:
        from ..video_utils import format_ms_to_timestamp
        lines, cur_seg, cur_start, count = [], [], None, 0
        for w in words:
            if cur_start is None: cur_start = w["start"]
            cur_seg.append(w["text"])
            count += 1
            if count >= 8 or w["text"].endswith((".", "!", "?")):
                lines.append(f"[{format_ms_to_timestamp(cur_start)} - {format_ms_to_timestamp(w['end'])}] {' '.join(cur_seg)}")
                cur_seg, cur_start, count = [], None, 0
        return "\n".join(lines)
