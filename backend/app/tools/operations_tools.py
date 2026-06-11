"""Event operations tools for EventSphere AI agents."""
from datetime import datetime


def report_incident(venue_id: str, incident_type: str, description: str, severity: str = "medium") -> dict:
    """Report a safety or operational incident at a venue.

    Args:
        venue_id: The venue where the incident occurred.
        incident_type: Type ('medical', 'security', 'lost_person', 'facility', 'crowd').
        description: Description of the incident.
        severity: Severity level ('low', 'medium', 'high', 'critical').

    Returns:
        Incident report with recommended response actions.
    """
    from app.data.seed_data import VENUES
    venue = next((v for v in VENUES if v["_id"] == venue_id), None)

    responses = {
        "medical": {
            "immediate": ["Contact on-site medical team", "Clear area around patient", "If critical, call emergency services"],
            "team": "Medical Response Unit",
            "escalation": "critical" if severity in ["high", "critical"] else "standard"
        },
        "security": {
            "immediate": ["Alert security command center", "Deploy nearest security team", "Monitor CCTV in affected area"],
            "team": "Security Operations",
            "escalation": "high" if severity in ["high", "critical"] else "standard"
        },
        "lost_person": {
            "immediate": ["Broadcast description to all stewards", "Check designated meeting points", "Alert gate staff"],
            "team": "Guest Services + Security",
            "escalation": "standard"
        },
        "facility": {
            "immediate": ["Dispatch maintenance team", "Set up barriers if needed", "Redirect foot traffic"],
            "team": "Facilities Management",
            "escalation": "standard"
        },
        "crowd": {
            "immediate": ["Monitor crowd density sensors", "Open additional entry/exit gates", "Deploy crowd management stewards"],
            "team": "Crowd Control Unit",
            "escalation": "high" if severity in ["high", "critical"] else "standard"
        }
    }

    response = responses.get(incident_type, responses["facility"])

    return {
        "incident_id": f"INC-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "venue": venue["name"] if venue else venue_id,
        "type": incident_type,
        "severity": severity,
        "description": description,
        "timestamp": datetime.utcnow().isoformat(),
        "response": response,
        "status": "reported"
    }


def get_volunteer_schedule(venue_id: str, date: str) -> dict:
    """Get volunteer deployment schedule for a venue on a specific date.

    Args:
        venue_id: The venue identifier.
        date: The date (YYYY-MM-DD).

    Returns:
        Volunteer schedule with roles and shift times.
    """
    from app.data.seed_data import VENUES
    venue = next((v for v in VENUES if v["_id"] == venue_id), None)
    if not venue:
        return {"error": f"Venue '{venue_id}' not found."}

    capacity = venue["capacity"]
    vol_ratio = capacity // 500  # 1 volunteer per 500 attendees

    return {
        "venue": venue["name"],
        "date": date,
        "total_volunteers_needed": vol_ratio * 3,  # 3 shifts
        "shifts": [
            {"shift": "Morning Setup", "time": "06:00-12:00", "volunteers": vol_ratio, "roles": ["Gate stewards", "Wayfinding", "Accessibility support"]},
            {"shift": "Match Time", "time": "12:00-18:00", "volunteers": int(vol_ratio * 1.5), "roles": ["Crowd management", "First aid support", "Information desks", "Lost & found"]},
            {"shift": "Evening Closeout", "time": "18:00-23:00", "volunteers": vol_ratio, "roles": ["Exit management", "Cleanup coordination", "Transport guidance"]}
        ],
        "key_roles": {
            "gate_stewards": int(vol_ratio * 0.3),
            "wayfinding": int(vol_ratio * 0.2),
            "first_aid_support": int(vol_ratio * 0.1),
            "crowd_management": int(vol_ratio * 0.2),
            "accessibility": int(vol_ratio * 0.1),
            "information_desks": int(vol_ratio * 0.1)
        }
    }


def allocate_resources(venue_id: str, event_type: str = "group_stage") -> dict:
    """Recommend resource allocation for an event at a venue.

    Args:
        venue_id: The venue identifier.
        event_type: Type of match ('group_stage', 'knockout', 'semi_final', 'final').

    Returns:
        Resource allocation recommendations.
    """
    from app.data.seed_data import VENUES
    venue = next((v for v in VENUES if v["_id"] == venue_id), None)
    if not venue:
        return {"error": f"Venue '{venue_id}' not found."}

    capacity = venue["capacity"]
    multipliers = {"group_stage": 1.0, "knockout": 1.3, "semi_final": 1.5, "final": 2.0}
    mult = multipliers.get(event_type, 1.0)

    return {
        "venue": venue["name"],
        "event_type": event_type,
        "resources": {
            "security_personnel": int(capacity / 200 * mult),
            "medical_staff": int(capacity / 1000 * mult),
            "ambulances_on_site": max(2, int(capacity / 10000 * mult)),
            "water_stations": int(capacity / 2000 * mult),
            "portable_toilets": int(capacity / 500 * mult) if capacity > 50000 else int(capacity / 750),
            "information_kiosks": int(capacity / 5000 * mult),
            "first_aid_stations": max(3, int(capacity / 5000 * mult)),
            "crowd_barriers_meters": int(capacity / 50 * mult),
        },
        "special_requirements": _get_special_requirements(event_type, venue)
    }


def _get_special_requirements(event_type: str, venue: dict) -> list:
    """Get special requirements based on event type."""
    reqs = ["Standard safety briefing for all staff"]
    if event_type in ["semi_final", "final"]:
        reqs.extend([
            "VIP security detail for dignitaries",
            "Media management team",
            "Anti-drone surveillance",
            "Extended perimeter security zone",
            "Bomb disposal unit on standby"
        ])
    if event_type == "final":
        reqs.extend([
            "Trophy security escort",
            "Post-match celebration management plan",
            "Extended public transport hours coordination"
        ])
    return reqs
