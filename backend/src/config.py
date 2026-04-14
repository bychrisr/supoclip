from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    def __init__(self):
        self.openai_api_key = self._get_optional_env("OPENAI_API_KEY")
        self.anthropic_api_key = self._get_optional_env("ANTHROPIC_API_KEY")
        self.google_api_key = self._get_optional_env("GOOGLE_API_KEY")
        self.ollama_base_url = self._get_optional_env("OLLAMA_BASE_URL")
        self.ollama_api_key = self._get_optional_env("OLLAMA_API_KEY")

        self.whisper_model = os.getenv("WHISPER_MODEL", "base")
        self.llm = self._get_optional_env("LLM") or self._infer_default_llm()
        self.assembly_ai_api_key = os.getenv("ASSEMBLY_AI_API_KEY")
        self.pexels_api_key = os.getenv("PEXELS_API_KEY")

        self.max_video_duration = int(os.getenv("MAX_VIDEO_DURATION", "3600"))
        self.output_dir = os.getenv("OUTPUT_DIR", "outputs")

        self.max_clips = int(os.getenv("MAX_CLIPS", "10"))
        self.clip_duration = int(os.getenv("CLIP_DURATION", "30"))  # seconds

        self.temp_dir = os.getenv("TEMP_DIR", "temp")

        # Redis configuration
        self.redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_port = int(os.getenv("REDIS_PORT", "6379"))

        # Fail-safe: queued tasks should not stay queued forever
        self.queued_task_timeout_seconds = int(
            os.getenv("QUEUED_TASK_TIMEOUT_SECONDS", "180")
        )

        self.self_host = self._get_bool_env("SELF_HOST", True)
        self.monetization_enabled = not self.self_host
        self.backend_auth_secret = self._get_optional_env("BACKEND_AUTH_SECRET")
        self.auth_signature_ttl_seconds = int(
            os.getenv("AUTH_SIGNATURE_TTL_SECONDS", "300")
        )
        self.free_plan_task_limit = int(os.getenv("FREE_PLAN_TASK_LIMIT", "10"))
        self.pro_plan_task_limit = int(os.getenv("PRO_PLAN_TASK_LIMIT", "0"))
        self.cors_origins = self._get_csv_env(
            "CORS_ORIGINS",
            [
                "http://localhost:3000",
                "http://sp.localhost:3000",
            ],
        )
        self.discord_feedback_webhook_url = self._get_optional_env("DISCORD_FEEDBACK_WEBHOOK_URL")
        self.discord_sales_webhook_url = self._get_optional_env("DISCORD_SALES_WEBHOOK_URL")
        self.default_processing_mode = os.getenv("DEFAULT_PROCESSING_MODE", "fast")
        self.fast_mode_max_clips = int(os.getenv("FAST_MODE_MAX_CLIPS", "4"))
        self.fast_mode_transcript_model = os.getenv(
            "FAST_MODE_TRANSCRIPT_MODEL", "nano"
        )

        # Transcription localization
        # "pt" is a sensible default for BR-focused UX; set to "auto"/"none" to disable hints.
        self.transcription_language_hint = os.getenv(
            "TRANSCRIPTION_LANGUAGE_HINT", "pt"
        ).strip()

        # External imports (Drive/Vimeo/Loom/Direct URL)
        self.import_allowed_hosts = self._get_csv_env(
            "IMPORT_ALLOWED_HOSTS",
            [
                "drive.google.com",
                "docs.google.com",
                "www.googleapis.com",
                "vimeo.com",
                "player.vimeo.com",
                "www.loom.com",
            ],
        )
        self.import_max_file_bytes = int(os.getenv("IMPORT_MAX_FILE_BYTES", str(1024**3)))
        self.import_max_redirects = int(os.getenv("IMPORT_MAX_REDIRECTS", "5"))
        self.import_connect_timeout_seconds = float(
            os.getenv("IMPORT_CONNECT_TIMEOUT_SECONDS", "10")
        )
        self.import_read_timeout_seconds = float(
            os.getenv("IMPORT_READ_TIMEOUT_SECONDS", "60")
        )
        # Optional: gate passing provider API tokens from clients in dev
        self.import_dev_token = self._get_optional_env("IMPORT_DEV_TOKEN")

        # Processing cache TTL + cleanup loop
        self.processing_cache_ttl_seconds = int(
            os.getenv("PROCESSING_CACHE_TTL_SECONDS", "604800")
        )  # 7 days
        self.processing_cache_cleanup_interval_seconds = int(
            os.getenv("PROCESSING_CACHE_CLEANUP_INTERVAL_SECONDS", "3600")
        )  # 1 hour
        self.processing_cache_cleanup_batch_size = int(
            os.getenv("PROCESSING_CACHE_CLEANUP_BATCH_SIZE", "2000")
        )

    @staticmethod
    def _get_optional_env(name: str):
        value = os.getenv(name)
        if value is None:
            return None

        normalized = value.strip()
        return normalized or None

    @staticmethod
    def _get_bool_env(name: str, default: bool) -> bool:
        value = os.getenv(name)
        if value is None:
            return default
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
        return default

    @staticmethod
    def _get_csv_env(name: str, default: list[str]) -> list[str]:
        value = os.getenv(name)
        if not value:
            return default
        return [item.strip() for item in value.split(",") if item.strip()]

    def _infer_default_llm(self) -> str:
        """
        Infer a usable default model based on whichever API key is present.
        Falls back to Google for backward compatibility.
        """
        if self.google_api_key:
            return "google-gla:gemini-3-flash-preview"
        if self.openai_api_key:
            return "openai:gpt-5.2"
        if self.anthropic_api_key:
            return "anthropic:claude-4-sonnet"
        return "google-gla:gemini-3-flash-preview"
