"""
Unit tests for youtube_utils.py.
Ensures proxy rotation and cookie handling logic is correct.
"""

import pytest
from src.youtube_utils import YouTubeDownloader

def test_optimal_download_options_without_extras():
    downloader = YouTubeDownloader()
    opts = downloader.get_optimal_download_options(video_id="12345678901")
    
    assert "cookiefile" not in opts
    assert "proxy" not in opts
    assert opts["format_sort"] == ["res", "fps"] # Default to best

def test_optimal_download_options_with_cookies():
    downloader = YouTubeDownloader()
    opts = downloader.get_optimal_download_options(video_id="12345678901", cookie_file_path="/tmp/fake_cookie.txt")
    
    assert opts["cookiefile"] == "/tmp/fake_cookie.txt"
    assert "proxy" not in opts

def test_optimal_download_options_with_proxy():
    downloader = YouTubeDownloader()
    opts = downloader.get_optimal_download_options(video_id="12345678901", proxy="http://proxy:8080")
    
    assert "cookiefile" not in opts
    assert opts["proxy"] == "http://proxy:8080"

def test_optimal_download_options_with_all_extras():
    downloader = YouTubeDownloader()
    opts = downloader.get_optimal_download_options(
        video_id="12345678901",
        cookie_file_path="/tmp/fake_cookie.txt",
        proxy="http://proxy:8080",
        video_quality="720p"
    )
    
    assert opts["cookiefile"] == "/tmp/fake_cookie.txt"
    assert opts["proxy"] == "http://proxy:8080"
    assert "res:720" in opts["format_sort"]
