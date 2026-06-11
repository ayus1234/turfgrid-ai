"""Crowd intelligence tools for EventSphere AI agents."""
import os
import requests
from app.data.seed_data import CROWD_DATA, VENUES, MATCHES


def get_crowd_forecast(venue_id: str = "", match_id: str = "") -> dict:
    """Get crowd density forecast for a venue or specific match.

    Args:
        venue_id: The venue identifier.
        match_id: Optional specific match ID.

    Returns:
        Crowd forecast with congestion levels, peak hours, and recommendations.
    """
    results = []
    for cd in CROWD_DATA:
        if venue_id and cd["venue_id"] != venue_id:
            continue
        if match_id and cd.get("match_id") != match_id:
            continue

        venue = next((v for v in VENUES if v["_id"] == cd["venue_id"]), {})
        match = next((m for m in MATCHES if m["_id"] == cd.get("match_id", "")), {})

        results.append({
            "venue": venue.get("name", cd["venue_id"]),
            "city": venue.get("city", ""),
            "match": match.get("round", "") + (": " + " vs ".join(match.get("teams", [])) if match.get("teams") else ""),
            "date": match.get("date", ""),
            "predicted_attendance": cd["predicted_attendance"],
            "capacity": cd["venue_capacity"],
            "utilization": f"{cd['utilization_pct']}%",
            "congestion_level": cd["congestion_level"],
            "peak_hours": cd["peak_hours"],
            "recommended_arrival": f"{cd['recommended_arrival_hours_before']} hours before kickoff",
            "estimated_queue": f"{cd['estimated_queue_minutes']} minutes",
            "parking": cd["parking_availability"],
            "public_transport_load": cd["public_transport_load"],
            "alternative_routes": cd["alternative_routes"]
        })

    if not results:
        return _generate_estimate(venue_id, match_id)

    return {"forecasts": results, "count": len(results)}


def get_live_weather(venue_id: str) -> dict:
    """Get real-time weather data for a specific venue using OpenWeatherMap API.

    Args:
        venue_id: The venue identifier.

    Returns:
        Current weather conditions, temperature, and description.
    """
    venue = next((v for v in VENUES if v["_id"] == venue_id), None)
    if not venue:
        return {"error": f"Venue '{venue_id}' not found."}

    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return {
            "venue": venue["name"],
            "city": venue["city"],
            "note": "WEATHER_API_KEY not configured. Using simulated clear weather.",
            "temperature": "22°C",
            "condition": "Clear sky",
            "impact_on_crowd": "minimal"
        }

    lat, lng = venue.get("lat"), venue.get("lng")
    if not lat or not lng:
        return {"error": "Coordinates not available for this venue."}

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        condition = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        
        # Determine crowd impact
        impact = "minimal"
        if "rain" in condition or "storm" in condition or "snow" in condition:
            impact = "high (umbrellas/coats will slow down security checks, queues may take 20% longer)"
        elif temp > 32:
            impact = "moderate (high heat may cause medical incidents in queues, fans arrive closer to kickoff)"

        return {
            "venue": venue["name"],
            "city": venue["city"],
            "temperature": f"{temp}°C",
            "condition": condition,
            "humidity": f"{data['main']['humidity']}%",
            "wind_speed": f"{data['wind']['speed']} m/s",
            "impact_on_crowd": impact
        }
    except Exception as e:
        return {"error": f"Failed to fetch live weather: {str(e)}"}


def predict_congestion(venue_id: str, date: str, event_type: str = "group_stage") -> dict:
    """Predict congestion levels for a venue on a specific date.

    Args:
        venue_id: The venue identifier.
        date: The date (YYYY-MM-DD).
        event_type: Type of match ('group_stage', 'knockout', 'semi_final', 'final').

    Returns:
        Congestion prediction with mitigation recommendations.
    """
    venue = next((v for v in VENUES if v["_id"] == venue_id), None)
    if not venue:
        return {"error": f"Venue '{venue_id}' not found."}

    capacity = venue["capacity"]

    # Estimate based on event type
    fill_rates = {
        "group_stage": 0.75,
        "knockout": 0.90,
        "quarter_final": 0.95,
        "semi_final": 0.98,
        "final": 1.0
    }
    fill = fill_rates.get(event_type, 0.80)
    predicted = int(capacity * fill)

    if fill >= 0.95:
        congestion = "extreme"
        arrival_hours = 4
        queue_min = 45
    elif fill >= 0.85:
        congestion = "very_high"
        arrival_hours = 3
        queue_min = 30
    elif fill >= 0.70:
        congestion = "high"
        arrival_hours = 2
        queue_min = 20
    else:
        congestion = "moderate"
        arrival_hours = 1
        queue_min = 10

    return {
        "venue": venue["name"],
        "city": venue["city"],
        "date": date,
        "event_type": event_type,
        "predicted_attendance": predicted,
        "capacity": capacity,
        "fill_rate": f"{int(fill * 100)}%",
        "congestion_level": congestion,
        "recommended_arrival": f"{arrival_hours} hours before",
        "estimated_queue": f"{queue_min} minutes",
        "transport_options": venue.get("transport", []),
        "mitigation_tips": _get_mitigation_tips(congestion, venue)
    }


def suggest_optimal_route(venue_id: str, origin_area: str = "city_center") -> dict:
    """Suggest optimal travel routes to a venue.

    Args:
        venue_id: The destination venue.
        origin_area: General origin area ('city_center', 'airport', 'hotel_district').

    Returns:
        Route suggestions with estimated times and crowd avoidance tips.
    """
    venue = next((v for v in VENUES if v["_id"] == venue_id), None)
    if not venue:
        return {"error": f"Venue '{venue_id}' not found."}

    return {
        "venue": venue["name"],
        "city": venue["city"],
        "primary_transport": venue.get("transport", []),
        "tips": [
            f"Use {venue.get('transport', ['public transport'])[0]} for fastest access",
            "Arrive early to avoid peak congestion",
            "Download offline maps — mobile signal may be weak near venue",
            "Keep tickets on your phone with backup screenshots",
        ],
        "avoid": [
            "Private vehicles on match day — parking is extremely limited",
            "Last-minute arrival — queues build 1-2 hours before kickoff",
        ],
        "nearby_attractions": venue.get("nearby_attractions", [])
    }


def _generate_estimate(venue_id: str, match_id: str) -> dict:
    """Generate a rough estimate when no historical data exists."""
    venue = next((v for v in VENUES if v["_id"] == venue_id), None)
    if not venue:
        return {"message": "No forecast data available for this venue/match combination."}

    return {
        "forecasts": [{
            "venue": venue["name"],
            "city": venue["city"],
            "note": "Estimated based on venue capacity — no historical data",
            "predicted_attendance": int(venue["capacity"] * 0.8),
            "capacity": venue["capacity"],
            "utilization": "80% (estimated)",
            "congestion_level": "high",
            "recommended_arrival": "2 hours before",
            "estimated_queue": "20 minutes (estimated)"
        }],
        "count": 1
    }


def _get_mitigation_tips(congestion: str, venue: dict) -> list:
    """Get congestion mitigation tips."""
    tips = [
        "Use public transport — driving will be extremely slow",
        f"Primary transport: {', '.join(venue.get('transport', ['Check local options']))}",
    ]
    if congestion in ["extreme", "very_high"]:
        tips.extend([
            "Consider arriving 3-4 hours early and exploring nearby attractions",
            f"Nearby: {', '.join(venue.get('nearby_attractions', [])[:3])}",
            "Bring water and snacks — queues may be long",
            "Have backup routes planned in case of closures",
            "Follow official event social media for real-time updates",
        ])
    return tips
