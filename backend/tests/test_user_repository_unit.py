"""
Unit tests for UserRepository.
Ensures YouTube cookies are saved and retrieved correctly.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, MagicMock
from src.repositories.user_repository import UserRepository
from src.models import User

@pytest.fixture
def mock_db_session():
    return AsyncMock(spec=AsyncSession)

@pytest.mark.asyncio
async def test_get_by_id_found(mock_db_session):
    repo = UserRepository(mock_db_session)
    
    mock_user = User(id="user-123", youtube_cookies="mock_cookies")
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user
    mock_db_session.execute.return_value = mock_result
    
    user = await repo.get_by_id("user-123")
    assert user is not None
    assert user.id == "user-123"
    assert user.youtube_cookies == "mock_cookies"

@pytest.mark.asyncio
async def test_get_by_id_not_found(mock_db_session):
    repo = UserRepository(mock_db_session)
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db_session.execute.return_value = mock_result
    
    user = await repo.get_by_id("non-existent")
    assert user is None

@pytest.mark.asyncio
async def test_get_youtube_cookies(mock_db_session):
    repo = UserRepository(mock_db_session)
    
    mock_user = User(id="user-123", youtube_cookies="netscape_cookie_data")
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user
    mock_db_session.execute.return_value = mock_result
    
    cookies = await repo.get_youtube_cookies("user-123")
    assert cookies == "netscape_cookie_data"

@pytest.mark.asyncio
async def test_update_youtube_cookies_success(mock_db_session):
    repo = UserRepository(mock_db_session)
    
    success = await repo.update_youtube_cookies("user-123", "new_cookies")
    
    assert success is True
    mock_db_session.execute.assert_called_once()
    mock_db_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_update_youtube_cookies_failure(mock_db_session):
    repo = UserRepository(mock_db_session)
    
    mock_db_session.execute.side_effect = Exception("DB Error")
    
    success = await repo.update_youtube_cookies("user-123", "new_cookies")
    
    assert success is False
    mock_db_session.execute.assert_called_once()
    mock_db_session.rollback.assert_called_once()
