"""
Integration tests for users API routes.
Tests the endpoints for setting and getting YouTube cookies.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
import uuid

from src.main_refactored import app
from src.database import get_db

# Override the database dependency
async def override_get_db():
    yield AsyncMock()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture
def mock_user_repo(user_id):
    with patch("src.api.routes.users.UserRepository") as mock_repo, \
         patch("src.api.routes.users.get_signed_user_id", new_callable=AsyncMock) as mock_auth:
        
        # Mock auth to always return our test user from fixture
        mock_auth.return_value = user_id
        
        instance = mock_repo.return_value
        instance.update_youtube_cookies = AsyncMock(return_value=True)
        
        # Mocking the returned user for the GET endpoint
        mock_user = AsyncMock()
        mock_user.youtube_cookies = "very_long_cookie_string_that_should_be_truncated_in_preview_endpoint"
        instance.get_by_id = AsyncMock(return_value=mock_user)
        
        yield instance

@pytest.mark.asyncio
async def test_update_youtube_cookies_unauthorized(async_client: AsyncClient):
    response = await async_client.patch(
        "/users/me/youtube-cookies",
        content="mock_cookies_content"
    )
    # 401 because no user_id header is present
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_update_youtube_cookies_success(async_client: AsyncClient, mock_user_repo, auth_headers: dict, user_id: str):
    response = await async_client.patch(
        "/users/me/youtube-cookies",
        content="mock_cookies_content_123",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    assert response.json() == {"message": "YouTube cookies updated successfully"}
    mock_user_repo.update_youtube_cookies.assert_called_once_with(user_id, "mock_cookies_content_123")

@pytest.mark.asyncio
async def test_get_user_integrations(async_client: AsyncClient, mock_user_repo, auth_headers: dict, user_id: str):
    response = await async_client.get(
        "/users/me/integrations",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["youtube_cookies_active"] is True
    assert data["youtube_cookies_preview"].startswith("very_long_cookie_string")
    assert "..." in data["youtube_cookies_preview"]
    mock_user_repo.get_by_id.assert_called_once_with(user_id)
