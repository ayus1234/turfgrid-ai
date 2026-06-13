"""
booking_tools.py – Utility functions for ticket, hotel, and flight booking features.
Provides mock data when external APIs (Amadeus, Google Maps) are not configured.
"""

import random
from typing import List, Dict

from app.data.seed_data import MATCHES, VENUES

# ---------------------------------------------------------------------------
# Ticket booking URLs (official)
# ---------------------------------------------------------------------------
_TICKET_URLS = {
    "fifa_wc_2026": "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/tickets",
    "icc_wt20_2026": "https://tickets.womens.t20worldcup.com/selection/event/date?lang=en&productId=10228814154367",
}

def get_ticket_booking_url(match_id: str) -> Dict:
    """Return the official ticket booking URL for a given match.

    Args:
        match_id: The `_id` value of the match from `MATCHES`.

    Returns:
        dict with keys `match_id`, `event_id`, `venue_name`, `ticket_url`.
        If the match is not found, returns an ``error`` field.
    """
    match = next((m for m in MATCHES if m.get("_id") == match_id), None)
    if not match:
        return {"error": f"Match '{match_id}' not found"}
    event_id = match.get("event_id")
    ticket_url = _TICKET_URLS.get(event_id)
    if not ticket_url:
        return {"error": f"No ticket URL configured for event '{event_id}'"}
    venue = next((v for v in VENUES if v.get("_id") == match.get("venue_id")), {})
    return {"match_id": match_id, "event_id": event_id, "venue_name": venue.get("name", ""), "ticket_url": ticket_url}

# ---------------------------------------------------------------------------
# Hotel search (mock data with realistic hotel names)
# ---------------------------------------------------------------------------
_VENUE_HOTELS_DATA = {
    # ── FIFA – USA ──
    "metlife_stadium": [
        {"hotel_name": "Marriott Meadowlands", "price": "₹14,940", "rating": 4.5, "distance_km": 1.2, "booking_url": "https://www.booking.com/hotel/us/marriott-meadowlands.en-gb.html"},
        {"hotel_name": "Hilton East Rutherford", "price": "₹12,450", "rating": 4.2, "distance_km": 0.9, "booking_url": "https://www.agoda.com/hilton-east-rutherford/hotel/us.html"},
        {"hotel_name": "Holiday Inn Express", "price": "₹10,790", "rating": 4.0, "distance_km": 2.0, "booking_url": "https://www.expedia.com/Hotel-Search?destination=East%20Rutherford"},
    ],
    "sofi_stadium": [
        {"hotel_name": "SoFi Hotel & Suites", "price": "₹13,280", "rating": 4.0, "distance_km": 0.8, "booking_url": "https://www.booking.com/searchresults.html?ss=Inglewood"},
        {"hotel_name": "Hyatt Place LAX", "price": "₹14,525", "rating": 4.3, "distance_km": 3.5, "booking_url": "https://www.hyatt.com"},
        {"hotel_name": "Four Points by Sheraton LAX", "price": "₹11,620", "rating": 4.1, "distance_km": 4.0, "booking_url": "https://www.marriott.com"},
    ],
    "att_stadium": [
        {"hotel_name": "Hilton Arlington", "price": "₹12,035", "rating": 4.2, "distance_km": 1.5, "booking_url": "https://www.booking.com/searchresults.html?ss=Arlington+TX"},
        {"hotel_name": "Live! by Loews", "price": "₹18,260", "rating": 4.6, "distance_km": 0.3, "booking_url": "https://www.loewshotels.com"},
        {"hotel_name": "Courtyard by Marriott Arlington", "price": "₹10,790", "rating": 4.0, "distance_km": 2.0, "booking_url": "https://www.marriott.com"},
    ],
    "hard_rock_stadium": [
        {"hotel_name": "Courtyard Miami", "price": "₹14,110", "rating": 4.1, "distance_km": 3.0, "booking_url": "https://www.booking.com/searchresults.html?ss=Miami+Gardens"},
        {"hotel_name": "Fontainebleau Miami Beach", "price": "₹29,050", "rating": 4.7, "distance_km": 15.0, "booking_url": "https://www.fontainebleau.com"},
        {"hotel_name": "Hampton Inn Hallandale", "price": "₹11,620", "rating": 4.0, "distance_km": 8.0, "booking_url": "https://www.hilton.com"},
    ],
    "mercedes_benz_stadium": [
        {"hotel_name": "Omni Atlanta Hotel at CNN Center", "price": "₹15,770", "rating": 4.4, "distance_km": 0.5, "booking_url": "https://www.omnihotels.com"},
        {"hotel_name": "The Glenn Hotel", "price": "₹13,280", "rating": 4.3, "distance_km": 0.8, "booking_url": "https://www.booking.com/searchresults.html?ss=Atlanta+Downtown"},
        {"hotel_name": "Holiday Inn Express Downtown", "price": "₹9,960", "rating": 3.9, "distance_km": 1.2, "booking_url": "https://www.ihg.com"},
    ],
    # ── FIFA – Mexico ──
    "estadio_azteca": [
        {"hotel_name": "Fiesta Inn Perisur", "price": "₹7,055", "rating": 4.1, "distance_km": 3.0, "booking_url": "https://www.booking.com/searchresults.html?ss=Mexico+City"},
        {"hotel_name": "Hilton Mexico City Santa Fe", "price": "₹11,620", "rating": 4.5, "distance_km": 12.0, "booking_url": "https://www.hilton.com"},
        {"hotel_name": "Hotel Geneve", "price": "₹8,300", "rating": 4.3, "distance_km": 8.0, "booking_url": "https://www.expedia.com/Hotel-Search?destination=Mexico+City"},
    ],
    "estadio_bbva": [
        {"hotel_name": "Fiesta Americana Monterrey", "price": "₹7,885", "rating": 4.2, "distance_km": 5.0, "booking_url": "https://www.booking.com/searchresults.html?ss=Monterrey"},
        {"hotel_name": "Holiday Inn Express Monterrey", "price": "₹6,225", "rating": 3.9, "distance_km": 4.0, "booking_url": "https://www.ihg.com"},
    ],
    # ── FIFA – Canada ──
    "bmo_field": [
        {"hotel_name": "Hotel X Toronto", "price": "₹16,600", "rating": 4.6, "distance_km": 0.3, "booking_url": "https://www.booking.com/searchresults.html?ss=Hotel+X+Toronto"},
        {"hotel_name": "Radisson Blu Toronto Downtown", "price": "₹13,280", "rating": 4.2, "distance_km": 2.0, "booking_url": "https://www.booking.com/searchresults.html?ss=Radisson+Blu+Toronto+Downtown"},
    ],
    "bc_place": [
        {"hotel_name": "Fairmont Hotel Vancouver", "price": "₹23,240", "rating": 4.7, "distance_km": 1.0, "booking_url": "https://www.booking.com/searchresults.html?ss=Fairmont+Hotel+Vancouver"},
        {"hotel_name": "YWCA Hotel Vancouver", "price": "₹7,885", "rating": 3.8, "distance_km": 0.5, "booking_url": "https://www.booking.com/searchresults.html?ss=YWCA+Hotel+Vancouver"},
    ],
    # ── ICC – England ──
    "lords": [
        {"hotel_name": "The Langham London", "price": "₹20,750", "rating": 4.7, "distance_km": 2.4, "booking_url": "https://www.booking.com/searchresults.html?ss=The+Langham+London"},
        {"hotel_name": "Danubius Hotel Regent's Park", "price": "₹14,940", "rating": 4.3, "distance_km": 0.5, "booking_url": "https://www.booking.com/searchresults.html?ss=Danubius+Hotel+Regents+Park"},
        {"hotel_name": "Premier Inn London City", "price": "₹9,960", "rating": 4.0, "distance_km": 3.0, "booking_url": "https://www.booking.com/searchresults.html?ss=Premier+Inn+London+City"},
    ],
    "the_oval": [
        {"hotel_name": "Clayton Hotel City of London", "price": "₹14,110", "rating": 4.3, "distance_km": 2.0, "booking_url": "https://www.booking.com/searchresults.html?ss=Clayton+Hotel+City+of+London"},
        {"hotel_name": "Park Plaza Waterloo", "price": "₹16,600", "rating": 4.4, "distance_km": 1.5, "booking_url": "https://www.booking.com/searchresults.html?ss=Park+Plaza+Waterloo"},
        {"hotel_name": "Travelodge London Central", "price": "₹7,470", "rating": 3.7, "distance_km": 3.0, "booking_url": "https://www.booking.com/searchresults.html?ss=Travelodge+London+Central"},
    ],
    "edgbaston": [
        {"hotel_name": "Hotel du Vin Birmingham", "price": "₹12,865", "rating": 4.4, "distance_km": 0.8, "booking_url": "https://www.booking.com/searchresults.html?ss=Hotel+du+Vin+Birmingham"},
        {"hotel_name": "Hyatt Regency Birmingham", "price": "₹14,940", "rating": 4.3, "distance_km": 2.0, "booking_url": "https://www.booking.com/searchresults.html?ss=Hyatt+Regency+Birmingham"},
        {"hotel_name": "Premier Inn Edgbaston", "price": "₹6,640", "rating": 4.0, "distance_km": 1.0, "booking_url": "https://www.booking.com/searchresults.html?ss=Premier+Inn+Edgbaston"},
    ],
    "old_trafford": [
        {"hotel_name": "Hotel Football", "price": "₹13,695", "rating": 4.5, "distance_km": 0.3, "booking_url": "https://www.booking.com/searchresults.html?ss=Hotel+Football"},
        {"hotel_name": "Hilton Garden Inn Manchester", "price": "₹10,790", "rating": 4.2, "distance_km": 1.5, "booking_url": "https://www.booking.com/searchresults.html?ss=Hilton+Garden+Inn+Manchester"},
    ],
    "headingley": [
        {"hotel_name": "Headingley Lodge", "price": "₹8,300", "rating": 4.0, "distance_km": 0.2, "booking_url": "https://www.booking.com/searchresults.html?ss=Headingley+Lodge"},
        {"hotel_name": "Queens Hotel Leeds", "price": "₹11,620", "rating": 4.3, "distance_km": 3.0, "booking_url": "https://www.booking.com/searchresults.html?ss=Queens+Hotel+Leeds"},
    ],
    "hampshire_bowl": [
        {"hotel_name": "Hilton at the Ageas Bowl", "price": "₹14,525", "rating": 4.5, "distance_km": 0.1, "booking_url": "https://www.booking.com/searchresults.html?ss=Hilton+at+the+Ageas+Bowl"},
        {"hotel_name": "Holiday Inn Southampton", "price": "₹9,130", "rating": 4.0, "distance_km": 5.0, "booking_url": "https://www.booking.com/searchresults.html?ss=Holiday+Inn+Southampton"},
    ],
    "bristol_county": [
        {"hotel_name": "Mercure Bristol Grand", "price": "₹10,790", "rating": 4.2, "distance_km": 1.0, "booking_url": "https://www.booking.com/searchresults.html?ss=Mercure+Bristol+Grand"},
        {"hotel_name": "Premier Inn Bristol City Centre", "price": "₹7,055", "rating": 4.0, "distance_km": 0.5, "booking_url": "https://www.booking.com/searchresults.html?ss=Premier+Inn+Bristol+City+Centre"},
    ],
}

def search_nearby_hotels(venue_id: str) -> Dict:
    """Return a list of nearby hotels for a venue.
    If no curated data exists, generate a generic list.
    """
    hotels = _VENUE_HOTELS_DATA.get(venue_id)
    if not hotels:
        hotels = [
            {"hotel_name": f"Hotel {venue_id.title()} {i}",
             "price": f"₹{random.randint(100, 300) * 83:,}",
             "rating": round(random.uniform(3.5, 4.8), 1),
             "distance_km": round(random.uniform(0.5, 3.5), 1),
             "booking_url": f"https://www.booking.com/searchresults.html?ss={venue_id.replace('_', '+')}"
            } for i in range(1, 5)
        ]
    return {"venue_id": venue_id, "hotels": hotels, "count": len(hotels)}

# ---------------------------------------------------------------------------
# Flight search (mock data with realistic airline names)
# ---------------------------------------------------------------------------
_VENUE_AIRPORT_MAP = {
    # FIFA – USA
    "metlife_stadium": ["EWR", "JFK"],
    "sofi_stadium": ["LAX"],
    "att_stadium": ["DFW"],
    "nrg_stadium": ["IAH", "HOU"],
    "hard_rock_stadium": ["MIA", "FLL"],
    "mercedes_benz_stadium": ["ATL"],
    "lumen_field": ["SEA"],
    "levis_stadium": ["SJC", "SFO"],
    "gillette_stadium": ["BOS"],
    "lincoln_financial": ["PHL"],
    "arrowhead_stadium": ["MCI"],
    # FIFA – Mexico
    "estadio_azteca": ["MEX"],
    "estadio_bbva": ["MTY"],
    "estadio_akron": ["GDL"],
    # FIFA – Canada
    "bmo_field": ["YYZ"],
    "bc_place": ["YVR"],
    # ICC – England
    "lords": ["LHR", "LGW"],
    "the_oval": ["LHR", "LGW"],
    "edgbaston": ["BHX"],
    "old_trafford": ["MAN"],
    "headingley": ["LBA"],
    "hampshire_bowl": ["SOU", "LHR"],
    "bristol_county": ["BRS"],
}

def _mock_flight_data(origin_iata: str, dest_iata: str, date: str) -> List[Dict]:
    airlines = ["British Airways", "Delta", "American Airlines", "Emirates", "Virgin Atlantic"]
    flights = []
    for _ in range(4):
        price = random.randint(400, 1200)
        duration_h = random.randint(6, 12)
        duration_m = random.randint(0, 59)
        stops = random.choice([0, 1])
        flights.append({
            "price": f"₹{price * 83:,}",
            "airline": random.choice(airlines),
            "duration": f"{duration_h}h {duration_m}m",
            "stops": stops,
            "departure_date": date,
            "origin": origin_iata,
            "destination": dest_iata,
            "booking_url": f"https://www.kayak.co.in/flights/{origin_iata}-{dest_iata}/{date}",
        })
    flights.sort(key=lambda x: int(x["price"].replace("₹", "").replace(",", "")))
    return flights

_LAST_MILE = {
    "metlife_stadium": {"mode": "shuttle", "estimate": "₹1,660‑₹2,905", "description": "NJ Transit shuttle from EWR or taxi (~30 min)"},
    "sofi_stadium": {"mode": "metro", "estimate": "₹145", "description": "Metro C Line from LAX to Inglewood (~25 min)"},
    "att_stadium": {"mode": "taxi", "estimate": "₹2,490‑₹3,320", "description": "Taxi from DFW airport (~25 min)"},
    "hard_rock_stadium": {"mode": "taxi", "estimate": "₹2,075‑₹2,905", "description": "Taxi from MIA airport (~30 min)"},
    "mercedes_benz_stadium": {"mode": "metro", "estimate": "₹207", "description": "MARTA rail from ATL airport to Vine City station (~20 min)"},
    "estadio_azteca": {"mode": "metro", "estimate": "₹25", "description": "Metro Line 2 to Tasqueña, then shuttle (~40 min)"},
    "bmo_field": {"mode": "train", "estimate": "₹730", "description": "UP Express from YYZ to Union Station, then streetcar (~35 min)"},
    "lords": {"mode": "tube", "estimate": "₹525‑₹735", "description": "Heathrow Express to Paddington, then Bakerloo to Baker Street, walk (~50 min total)"},
    "the_oval": {"mode": "tube", "estimate": "₹525‑₹735", "description": "Piccadilly Line from LHR to Oval Station (~60 min)"},
    "edgbaston": {"mode": "train", "estimate": "₹315‑₹525", "description": "Train from BHX to Five Ways station, then walk (~30 min total)"},
    "old_trafford": {"mode": "tram", "estimate": "₹315‑₹525", "description": "Train from MAN airport to Piccadilly, then Metrolink tram (~40 min)"},
}

def _last_mile_info(venue_id: str, arrival_iata: str) -> Dict:
    info = _LAST_MILE.get(venue_id)
    if info:
        return info
    # Fallback for venues without specific data
    return {"mode": "taxi", "estimate": "₹2,075‑₹3,320", "description": f"Taxi from {arrival_iata} to venue (~30-45 min)"}

_CITY_TO_IATA = {
    "delhi": "DEL",
    "mumbai": "BOM",
    "bangalore": "BLR",
    "bengaluru": "BLR",
    "chennai": "MAA",
    "kolkata": "CCU",
    "hyderabad": "HYD",
    "ahmedabad": "AMD",
    "pune": "PNQ",
    "new york": "JFK",
    "london": "LHR",
    "los angeles": "LAX",
    "paris": "CDG",
    "tokyo": "HND",
    "dubai": "DXB",
    "singapore": "SIN",
    "sydney": "SYD",
    "toronto": "YYZ",
    "mexico city": "MEX",
    "atlanta": "ATL",
    "dallas": "DFW",
    "miami": "MIA",
    "chicago": "ORD",
    "houston": "IAH"
}

def _get_iata_for_city(city_name: str) -> str:
    if not city_name or city_name.strip().lower() == "any":
        return "ANY"
    city_lower = city_name.strip().lower()
    if city_lower in _CITY_TO_IATA:
        return _CITY_TO_IATA[city_lower]
    if len(city_lower) == 3:
        return city_lower.upper()
    return city_lower[:3].upper()

def search_flights(source_city: str, venue_id: str, departure_date: str) -> Dict:
    source_iata = _get_iata_for_city(source_city)
    dest_iatas = _VENUE_AIRPORT_MAP.get(venue_id)
    if not dest_iatas:
        return {"error": f"No airport mapping for venue '{venue_id}'"}
    dest_iata = dest_iatas[0]
    flights = _mock_flight_data(source_iata, dest_iata, departure_date)
    last_mile = _last_mile_info(venue_id, dest_iata)
    return {"source_city": source_city, "venue_id": venue_id, "destination_airport": dest_iata, "flights": flights, "last_mile": last_mile, "count": len(flights)}

# ---------------------------------------------------------------------------
# Match detail helper
# ---------------------------------------------------------------------------
def get_match_detail(match_id: str) -> Dict:
    match = next((m for m in MATCHES if m.get("_id") == match_id), None)
    if not match:
        return {"error": f"Match '{match_id}' not found"}
    venue = next((v for v in VENUES if v.get("_id") == match.get("venue_id")), {})
    return {
        "match_id": match_id,
        "event_id": match.get("event_id"),
        "round": match.get("round"),
        "date": match.get("date"),
        "teams": match.get("teams"),
        "venue": {"id": venue.get("_id"), "name": venue.get("name"), "city": venue.get("city"), "country": venue.get("country"), "capacity": venue.get("capacity")},
    }

__all__ = ["get_ticket_booking_url", "search_nearby_hotels", "search_flights", "get_match_detail"]
