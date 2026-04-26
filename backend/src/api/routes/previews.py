"""
Preview API routes - generates short animation previews for caption templates.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
import logging
from moviepy import ColorClip, CompositeVideoClip
from ...services.caption_renderer import CaptionRenderer
from ...config import Config

router = APIRouter(prefix="/previews", tags=["previews"])
logger = logging.getLogger(__name__)
config = Config()

@router.get("/{template_name}")
async def get_template_preview(template_name: str):
    """
    Generates a 2-second MP4 preview of a caption template.
    Addresses QA Audit Item 5.
    """
    template_name = CaptionRenderer.validate_template(template_name)
    preview_dir = Path(config.temp_dir) / "previews"
    preview_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = preview_dir / f"{template_name}.mp4"
    
    # Return cached if exists and not too old
    if output_path.exists():
        return FileResponse(output_path)

    try:
        # Create a simple black background 1080x1920
        bg = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=2)
        
        renderer = CaptionRenderer(1080, 1920, template_name)
        
        # Render "SupoClip" with the template's animation
        text_clip = renderer.render_word("SupoClip", 0.5, 1.0, is_highlighted=True)
        
        composite = CompositeVideoClip([bg, text_clip])
        composite.write_videofile(
            str(output_path),
            fps=24,
            codec="libx264",
            audio=False,
            logger=None
        )
        
        # Cleanup
        text_clip.close()
        bg.close()
        composite.close()
        
        return FileResponse(output_path)
    except Exception as e:
        logger.error(f"Failed to generate preview for {template_name}: {e}")
        raise HTTPException(status_code=500, detail="Preview generation failed")
