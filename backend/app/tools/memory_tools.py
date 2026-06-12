"""
Persistent User Memory Tools for TurfGrid AI Agents.

These tools allow the Orchestrator to remember user preferences across sessions
by storing them in MongoDB. This enables personalized recommendations without
the user having to repeat themselves.
"""
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

_client = None
_db = None


def _get_db():
    """Get or create the async MongoDB connection."""
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(settings.MONGODB_URI)
        _db = _client[settings.MONGODB_DB]
    return _db


async def save_user_preference(
    user_id: str,
    preference_type: str,
    preference_value: str
) -> dict:
    """Save a user's personal preference to MongoDB for future personalization.
    Call this whenever the user mentions personal details like dietary needs, 
    accessibility requirements, budget, favorite teams, or travel preferences.

    Args:
        user_id: The user's session identifier.
        preference_type: Category of preference ('diet', 'accessibility', 'budget', 'favorite_team', 'travel_style', 'language', 'group_size').
        preference_value: The preference value (e.g., 'vegetarian', 'wheelchair', 'luxury', 'India').

    Returns:
        Confirmation that the preference was saved.
    """
    db = _get_db()

    try:
        await db["user_profiles"].update_one(
            {"_id": user_id},
            {
                "$set": {
                    f"preferences.{preference_type}": preference_value,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                },
                "$setOnInsert": {
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
            },
            upsert=True,
        )
        return {
            "status": "success",
            "message": f"🧠 Remembered your {preference_type}: {preference_value}",
            "preference": {preference_type: preference_value},
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to save preference: {str(e)}"}


async def get_user_profile(user_id: str) -> dict:
    """Retrieve a user's saved preferences from MongoDB.
    Call this at the start of a conversation to personalize responses.

    Args:
        user_id: The user's session identifier.

    Returns:
        The user's stored preferences, or an empty profile if none exist.
    """
    db = _get_db()

    try:
        profile = await db["user_profiles"].find_one({"_id": user_id})
        if profile:
            return {
                "status": "found",
                "user_id": user_id,
                "preferences": profile.get("preferences", {}),
                "message": "User profile loaded. Use these preferences to personalize all recommendations.",
            }
        return {
            "status": "new_user",
            "user_id": user_id,
            "preferences": {},
            "message": "No saved preferences found. This is a new user.",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to load profile: {str(e)}"}
