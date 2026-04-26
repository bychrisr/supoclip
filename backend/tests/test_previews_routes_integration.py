"""
Integration tests for previews API routes.
Tests the endpoints for generating short MP4 animation previews.
"""

import pytest
from httpx import AsyncClient, ASGITransport
import os

from src.main_refactored import app

@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_get_preview_invalid_template(async_client: AsyncClient):
    # Should fallback to 'default' if invalid template is passed, but still return 200
    response = await async_client.get("/previews/non_existent_template")
    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"

@pytest.mark.asyncio
async def test_get_preview_valid_template(async_client: AsyncClient):
    response = await async_client.get("/previews/tiktok")
    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"
    # Ensure it's not a zero-byte file
    assert int(response.headers.get("content-length", 0)) > 0
