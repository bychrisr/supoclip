"""
Unit tests for CaptionRenderer service.
Ensures animations and resource management are working correctly.
"""

import pytest
from pathlib import Path
from src.services.caption_renderer import CaptionRenderer
from moviepy import VideoClip, TextClip

def test_caption_renderer_initialization():
    """Test if renderer initializes with correct font scaling and template validation."""
    # Test valid template
    renderer = CaptionRenderer(video_width=1280, video_height=720, template_name="mrbeast")
    assert renderer.template_name == "mrbeast"
    assert renderer.font_size > 0
    assert renderer.y_position > 0

    # Test invalid template (should fallback to default)
    renderer_invalid = CaptionRenderer(video_width=1280, video_height=720, template_name="non_existent")
    assert renderer_invalid.template_name == "default"

def test_render_word_basic():
    """Test rendering a single word returns a valid TextClip."""
    renderer = CaptionRenderer(video_width=1280, video_height=720, template_name="default")
    
    # Render a simple word
    clip = renderer.render_word(text="Hello", start_t=1.0, duration=0.5, is_highlighted=False)
    
    assert isinstance(clip, TextClip)
    assert clip.start == 1.0
    assert clip.duration == 0.5
    
    # Cleanup
    clip.close()

def test_render_word_pop_animation():
    """Test rendering with pop animation (MoviePy v2 compatibility)."""
    renderer = CaptionRenderer(video_width=1280, video_height=720, template_name="mrbeast")
    
    # mrbeast uses 'pop' animation
    clip = renderer.render_word(text="POP", start_t=0, duration=1.0)
    
    assert clip.duration == 1.0
    # Check if position is set (center, y)
    assert clip.pos(0) is not None
    
    clip.close()

def test_render_words_batch():
    """Test batch rendering of multiple words."""
    renderer = CaptionRenderer(video_width=1280, video_height=720, template_name="default")
    
    words_data = [
        {"text": "First", "start": 0.0, "end": 0.5, "highlight": False},
        {"text": "Second", "start": 0.6, "end": 1.0, "highlight": True}
    ]
    
    clips = renderer.render_words_batch(words_data)
    
    assert len(clips) == 2
    assert clips[0].text == "First"
    assert clips[1].text == "Second"
    
    # Cleanup
    for c in clips:
        c.close()
