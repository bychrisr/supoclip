"""
User repository - handles user profile and integration settings.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Optional
import logging

from ..models import User

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def update_youtube_cookies(self, user_id: str, cookies: str) -> bool:
        """Update user's YouTube cookies content."""
        return await self._update_field(user_id, "youtube_cookies", cookies)

    async def update_api_key(self, user_id: str, provider: str, key: str) -> bool:
        """Update a specific API key for the user."""
        field_map = {
            "assembly": "assembly_ai_api_key",
            "google": "google_api_key",
            "openrouter": "openrouter_api_key"
        }
        field = field_map.get(provider.lower())
        if not field:
            return False
        return await self._update_field(user_id, field, key)

    async def _update_field(self, user_id: str, field: str, value: str) -> bool:
        """Generic field update helper."""
        try:
            await self.db.execute(
                update(User)
                .where(User.id == user_id)
                .values({field: value})
            )
            await self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating {field} for user {user_id}: {e}")
            await self.db.rollback()
            return False

    async def get_youtube_cookies(self, user_id: str) -> Optional[str]:
        """Get user's YouTube cookies content."""
        user = await self.get_by_id(user_id)
        return user.youtube_cookies if user else None
