from __future__ import annotations

from pydantic import BaseModel, Field


class VideoUploadResponse(BaseModel):
    video_url: str = Field(
        ...,
        description="Opaque URL to be used as source.url for clipping jobs. Format: upload://<filename>",
        examples=["upload://b2a9c4d1-acde-4d1c-9a5d-3f14d2a1c1b2.mp4"],
    )


class SourceInput(BaseModel):
    url: str = Field(..., description="YouTube URL, direct URL, or upload://<filename>")
    title: str | None = Field(None, description="Optional title override")


class StartClippingJobRequest(BaseModel):
    source: SourceInput
    processing_mode: str | None = Field(
        None, description="fast|balanced|quality (defaults to server config)"
    )
    output_format: str | None = Field(None, description="vertical|original")
    add_subtitles: bool | None = Field(None, description="Whether to burn subtitles")
    video_quality: str | None = Field(None, description="best|1080p|720p|480p")

    font_family: str | None = None
    font_size: int | None = None
    font_color: str | None = None
    caption_template: str | None = None
    include_broll: bool | None = None


class StartClippingJobResponse(BaseModel):
    task_id: str
    queue_job_id: str


class JobStatusResponse(BaseModel):
    task_id: str
    status: str | None = None
    progress: int | None = None
    message: str | None = None


class ClipListResponse(BaseModel):
    task_id: str
    total_clips: int
    clips: list[dict]


class ApiKeyCreateRequest(BaseModel):
    name: str = Field(..., max_length=120)
    scopes: list[str] = Field(default_factory=list)


class ApiKeyCreateResponse(BaseModel):
    id: str
    prefix: str
    name: str
    scopes: list[str]
    api_key: str = Field(..., description="Secret token. Visible only once at creation.")


class ApiKeyListItem(BaseModel):
    id: str
    prefix: str
    name: str
    scopes: list[str]
    last_used_at: str | None = None
    revoked_at: str | None = None
    created_at: str


class ApiKeyListResponse(BaseModel):
    keys: list[ApiKeyListItem]

