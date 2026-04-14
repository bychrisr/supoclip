from __future__ import annotations

import logging
import re
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional
from urllib.parse import parse_qs, urlparse

import httpx

from ..config import Config
from ..utils.ssrf import validate_external_url

logger = logging.getLogger(__name__)
config = Config()


@dataclass(frozen=True)
class ResolvedImport:
    provider: str
    original_url: str
    download_url: str
    title: str | None
    filename: str | None
    headers: dict[str, str]


class ImportError(ValueError):
    pass


class ImportAdapter:
    provider: str

    async def resolve(self, *, source_url: str, api_token: str | None) -> ResolvedImport:
        raise NotImplementedError


class GoogleDriveAdapter(ImportAdapter):
    provider = "google_drive"

    _ID_PATTERNS = [
        re.compile(r"https?://drive\.google\.com/file/d/(?P<id>[a-zA-Z0-9_-]+)", re.I),
        re.compile(r"https?://drive\.google\.com/open\?id=(?P<id>[a-zA-Z0-9_-]+)", re.I),
        re.compile(r"https?://drive\.google\.com/uc\?export=download&id=(?P<id>[a-zA-Z0-9_-]+)", re.I),
        re.compile(r"https?://docs\.google\.com/uc\?export=download&id=(?P<id>[a-zA-Z0-9_-]+)", re.I),
    ]

    def _extract_file_id(self, url: str) -> str | None:
        for pat in self._ID_PATTERNS:
            m = pat.search(url)
            if m:
                return m.group("id")
        try:
            parsed = urlparse(url)
            q = parse_qs(parsed.query)
            if "id" in q and q["id"]:
                return q["id"][0]
        except Exception:
            return None
        return None

    async def resolve(self, *, source_url: str, api_token: str | None) -> ResolvedImport:
        file_id = self._extract_file_id(source_url)
        if not file_id:
            raise ImportError("Could not extract Google Drive file id from URL")

        # Two modes:
        # - Public share: use drive.google.com/uc export=download
        # - API token: use Google Drive API alt=media
        if api_token:
            download_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
            headers = {"Authorization": f"Bearer {api_token}"}
            return ResolvedImport(
                provider=self.provider,
                original_url=source_url,
                download_url=download_url,
                title=None,
                filename=None,
                headers=headers,
            )

        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        return ResolvedImport(
            provider=self.provider,
            original_url=source_url,
            download_url=download_url,
            title=None,
            filename=None,
            headers={},
        )


class VimeoAdapter(ImportAdapter):
    provider = "vimeo"

    _VIMEO_ID = re.compile(r"(?:vimeo\.com/(?:video/)?)(?P<id>\d+)", re.I)

    def _extract_video_id(self, url: str) -> str | None:
        m = self._VIMEO_ID.search(url)
        if m:
            return m.group("id")
        return None

    async def resolve(self, *, source_url: str, api_token: str | None) -> ResolvedImport:
        video_id = self._extract_video_id(source_url)
        if not video_id:
            raise ImportError("Could not extract Vimeo video id from URL")

        # Public Vimeo pages do not reliably provide a direct downloadable MP4.
        # If a dev token is provided, use the Vimeo API to find a downloadable file.
        if not api_token:
            raise ImportError(
                "Vimeo imports require an API token for now (or provide a direct download URL)."
            )

        headers = {"Authorization": f"Bearer {api_token}"}
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(f"https://api.vimeo.com/videos/{video_id}", headers=headers)
            if resp.status_code == 401:
                raise ImportError("Vimeo API token unauthorized")
            if resp.status_code >= 400:
                raise ImportError(f"Vimeo API error: {resp.status_code}")
            data = resp.json()

        title = data.get("name") if isinstance(data, dict) else None
        downloads = data.get("download") if isinstance(data, dict) else None
        if not isinstance(downloads, list) or not downloads:
            raise ImportError(
                "No downloadable files available for this Vimeo video. Provide a direct download URL instead."
            )

        # Pick the best-ish download link (largest size), fallback first link
        best: Mapping[str, Any] | None = None
        for item in downloads:
            if not isinstance(item, dict):
                continue
            if not item.get("link"):
                continue
            if best is None:
                best = item
                continue
            try:
                if int(item.get("size") or 0) > int(best.get("size") or 0):
                    best = item
            except Exception:
                pass

        link = (best or {}).get("link") if best else None
        if not isinstance(link, str) or not link:
            raise ImportError("Could not resolve a Vimeo download link")

        filename = (best or {}).get("filename") if best else None
        if not isinstance(filename, str) or not filename.strip():
            filename = None

        return ResolvedImport(
            provider=self.provider,
            original_url=source_url,
            download_url=link,
            title=title if isinstance(title, str) and title.strip() else None,
            filename=filename,
            headers={},
        )


class LoomAdapter(ImportAdapter):
    provider = "loom"

    _LOOM_ID = re.compile(r"loom\.com/(?:share|embed)/(?P<id>[a-zA-Z0-9]+)", re.I)

    def _extract_id(self, url: str) -> str | None:
        m = self._LOOM_ID.search(url)
        if m:
            return m.group("id")
        return None

    async def resolve(self, *, source_url: str, api_token: str | None) -> ResolvedImport:
        _ = api_token  # reserved for future OAuth/token flow
        loom_id = self._extract_id(source_url)
        if not loom_id:
            raise ImportError("Could not extract Loom share id from URL")

        # Loom commonly supports direct MP4 at /share/<id>.mp4 for public shares.
        download_url = f"https://www.loom.com/share/{loom_id}.mp4"
        return ResolvedImport(
            provider=self.provider,
            original_url=source_url,
            download_url=download_url,
            title=None,
            filename=f"{loom_id}.mp4",
            headers={},
        )


class DirectUrlAdapter(ImportAdapter):
    provider = "direct"

    async def resolve(self, *, source_url: str, api_token: str | None) -> ResolvedImport:
        _ = api_token
        return ResolvedImport(
            provider=self.provider,
            original_url=source_url,
            download_url=source_url,
            title=None,
            filename=None,
            headers={},
        )


class ImportService:
    def __init__(self):
        self._adapters: list[ImportAdapter] = [
            GoogleDriveAdapter(),
            VimeoAdapter(),
            LoomAdapter(),
            DirectUrlAdapter(),
        ]

    def _pick_adapter(self, provider: str | None, source_url: str) -> ImportAdapter:
        if provider:
            for ad in self._adapters:
                if ad.provider == provider:
                    return ad
            raise ImportError(f"Unknown provider: {provider}")

        host = (urlparse(source_url).hostname or "").lower()
        if "drive.google.com" in host or "docs.google.com" in host:
            return GoogleDriveAdapter()
        if "vimeo.com" in host:
            return VimeoAdapter()
        if "loom.com" in host:
            return LoomAdapter()
        return DirectUrlAdapter()

    async def resolve_import(
        self,
        *,
        provider: str | None,
        source_url: str,
        api_token: str | None,
    ) -> ResolvedImport:
        adapter = self._pick_adapter(provider, source_url)
        resolved = await adapter.resolve(source_url=source_url, api_token=api_token)

        safety = validate_external_url(resolved.download_url, allowed_hosts=config.import_allowed_hosts)
        if not safety.ok:
            raise ImportError(f"Unsafe download URL: {safety.reason}")

        return resolved

    async def download_to_upload(
        self,
        *,
        resolved: ResolvedImport,
    ) -> dict[str, Any]:
        """
        Download the resolved URL to TEMP_DIR/uploads and return upload:// reference.
        Implements redirect + size limit enforcement to reduce SSRF and memory risk.
        """
        uploads_dir = Path(config.temp_dir) / "uploads"
        uploads_dir.mkdir(parents=True, exist_ok=True)

        requested_name = resolved.filename or Path(urlparse(resolved.download_url).path).name
        suffix = Path(requested_name).suffix if requested_name else ""
        if not suffix or len(suffix) > 10:
            suffix = ".mp4"

        unique_filename = f"{uuid.uuid4()}{suffix}"
        target = uploads_dir / unique_filename

        max_bytes = int(config.import_max_file_bytes)
        max_redirects = int(config.import_max_redirects)

        async with httpx.AsyncClient(
            timeout=httpx.Timeout(
                connect=config.import_connect_timeout_seconds,
                read=config.import_read_timeout_seconds,
                write=config.import_read_timeout_seconds,
                pool=config.import_connect_timeout_seconds,
            ),
            headers={"User-Agent": config.import_user_agent},
            follow_redirects=False,
        ) as client:
            url = resolved.download_url
            headers: dict[str, str] = dict(resolved.headers or {})

            for _ in range(max_redirects + 1):
                # HEAD first to preflight size if available
                head = await client.head(url, headers=headers)
                if head.status_code in {301, 302, 303, 307, 308}:
                    loc = head.headers.get("location")
                    if not loc:
                        raise ImportError("Redirect without location header")
                    next_url = httpx.URL(url).join(loc).human_repr()
                    safety = validate_external_url(next_url, allowed_hosts=config.import_allowed_hosts)
                    if not safety.ok:
                        raise ImportError(f"Unsafe redirect URL: {safety.reason}")
                    url = next_url
                    continue

                if head.status_code >= 400 and head.status_code != 405:
                    raise ImportError(f"Upstream returned {head.status_code}")

                content_length = head.headers.get("content-length")
                if content_length:
                    try:
                        size = int(content_length)
                        if size > max_bytes:
                            raise ImportError("File is too large")
                    except ValueError:
                        pass

                # GET stream
                resp = await client.get(url, headers=headers)
                if resp.status_code in {301, 302, 303, 307, 308}:
                    loc = resp.headers.get("location")
                    if not loc:
                        raise ImportError("Redirect without location header")
                    next_url = httpx.URL(url).join(loc).human_repr()
                    safety = validate_external_url(next_url, allowed_hosts=config.import_allowed_hosts)
                    if not safety.ok:
                        raise ImportError(f"Unsafe redirect URL: {safety.reason}")
                    url = next_url
                    continue

                if resp.status_code >= 400:
                    raise ImportError(f"Upstream returned {resp.status_code}")

                written = 0
                try:
                    with target.open("wb") as f:
                        async for chunk in resp.aiter_bytes(chunk_size=1024 * 1024):
                            if not chunk:
                                continue
                            written += len(chunk)
                            if written > max_bytes:
                                raise ImportError("File exceeded size limit while downloading")
                            f.write(chunk)
                except Exception:
                    try:
                        if target.exists():
                            target.unlink()
                    except Exception:
                        pass
                    raise

                return {
                    "provider": resolved.provider,
                    "source_url": resolved.original_url,
                    "download_url": url,
                    "video_path": f"upload://{unique_filename}",
                    "bytes": written,
                    "title": resolved.title,
                }

            raise ImportError("Too many redirects")

