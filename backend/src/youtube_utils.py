"""
Utility functions for YouTube-related operations.
Optimized for high-quality downloads and better error handling.
"""

import re
from urllib.parse import urlparse, parse_qs
import yt_dlp
from typing import Optional, Dict, Any
from pathlib import Path
import logging
import time
import subprocess

from .config import Config

logger = logging.getLogger(__name__)
config = Config()


class YouTubeDownloader:
    """Enhanced YouTube downloader with optimized settings."""

    def __init__(self):
        self.temp_dir = Path(config.temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    # Mapeamento de qualidade → (format string, format_sort)
    _QUALITY_FORMAT_MAP: Dict[str, tuple[str, list[str]]] = {
        "best": (
            "bestvideo*+bestaudio/best",
            ["res", "fps"],
        ),
        "1080p": (
            "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
            ["res:1080", "fps"],
        ),
        "720p": (
            "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]/best",
            ["res:720", "fps"],
        ),
        "480p": (
            "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best[height<=480]/best",
            ["res:480", "fps"],
        ),
    }

    def get_optimal_download_options(
        self,
        video_id: str,
        progress_hooks: Optional[list] = None,
        video_quality: str = "best",
    ) -> Dict[str, Any]:
        """Get optimal yt-dlp options for high-quality downloads with enhanced YouTube bypass."""
        output_path = self.temp_dir / f"{video_id}.%(ext)s"

        quality = video_quality if video_quality in self._QUALITY_FORMAT_MAP else "best"
        fmt, fmt_sort = self._QUALITY_FORMAT_MAP[quality]
        logger.debug(f"[get_optimal_download_options] quality={quality} format={fmt!r}")

        return {
            "outtmpl": str(output_path),
            "format": fmt,
            "format_sort": fmt_sort,
            "merge_output_format": "mp4",
            "writesubtitles": False,
            "writeautomaticsub": False,
            "noplaylist": True,
            "overwrites": True,
            # Otimizado para velocidade e confiabilidade
            "socket_timeout": 30,
            "retries": 5,
            "fragment_retries": 5,
            "http_chunk_size": 10485760,  # 10MB chunks
            # Progresso em tempo real via hooks
            "progress_hooks": progress_hooks or [],
            "quiet": True,
            "no_warnings": False,
            "ignoreerrors": False,
            # Headers para evitar 403
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            },
            "extract_flat": False,
            "writeinfojson": False,
            "nocheckcertificate": True,
            "prefer_insecure": False,
            "age_limit": None,
            # Player clients para melhorar compatibilidade
            "extractor_args": {
                "youtube": {
                    "player_client": ["web", "android"],
                }
            },
            # Usar node como runtime JS para decriptar URLs de alta qualidade
            "js_runtimes": {"node": {}},
        }


def _get_local_video_dimensions(path: Path) -> tuple[int, int]:
    """Return local video width/height using ffprobe."""
    try:
        command = [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height",
            "-of",
            "csv=s=x:p=0",
            str(path),
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        if not output or "x" not in output:
            return (0, 0)
        width_str, height_str = output.split("x", 1)
        return (int(width_str), int(height_str))
    except Exception:
        return (0, 0)


def get_youtube_video_id(url: str) -> Optional[str]:
    """
    Extract YouTube video ID from various URL formats.
    Supports standard, short, embed, and mobile URLs.
    """
    if not isinstance(url, str) or not url.strip():
        return None

    url = url.strip()

    # Comprehensive regex patterns for different YouTube URL formats
    patterns = [
        r"(?:youtube\.com/(?:.*v=|v/|embed/|shorts/)|youtu\.be/)([A-Za-z0-9_-]{11})",
        r"youtube\.com/watch\?v=([A-Za-z0-9_-]{11})",
        r"youtube\.com/embed/([A-Za-z0-9_-]{11})",
        r"youtube\.com/v/([A-Za-z0-9_-]{11})",
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"youtube\.com/shorts/([A-Za-z0-9_-]{11})",
        r"m\.youtube\.com/watch\?v=([A-Za-z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            video_id = match.group(1)
            # Validate video ID length (YouTube IDs are always 11 characters)
            if len(video_id) == 11:
                return video_id

    # Fallback: parse query parameters
    try:
        parsed_url = urlparse(url)
        if "youtube.com" in parsed_url.netloc.lower():
            query = parse_qs(parsed_url.query)
            video_ids = query.get("v")
            if video_ids and len(video_ids[0]) == 11:
                return video_ids[0]
    except Exception as e:
        logger.warning(f"Error parsing URL query parameters: {e}")

    return None


def validate_youtube_url(url: str) -> bool:
    """Validate if URL is a proper YouTube URL."""
    video_id = get_youtube_video_id(url)
    return video_id is not None


def get_youtube_video_info(url: str) -> Optional[Dict[str, Any]]:
    """
    Get comprehensive video information without downloading.
    Returns title, duration, description, and other metadata.
    """
    video_id = get_youtube_video_id(url)
    if not video_id:
        logger.error(f"Invalid YouTube URL: {url}")
        return None

    try:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extractaudio": False,
            "skip_download": True,
            "socket_timeout": 30,
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
            },
            "nocheckcertificate": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            return {
                "id": info.get("id"),
                "title": info.get("title"),
                "description": info.get("description", ""),
                "duration": info.get("duration"),
                "uploader": info.get("uploader"),
                "upload_date": info.get("upload_date"),
                "view_count": info.get("view_count"),
                "like_count": info.get("like_count"),
                "thumbnail": info.get("thumbnail"),
                "format_id": info.get("format_id"),
                "resolution": info.get("resolution"),
                "fps": info.get("fps"),
                "filesize": info.get("filesize"),
            }

    except Exception as e:
        logger.error(f"Error extracting video info: {e}")
        return None


def get_youtube_video_title(url: str) -> Optional[str]:
    """
    Get the title of a YouTube video from a URL.
    Enhanced with better error handling and validation.
    """
    video_info = get_youtube_video_info(url)
    return video_info.get("title") if video_info else None


def download_youtube_video(
    url: str,
    max_retries: int = 3,
    progress_cb: Optional[Any] = None,
    video_quality: str = "best",
) -> Optional[Path]:
    """
    Download YouTube video com retry e progresso em tempo real.

    progress_cb: callable síncrono chamado com (percent: float, downloaded_bytes: int,
                 total_bytes: int, speed: str, eta: int) durante o download.
                 Chamado no máximo 1x por segundo para não saturar Redis.
    """
    logger.info(f"Starting YouTube download: {url} quality={video_quality!r}")

    video_id = get_youtube_video_id(url)
    if not video_id:
        logger.error(f"Could not extract video ID from URL: {url}")
        return None

    downloader = YouTubeDownloader()

    # Reutiliza arquivo existente se já foi baixado com qualidade suficiente (≥480p).
    # Evita re-download em tarefas paralelas ou retry para o mesmo vídeo.
    video_extensions = {".mp4", ".mkv", ".webm"}
    cached_files = [
        f for f in downloader.temp_dir.glob(f"{video_id}.*")
        if f.is_file() and f.suffix.lower() in video_extensions and not f.name.endswith(".part")
    ]
    if cached_files:
        best = max(cached_files, key=lambda f: f.stat().st_size)
        width, height = _get_local_video_dimensions(best)
        if height >= 480:
            logger.info(
                f"Reusing cached file: {best.name} ({best.stat().st_size // 1024 // 1024}MB, {width}x{height})"
            )
            if progress_cb:
                progress_cb(100.0, best.stat().st_size, best.stat().st_size, "N/A", 0)
            return best
        # Baixa qualidade demais — apaga e baixa de novo
        logger.info(f"Cached file too low quality ({height}p), re-downloading")
        for f in cached_files:
            try:
                f.unlink()
            except Exception as e:
                logger.warning(f"Failed to remove stale cache: {f}: {e}")

    # Info do vídeo para log e validação
    video_info = get_youtube_video_info(url)
    if not video_info:
        logger.error(f"Could not retrieve video information for: {url}")
        return None

    logger.info(f"Video: '{video_info.get('title')}' ({video_info.get('duration')}s)")

    duration = video_info.get("duration", 0)
    if duration > 3600:
        logger.warning(f"Video duration ({duration}s) exceeds 1h — may take a while")

    # Hook de progresso para o yt-dlp — chamado a cada chunk baixado.
    # _last_report[0] = último percent emitido, _last_report[1] = último timestamp
    _last_report = [0.0, 0.0]

    def _yt_dlp_progress_hook(d: dict) -> None:
        if not progress_cb or d.get("status") != "downloading":
            return
        total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
        downloaded = d.get("downloaded_bytes") or 0
        percent = (downloaded / total * 100.0) if total > 0 else 0.0
        now = time.monotonic()
        # Emite se avançou ≥1% ou passou ≥1s desde o último report
        if percent - _last_report[0] >= 1.0 or now - _last_report[1] >= 1.0:
            _last_report[0] = percent
            _last_report[1] = now
            speed = d.get("_speed_str", "N/A")
            eta = d.get("eta") or 0
            try:
                progress_cb(percent, downloaded, total, speed, eta)
            except Exception:
                pass

    # Retry com backoff exponencial
    for attempt in range(max_retries):
        try:
            logger.info(f"Download attempt {attempt + 1}/{max_retries}")

            ydl_opts = downloader.get_optimal_download_options(
                video_id,
                progress_hooks=[_yt_dlp_progress_hook],
                video_quality=video_quality,
            )

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

                logger.info(f"Searching for downloaded file: {video_id}.*")
                downloaded_files = [
                    f for f in downloader.temp_dir.glob(f"{video_id}.*")
                    if f.is_file() and f.suffix.lower() in video_extensions and not f.name.endswith(".part")
                ]
                if downloaded_files:
                    ranked = []
                    for candidate in downloaded_files:
                        width, height = _get_local_video_dimensions(candidate)
                        ranked.append((height, width, candidate.stat().st_size, candidate))
                    ranked.sort(reverse=True)
                    best_file = ranked[0][3]
                    file_size = best_file.stat().st_size
                    width, height = _get_local_video_dimensions(best_file)
                    logger.info(
                        f"Download successful: {best_file.name} ({file_size // 1024 // 1024}MB, {width}x{height})"
                    )
                    return best_file

                logger.warning(f"No video file found after download attempt {attempt + 1}")

        except yt_dlp.utils.DownloadError as e:
            logger.warning(f"Download attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.info(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"All download attempts failed for: {url}")

        except Exception as e:
            logger.error(f"Unexpected error during download attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.info(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"All download attempts failed for: {url}")

    return None


def get_video_duration(url: str) -> Optional[int]:
    """Get video duration in seconds without downloading."""
    video_info = get_youtube_video_info(url)
    return video_info.get("duration") if video_info else None


def is_video_suitable_for_processing(
    url: str, min_duration: int = 60, max_duration: int = 7200
) -> bool:
    """
    Check if video is suitable for processing based on duration and other factors.
    Default limits: 1 minute to 2 hours.
    """
    video_info = get_youtube_video_info(url)
    if not video_info:
        return False

    duration = video_info.get("duration", 0)

    # Check duration constraints
    if duration < min_duration or duration > max_duration:
        logger.warning(
            f"Video duration {duration}s outside allowed range ({min_duration}-{max_duration}s)"
        )
        return False

    # Additional checks could go here (e.g., content type, quality, etc.)

    return True


def cleanup_downloaded_files(video_id: str):
    """Clean up downloaded files for a specific video ID."""
    temp_dir = Path(config.temp_dir)

    for file_path in temp_dir.glob(f"{video_id}.*"):
        try:
            if file_path.is_file():
                file_path.unlink()
                logger.info(f"Cleaned up: {file_path.name}")
        except Exception as e:
            logger.warning(f"Failed to cleanup {file_path.name}: {e}")


# Backward compatibility functions
def extract_video_id(url: str) -> Optional[str]:
    """Backward compatibility wrapper."""
    return get_youtube_video_id(url)
