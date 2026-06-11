"""Business readiness tools for TurfGrid AI agents."""
from app.data.seed_data import BUSINESSES, MATCHES, VENUES, CROWD_DATA


def predict_match_day_demand(venue_id: str, match_id: str = "") -> dict:
    """Predict customer demand for businesses near a venue on match day.

    Args:
        venue_id: The venue identifier.
        match_id: Optional specific match ID for targeted predictions.

    Returns:
        Demand predictions with staffing and inventory recommendations.
    """
    businesses = [b for b in BUSINESSES if b["venue_id"] == venue_id]
    crowd = None
    if match_id:
        crowd = next((c for c in CROWD_DATA if c["match_id"] == match_id), None)

    venue = next((v for v in VENUES if v["_id"] == venue_id), None)
    if not venue:
        return {"error": f"Venue '{venue_id}' not found."}

    predictions = []
    for biz in businesses:
        normal = biz.get("normal_daily_covers", 0)
        capacity = biz.get("capacity", 0)

        if crowd:
            util = crowd.get("utilization_pct", 80)
            multiplier = 1.5 + (util / 100) * 1.5  # 1.5x to 3x based on crowd
        else:
            multiplier = 2.0

        predicted_demand = int(normal * multiplier) if normal else None
        overflow = max(0, (predicted_demand or 0) - capacity)

        extra_staff = max(0, int((multiplier - 1) * 3))  # Rough staffing calc

        predictions.append({
            "business": biz["name"],
            "type": biz["type"],
            "normal_daily_volume": normal,
            "predicted_match_day_volume": predicted_demand,
            "capacity": capacity,
            "overflow_risk": overflow > 0,
            "overflow_customers": overflow,
            "demand_multiplier": round(multiplier, 1),
            "staffing_recommendation": f"Add {extra_staff} additional staff",
            "inventory_recommendation": _get_inventory_tips(biz["type"], multiplier),
            "preparation_checklist": _get_prep_checklist(biz["type"], multiplier)
        })

    return {
        "venue": venue["name"],
        "predictions": predictions,
        "general_advice": f"Expect {int(multiplier * 100 - 100)}% increase in foot traffic on match day."
    }


def get_business_checklist(business_type: str, congestion_level: str = "high") -> dict:
    """Get a preparation checklist for a business type on match day.

    Args:
        business_type: Type of business ('restaurant', 'hotel', 'cafe', 'retail').
        congestion_level: Expected congestion ('moderate', 'high', 'very_high', 'extreme').

    Returns:
        A detailed preparation checklist.
    """
    checklists = {
        "restaurant": {
            "24_hours_before": [
                "Confirm all staff for extended shifts",
                "Pre-prep ingredients for high-demand items",
                "Stock up on beverages (especially beer/soft drinks)",
                "Test POS systems and backup payment methods",
                "Brief staff on expected crowd volume"
            ],
            "4_hours_before": [
                "Set up overflow seating if available",
                "Prepare takeaway packaging for walk-in orders",
                "Post match-day specials on social media",
                "Ensure kitchen is fully stocked and prepped",
                "Coordinate with delivery services"
            ],
            "during_match": [
                "Deploy extra front-of-house staff",
                "Monitor queue times and adjust service speed",
                "Offer match-themed specials",
                "Keep restrooms clean with frequent checks",
                "Have security aware of crowd management"
            ]
        },
        "hotel": {
            "24_hours_before": [
                "Confirm all reservations and early check-in requests",
                "Brief concierge on match schedule and transport options",
                "Prepare match-day information packs for guests",
                "Stock lobby with event brochures and maps",
                "Ensure late check-out options are communicated"
            ],
            "4_hours_before": [
                "Set up lobby TV for match viewing if applicable",
                "Prepare grab-and-go breakfast packs for early departures",
                "Coordinate with local transport providers",
                "Ensure extra towels and amenities in rooms"
            ],
            "during_match": [
                "Have concierge available for transport queries",
                "Monitor noise levels for non-event guests",
                "Offer match viewing in hotel bar/lounge",
                "Prepare for late arrivals post-match"
            ]
        },
        "cafe": {
            "24_hours_before": [
                "Order extra coffee beans, milk, and pastries",
                "Prepare batch cold brew for hot weather",
                "Staff up for 2x normal volume",
                "Update menu boards with match-day specials"
            ],
            "4_hours_before": [
                "Pre-make popular items in batches",
                "Set up a quick-service line for takeaway",
                "Post on social media about match-day hours"
            ],
            "during_match": [
                "Focus on speed of service",
                "Monitor stock levels hourly",
                "Keep seating area clean for turnover"
            ]
        }
    }

    checklist = checklists.get(business_type, checklists["restaurant"])

    if congestion_level in ["very_high", "extreme"]:
        checklist["24_hours_before"].append("Consider hiring temporary security staff")
        checklist["24_hours_before"].append("Plan for 3x normal waste disposal")

    return {
        "business_type": business_type,
        "congestion_level": congestion_level,
        "checklist": checklist
    }


def _get_inventory_tips(biz_type: str, multiplier: float) -> list:
    """Get inventory tips based on business type and expected demand."""
    pct = int((multiplier - 1) * 100)
    if biz_type == "restaurant":
        return [
            f"Increase food stock by {pct}%",
            f"Increase beverage stock by {int(pct * 1.5)}% (drinks spike higher)",
            "Pre-prepare sauces, sides, and desserts",
            "Stock disposable containers for takeaway overflow"
        ]
    elif biz_type == "cafe":
        return [
            f"Increase coffee bean stock by {pct}%",
            f"Order {int(pct * 0.5)}% more pastries/sandwiches",
            "Prepare extra cold brew batches"
        ]
    elif biz_type == "hotel":
        return [
            "Ensure all rooms are prepared 2 hours early",
            "Stock extra toiletries and towels",
            "Prepare early check-in capability"
        ]
    return [f"Increase stock by {pct}%"]


def _get_prep_checklist(biz_type: str, multiplier: float) -> list:
    """Quick prep checklist based on demand multiplier."""
    items = ["Confirm all staff schedules", "Test payment systems"]
    if multiplier > 2.0:
        items.append("Consider temporary staff or overtime")
        items.append("Set up overflow area if possible")
    if multiplier > 2.5:
        items.append("Coordinate with neighboring businesses for crowd management")
        items.append("Brief local security/police on expected volumes")
    return items
