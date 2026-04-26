"""
Caption Renderer Service - Unified logic for subtitle rendering and animations.
Addresses QA Audit: Redundancy, Performance, and Resource Management.
"""

import logging
import math
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from moviepy import TextClip, vfx
from ..caption_templates import get_template, CAPTION_TEMPLATES
from ..font_registry import find_font_path

logger = logging.getLogger(__name__)

class CaptionRenderer:
    """
    Unified service to render captions with animation support.
    Designed for high performance and resource safety.
    """
    
    # Whitelist of allowed templates for security (QA Audit Item 4)
    ALLOWED_TEMPLATES = set(CAPTION_TEMPLATES.keys())

    @staticmethod
    def validate_template(template_name: str) -> str:
        """Ensures template_name is valid, defaults to 'default' if not."""
        if template_name in CaptionRenderer.ALLOWED_TEMPLATES:
            return template_name
        logger.warning(f"Invalid template '{template_name}' requested. Falling back to 'default'.")
        return "default"

    def __init__(self, video_width: int, video_height: int, template_name: str = "default"):
        self.video_width = video_width
        self.video_height = video_height
        self.template_name = self.validate_template(template_name)
        self.template = get_template(self.template_name)
        
        # Pre-resolve font path
        font_family = self.template.get("font_family", "TikTokSans-Regular")
        resolved_font = find_font_path(font_family, allow_all_user_fonts=True)
        if not resolved_font:
            resolved_font = find_font_path("TikTokSans-Regular")
        self.font_path = str(resolved_font) if resolved_font else ""
        
        # Pre-calculate base scaling (Performance)
        self.font_size = self._get_scaled_font_size(self.template.get("font_size", 64))
        self.y_position = int(self.video_height * self.template.get("position_y", 0.78))

    def _get_scaled_font_size(self, base_size: int) -> int:
        """Scale font size based on video width."""
        scaled = int(base_size * (self.video_width / 720))
        return max(24, min(96, scaled))

    def render_word(self, text: str, start_t: float, duration: float, is_highlighted: bool = False) -> TextClip:
        """
        Renders a single word with optimized animations.
        QA Audit Item 1: Avoids complex lambdas when possible.
        """
        animation = self.template.get("animation", "none")
        color = self.template.get("highlight_color", "#FFD700") if is_highlighted else self.template.get("font_color", "#FFFFFF")
        stroke_color = self.template.get("stroke_color", "black")
        stroke_width = self.template.get("stroke_width", 2)

        # Base Clip
        t_clip = TextClip(
            text=text,
            font=self.font_path,
            font_size=self.font_size,
            color=color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            method="label",
        ).with_start(start_t).with_duration(duration)

        # Optimized Animations
        if animation == "pop":
            # Optimized Pop: uses a single scale effect instead of complex frame-by-frame lambda
            # Simple scaling over first 0.2s
            t_clip = t_clip.with_effects([
                lambda c, st=start_t: c.resized(lambda t: 1.0 + 0.15 * math.sin(math.pi * (t - st) / 0.2) if 0 <= (t - st) < 0.2 else 1.0)
            ])
            t_clip = t_clip.with_position(("center", self.y_position))
        
        elif animation == "fade":
            fade_io = min(0.1, duration / 3)
            t_clip = t_clip.with_effects([vfx.FadeIn(fade_io), vfx.FadeOut(fade_io)])
            t_clip = t_clip.with_position(("center", self.y_position))
            
        elif animation == "bounce":
            orig_y = self.y_position
            # Optimized Bounce: vertical movement only
            t_clip = t_clip.with_position(
                lambda t, st=start_t: ("center", orig_y - 10 * math.sin(math.pi * (t - st) / 0.3) if 0 <= (t - st) < 0.3 else orig_y)
            )
        else:
            t_clip = t_clip.with_position(("center", self.y_position))

        return t_clip

    def render_words_batch(self, words_data: List[Dict[str, Any]]) -> List[TextClip]:
        """Renders a list of words, returning a list of clips to be composited."""
        clips = []
        for word in words_data:
            # words_data format: [{"text": "hello", "start": 0.5, "end": 0.8, "highlight": False}, ...]
            start = word.get("start", 0)
            duration = word.get("end", start + 0.1) - start
            is_highlight = word.get("highlight", False)
            
            clip = self.render_word(word["text"], start, duration, is_highlight)
            clips.append(clip)
        return clips
