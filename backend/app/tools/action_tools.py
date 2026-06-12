"""
State-Altering Action Tools for TurfGrid AI Agents.

These tools allow agents to WRITE to MongoDB, changing system state.
This is the critical upgrade from 'recommending' to 'executing'.
"""
import uuid
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


# ─── Fan Agent Tool: Save Itinerary ──────────────────────────────────────────

async def save_itinerary(
    user_name: str,
    event: str,
    origin: str,
    destination_city: str,
    matches: str,
    hotel: str = "",
    transport_route: str = "",
    budget: str = "moderate",
    notes: str = ""
) -> dict:
    """Save a confirmed travel itinerary to MongoDB. Call this when a fan approves a travel plan.

    Args:
        user_name: The fan's name.
        event: The event name (e.g., 'FIFA World Cup 2026').
        origin: Where the fan is traveling from.
        destination_city: Primary destination city.
        matches: Comma-separated list of matches the fan wants to attend.
        hotel: Recommended hotel or accommodation.
        transport_route: Recommended transport route to the venue.
        budget: Budget level ('budget', 'moderate', 'luxury').
        notes: Any additional notes or special requirements.

    Returns:
        Confirmation with the saved itinerary ID and details.
    """
    db = _get_db()
    itinerary_id = f"ITN-{uuid.uuid4().hex[:8].upper()}"

    document = {
        "_id": itinerary_id,
        "user_name": user_name,
        "event": event,
        "origin": origin,
        "destination_city": destination_city,
        "matches": [m.strip() for m in matches.split(",")],
        "hotel": hotel,
        "transport_route": transport_route,
        "budget": budget,
        "notes": notes,
        "status": "confirmed",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        await db["user_itineraries"].insert_one(document)
        return {
            "status": "success",
            "message": f"✅ Itinerary {itinerary_id} saved to MongoDB successfully!",
            "itinerary_id": itinerary_id,
            "details": {
                "fan": user_name,
                "event": event,
                "from": origin,
                "to": destination_city,
                "matches": document["matches"],
                "hotel": hotel,
                "transport": transport_route,
                "budget": budget,
                "status": "confirmed"
            }
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to save itinerary: {str(e)}"}


# ─── Business Agent Tool: Create Staffing Plan ──────────────────────────────

async def create_staffing_plan(
    business_name: str,
    business_type: str,
    venue_name: str,
    match_description: str,
    match_date: str,
    normal_staff: int,
    recommended_staff: int,
    peak_hours: str = "2 hours before to 2 hours after match",
    inventory_notes: str = "",
    special_preparations: str = ""
) -> dict:
    """Create and save a staffing plan for a local business on match day. Call this when a business owner approves a preparation plan.

    Args:
        business_name: Name of the business (e.g., 'The Stadium Grill').
        business_type: Type of business ('restaurant', 'hotel', 'cafe', 'retail').
        venue_name: The nearby venue name.
        match_description: Description of the match (e.g., 'FIFA Final - Argentina vs France').
        match_date: Date of the match (YYYY-MM-DD).
        normal_staff: Normal number of staff on a regular day.
        recommended_staff: Recommended staff count for match day.
        peak_hours: Expected peak hours description.
        inventory_notes: Inventory preparation recommendations.
        special_preparations: Any special preparations needed.

    Returns:
        Confirmation with the saved staffing plan ID and details.
    """
    db = _get_db()
    plan_id = f"STP-{uuid.uuid4().hex[:8].upper()}"

    document = {
        "_id": plan_id,
        "business_name": business_name,
        "business_type": business_type,
        "venue_name": venue_name,
        "match_description": match_description,
        "match_date": match_date,
        "normal_staff": normal_staff,
        "recommended_staff": recommended_staff,
        "additional_staff_needed": max(0, recommended_staff - normal_staff),
        "peak_hours": peak_hours,
        "inventory_notes": inventory_notes,
        "special_preparations": special_preparations,
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        await db["staffing_plans"].insert_one(document)
        return {
            "status": "success",
            "message": f"✅ Staffing Plan {plan_id} saved to MongoDB successfully!",
            "plan_id": plan_id,
            "details": {
                "business": business_name,
                "type": business_type,
                "venue": venue_name,
                "match": match_description,
                "date": match_date,
                "staff_increase": f"{normal_staff} → {recommended_staff} (+{max(0, recommended_staff - normal_staff)})",
                "peak_hours": peak_hours,
                "status": "active"
            }
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to save staffing plan: {str(e)}"}


# ─── Operations Agent Tool: Issue Operational Alert ──────────────────────────

async def issue_operational_alert(
    venue_name: str,
    alert_type: str,
    severity: str,
    message: str,
    recommended_actions: str = ""
) -> dict:
    """Issue an operational alert for a venue. Call this to flag crowd, security, medical, or facility issues.

    Args:
        venue_name: The venue where the alert applies (e.g., 'MetLife Stadium').
        alert_type: Type of alert ('crowd', 'security', 'medical', 'weather', 'facility', 'transport').
        severity: Severity level ('low', 'medium', 'high', 'critical').
        message: Description of the alert (e.g., 'Expected congestion at Gate C during halftime').
        recommended_actions: Comma-separated recommended actions to mitigate the issue.

    Returns:
        Confirmation with the alert ID and details.
    """
    db = _get_db()
    alert_id = f"ALT-{uuid.uuid4().hex[:8].upper()}"

    document = {
        "_id": alert_id,
        "venue_name": venue_name,
        "alert_type": alert_type,
        "severity": severity,
        "message": message,
        "recommended_actions": [a.strip() for a in recommended_actions.split(",")] if recommended_actions else [],
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        await db["operational_alerts"].insert_one(document)
        return {
            "status": "success",
            "message": f"🚨 Alert {alert_id} issued and saved to MongoDB!",
            "alert_id": alert_id,
            "details": {
                "venue": venue_name,
                "type": alert_type,
                "severity": severity,
                "message": message,
                "actions": document["recommended_actions"],
                "status": "active"
            }
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to issue alert: {str(e)}"}
