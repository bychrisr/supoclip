"""
User API routes - handles user profile and settings.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import logging

from ...database import get_db
from ...repositories.user_repository import UserRepository
from ...auth_headers import get_signed_user_id
from ...config import Config

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)
config = Config()

@router.patch("/me/youtube-cookies")
async def update_user_keys(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Saves API keys or cookies for the current user.
    Uses dynamic provider detection based on headers or body.
    """
    user_id = get_signed_user_id(request, config=config)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        content_type = request.headers.get("Content-Type", "")
        body = await request.body()
        content = body.decode("utf-8")
        
        # Determine what we are updating
        provider = request.headers.get("X-Provider", "youtube")
        
        logger.info(f"🚀 [API] Updating {provider} key for user {user_id}")
        
        repo = UserRepository(db)
        if provider == "youtube":
            success = await repo.update_youtube_cookies(user_id, content)
        else:
            success = await repo.update_api_key(user_id, provider, content)
        
        if not success:
            raise HTTPException(status_code=500, detail=f"Failed to update {provider} settings")
            
        return {"message": f"{provider.capitalize()} settings updated successfully"}
    except Exception as e:
        logger.error(f"❌ [API] Error updating user settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me/integrations")
async def get_user_integrations(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Returns info about user's active integrations and keys."""
    user_id = get_signed_user_id(request, config=config)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # AUDITORIA BRUTA (Aria's Debug)
    logger.info(f"🔍 [AUDIT] User ID: {user.id}")
    logger.info(f"🔍 [AUDIT] YouTube Cookies Value: {user.youtube_cookies}")
    logger.info(f"🔍 [AUDIT] OpenRouter Key Value: {user.openrouter_api_key}")
    
    return {
        "youtube_cookies_active": bool(user.youtube_cookies),
        "youtube_cookies": user.youtube_cookies,
        "assembly_ai_active": bool(user.assembly_ai_api_key),
        "google_active": bool(user.google_api_key),
        "openrouter_active": bool(user.openrouter_api_key),
    }
