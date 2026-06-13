import os
import json
import requests
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

_client = None
_db = None

def _get_db():
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(settings.MONGODB_URI)
        _db = _client[settings.MONGODB_DB]
    return _db


def search_matches(event_id: str = "", team: str = "", venue_id: str = "") -> dict:
    """Search for matches by event, team, or venue.

    Args:
        event_id: Filter by event ID (e.g., 'fifa_wc_2026' or 'icc_wt20_2026').
        team: Filter by team name (e.g., 'India', 'Brazil').
        venue_id: Filter by venue ID.

    Returns:
        A dictionary with matching results.
    """
    from app.data.seed_data import MATCHES, VENUES
    results = []
    for m in MATCHES:
        match = True
        if event_id and m["event_id"] != event_id:
            match = False
        if team:
            team_lower = team.lower()
            if not any(team_lower in t.lower() for t in m.get("teams", [])):
                match = False
        if venue_id and m.get("venue_id") != venue_id:
            match = False
        if match:
            venue = next((v for v in VENUES if v["_id"] == m["venue_id"]), {})
            results.append({
                "match_id": m["_id"],
                "round": m["round"],
                "date": m["date"],
                "teams": m["teams"],
                "venue": venue.get("name", ""),
                "city": venue.get("city", ""),
                "country": venue.get("country", ""),
                "expected_attendance": m.get("expected_attendance", 0),
                "significance": m.get("significance", "")
            })
    return {"matches": results, "count": len(results)}


def get_venue_details(venue_id: str) -> dict:
    """Get detailed information about a specific venue.

    Args:
        venue_id: The venue identifier (e.g., 'lords', 'metlife_stadium').

    Returns:
        Venue details including capacity, location, transport, and nearby attractions.
    """
    from app.data.seed_data import VENUES
    venue = next((v for v in VENUES if v["_id"] == venue_id), None)
    if not venue:
        return {"error": f"Venue '{venue_id}' not found. Available: {[v['_id'] for v in VENUES]}"}
    return venue


def list_venues(event_id: str = "") -> dict:
    """List all venues, optionally filtered by event.

    Args:
        event_id: Optional event ID filter ('fifa_wc_2026' or 'icc_wt20_2026').

    Returns:
        List of venues with basic details.
    """
    from app.data.seed_data import VENUES
    venues = VENUES
    if event_id:
        venues = [v for v in venues if v["event_id"] == event_id]
    return {
        "venues": [{"id": v["_id"], "name": v["name"], "city": v["city"], "country": v["country"], "capacity": v["capacity"], "hosts_final": v.get("hosts_final", False)} for v in venues],
        "count": len(venues)
    }


def get_event_info(event_id: str) -> dict:
    """Get information about a specific event.

    Args:
        event_id: The event identifier ('fifa_wc_2026' or 'icc_wt20_2026').

    Returns:
        Event details including dates, host countries, and format.
    """
    from app.data.seed_data import EVENTS
    event = next((e for e in EVENTS if e["_id"] == event_id), None)
    if not event:
        return {"error": f"Event not found. Available: fifa_wc_2026, icc_wt20_2026"}
    return event


def create_fan_itinerary(
    fan_name: str,
    origin: str,
    event_id: str,
    interests: str,
    budget: str,
    travel_from: str,
    travel_to: str
) -> dict:
    """Create a personalized travel itinerary for a fan.

    Args:
        fan_name: The fan's name.
        origin: Where the fan is traveling from (e.g., 'Ranchi, India').
        event_id: Which event ('fifa_wc_2026' or 'icc_wt20_2026').
        interests: Comma-separated interests (e.g., 'India matches, final').
        budget: Budget level ('budget', 'moderate', 'luxury').
        travel_from: Start date of travel (YYYY-MM-DD).
        travel_to: End date of travel (YYYY-MM-DD).

    Returns:
        A complete itinerary stored in the database.
    """
    from app.data.seed_data import MATCHES, VENUES

    # Find relevant matches
    interest_list = [i.strip().lower() for i in interests.split(",")]
    relevant_matches = []
    for m in MATCHES:
        if m["event_id"] != event_id:
            continue
        teams_lower = [t.lower() for t in m.get("teams", [])]
        round_lower = m.get("round", "").lower()
        sig_lower = m.get("significance", "").lower()
        for interest in interest_list:
            if interest in teams_lower or interest in round_lower or interest in sig_lower:
                venue = next((v for v in VENUES if v["_id"] == m["venue_id"]), {})
                relevant_matches.append({
                    "match": m["round"] + ": " + " vs ".join(m["teams"]),
                    "date": m["date"],
                    "venue": venue.get("name", ""),
                    "city": venue.get("city", ""),
                    "transport": venue.get("transport", []),
                    "nearby": venue.get("nearby_attractions", [])
                })
                break

    itinerary = {
        "fan_name": fan_name,
        "origin": origin,
        "event_id": event_id,
        "budget": budget,
        "travel_dates": {"from": travel_from, "to": travel_to},
        "recommended_matches": relevant_matches,
        "created_at": datetime.utcnow().isoformat(),
        "tips": _get_travel_tips(origin, event_id, budget)
    }

    return {"itinerary": itinerary, "status": "created"}


def calculate_live_travel_time(origin: str, venue_id: str) -> dict:
    """Calculate real-time driving distance and duration to a venue using Google Maps API.

    Args:
        origin: The starting address or location (e.g., 'Times Square, NY').
        venue_id: The destination venue identifier.

    Returns:
        Live travel time, distance, and traffic conditions.
    """
    from app.data.seed_data import VENUES
    venue = next((v for v in VENUES if v["_id"] == venue_id), None)
    if not venue:
        return {"error": f"Venue '{venue_id}' not found."}

    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return {
            "origin": origin,
            "destination": venue["name"],
            "note": "GOOGLE_MAPS_API_KEY not configured. Using estimated static distance.",
            "distance": "15 km (estimated)",
            "duration": "35 mins (estimated)",
            "traffic": "moderate"
        }

    lat, lng = venue.get("lat"), venue.get("lng")
    if not lat or not lng:
        return {"error": "Coordinates not available for this venue."}

    # Format destination as lat,lng
    destination = f"{lat},{lng}"
    
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&departure_time=now&key={api_key}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "OK":
            return {"error": f"Google Maps API error: {data.get('status')}"}
            
        element = data["rows"][0]["elements"][0]
        if element.get("status") != "OK":
            return {"error": f"Route calculation failed: {element.get('status')}"}
            
        distance = element["distance"]["text"]
        duration = element["duration"]["text"]
        
        # duration_in_traffic is only returned if departure_time=now is used and the route has traffic
        duration_in_traffic = element.get("duration_in_traffic", {}).get("text", duration)
        
        return {
            "origin": origin,
            "destination": venue["name"],
            "distance": distance,
            "normal_duration": duration,
            "current_duration_with_traffic": duration_in_traffic
        }
    except Exception as e:
        return {"error": f"Failed to fetch live travel time: {str(e)}"}


def get_nearby_businesses(venue_id: str, business_type: str = "") -> dict:
    """Find businesses near a specific venue.

    Args:
        venue_id: The venue identifier.
        business_type: Optional filter ('restaurant', 'hotel', 'cafe').

    Returns:
        List of nearby businesses with details.
    """
    from app.data.seed_data import BUSINESSES
    results = [b for b in BUSINESSES if b["venue_id"] == venue_id]
    if business_type:
        results = [b for b in results if b["type"] == business_type]
    return {"businesses": results, "count": len(results)}


async def semantic_search(query: str, search_type: str = "venues") -> dict:
    """Search for venues or matches using natural language semantic meaning.

    Args:
        query: The natural language query (e.g., 'stadiums near water', 'important matches').
        search_type: Which collection to search, either 'venues' or 'matches'.

    Returns:
        List of semantically relevant records from the database.
    """
    import os
    try:
        from google import genai
    except ImportError:
        return {"error": "google-genai not installed or configured."}

    if not os.getenv("GOOGLE_API_KEY"):
        return {"error": "GOOGLE_API_KEY is missing. Cannot generate embeddings for search."}

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    
    try:
        # Embed the search query
        resp = client.models.embed_content(
            model="gemini-embedding-2", 
            contents=query
        )
        if hasattr(resp, 'embeddings') and resp.embeddings:
            query_vector = resp.embeddings[0].values
        else:
            return {"error": "Failed to extract embeddings from the model response."}
    except Exception as e:
        return {"error": f"Failed to embed query: {e}"}

    # Perform the vector search against MongoDB
    db = _get_db()
    if search_type not in ["venues", "matches"]:
        search_type = "venues"
        
    collection = db[search_type]
    
    # Run aggregation pipeline
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": 100,
                "limit": 5
            }
        },
        {
            "$project": {
                "embedding": 0,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]

    try:
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=5)
        
        # Convert _id to string for JSON serialization
        for r in results:
            if '_id' in r:
                r['_id'] = str(r['_id'])
                
        return {"results": results, "count": len(results)}
    except Exception as e:
        return {
            "error": f"MongoDB Vector Search failed: {e}. "
                     "Have you created the 'vector_index' on this collection in Atlas?"
        }


def search_live_flights(origin_iata: str, destination_iata: str, departure_date: str) -> dict:
    """Search for real-time flight pricing and availability using the Amadeus API.
    
    Args:
        origin_iata: 3-letter IATA airport code for departure (e.g., 'JFK', 'LHR', 'DEL').
        destination_iata: 3-letter IATA airport code for arrival (e.g., 'JFK', 'LHR', 'DEL').
        departure_date: Date of departure in YYYY-MM-DD format.
        
    Returns:
        Live flight offers with prices, airlines, and durations.
    """
    import os
    try:
        from amadeus import Client, ResponseError
    except ImportError:
        return {"error": "Amadeus SDK not installed."}

    client_id = os.getenv("AMADEUS_CLIENT_ID")
    client_secret = os.getenv("AMADEUS_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        # MOCK MODE: Return realistic simulated flight data for the hackathon
        import random
        airlines = ["British Airways", "Delta", "Virgin Atlantic", "American Airlines", "Emirates"]
        return {
            "flights": [
                {
                    "price": f"{random.randint(450, 1200)}.00 USD",
                    "duration": f"{random.randint(6, 14)}H {random.randint(10, 50)}M",
                    "airline_code": random.choice(airlines),
                    "segments": random.randint(1, 2)
                } for _ in range(3)
            ],
            "count": 3,
            "note": "Using Simulated Flight Data (Amadeus Keys Missing)"
        }

    try:
        amadeus = Client(client_id=client_id, client_secret=client_secret)
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin_iata,
            destinationLocationCode=destination_iata,
            departureDate=departure_date,
            adults=1,
            max=5
        )
        
        flights = []
        for offer in response.data:
            price = offer.get("price", {})
            currency = price.get("currency", "USD")
            total = price.get("total", "0.00")
            
            itineraries = offer.get("itineraries", [])
            duration = itineraries[0].get("duration", "N/A") if itineraries else "N/A"
            
            # Get airline code from first segment
            segments = itineraries[0].get("segments", []) if itineraries else []
            airline = segments[0].get("carrierCode", "Unknown") if segments else "Unknown"
            
            flights.append({
                "price": f"{total} {currency}",
                "duration": duration,
                "airline_code": airline,
                "segments": len(segments)
            })
            
        return {"flights": flights, "count": len(flights)}
    except Exception as e:
        return {"error": f"Amadeus Flight API failed: {str(e)}"}


def search_live_hotels(city_code: str, check_in_date: str, check_out_date: str) -> dict:
    """Search for real-time hotel pricing and availability using the Amadeus API.
    
    Args:
        city_code: 3-letter IATA city code (e.g., 'NYC', 'LON', 'PAR').
        check_in_date: Date of check-in in YYYY-MM-DD format.
        check_out_date: Date of check-out in YYYY-MM-DD format.
        
    Returns:
        Live hotel offers with prices and hotel names.
    """
    import os
    try:
        from amadeus import Client, ResponseError
    except ImportError:
        return {"error": "Amadeus SDK not installed."}

    client_id = os.getenv("AMADEUS_CLIENT_ID")
    client_secret = os.getenv("AMADEUS_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        # MOCK MODE: Return realistic simulated hotel data for the hackathon
        import random
        hotel_brands = ["Marriott", "Hilton", "Hyatt", "Radisson", "InterContinental"]
        return {
            "hotels": [
                {
                    "hotel_name": f"{random.choice(hotel_brands)} {city_code} Center",
                    "price": f"{random.randint(150, 450)}.00 USD",
                    "hotel_id": f"HTL{random.randint(1000, 9999)}"
                } for _ in range(4)
            ],
            "count": 4,
            "note": "Using Simulated Hotel Data (Amadeus Keys Missing)"
        }

    try:
        amadeus = Client(client_id=client_id, client_secret=client_secret)
        
        # Amadeus v3 hotel search requires two steps: get hotel IDs by city, then get offers
        # Step 1: Get hotels in city
        hotels_response = amadeus.reference_data.locations.hotels.by_city.get(
            cityCode=city_code, radius=5, radiusUnit='KM'
        )
        
        if not hotels_response.data:
            return {"error": f"No hotels found in {city_code}"}
            
        # Get up to 10 hotel IDs
        hotel_ids = [hotel["hotelId"] for hotel in hotels_response.data[:10]]
        
        # Step 2: Get offers for these hotels
        offers_response = amadeus.shopping.hotel_offers_search.get(
            hotelIds=','.join(hotel_ids),
            checkInDate=check_in_date,
            checkOutDate=check_out_date,
            adults=1
        )
        
        hotels = []
        for offer in offers_response.data:
            hotel_data = offer.get("hotel", {})
            hotel_name = hotel_data.get("name", "Unknown Hotel")
            
            # Just get the lowest price offer
            offers_list = offer.get("offers", [])
            if not offers_list:
                continue
                
            price_data = offers_list[0].get("price", {})
            total = price_data.get("total", "0.00")
            currency = price_data.get("currency", "USD")
            
            hotels.append({
                "hotel_name": hotel_name,
                "price": f"{total} {currency}",
                "hotel_id": hotel_data.get("hotelId")
            })
            
        return {"hotels": hotels, "count": len(hotels)}
    except Exception as e:
        return {"error": f"Amadeus Hotel API failed: {str(e)}"}


def _get_travel_tips(origin: str, event_id: str, budget: str) -> list:
    """Generate travel tips based on origin and event."""
    tips = []
    origin_lower = origin.lower()
    if event_id == "icc_wt20_2026":
        tips.append("UK Tourist Visa required for Indian nationals — apply at least 4 weeks in advance.")
        tips.append("London Oyster Card recommended for public transport — covers Tube, Bus, DLR.")
        tips.append("Cricket grounds in England serve food and beverages; outside food may be restricted.")
        if "india" in origin_lower:
            tips.append("Direct flights available from Delhi/Mumbai to London Heathrow (8-9 hours).")
            tips.append("Time difference: UK is IST -4:30 hours (BST during summer).")
        if budget == "budget":
            tips.append("Consider hostels in zones 2-3 for affordable London accommodation.")
            tips.append("National Express coaches connect cricket venues cheaply.")
        elif budget == "luxury":
            tips.append("Consider The Langham or Claridge's for luxury London stay.")
    elif event_id == "fifa_wc_2026":
        tips.append("ESTA required for visitors from Visa Waiver countries; others need US tourist visa.")
        tips.append("Matches span 3 countries — check visa requirements for Mexico and Canada too.")
        if "india" in origin_lower:
            tips.append("US B1/B2 tourist visa required — apply well in advance.")
            tips.append("Direct flights to NYC from Delhi/Mumbai (15-16 hours).")
        if budget == "budget":
            tips.append("Greyhound/FlixBus connects cities cheaply. Share Airbnbs near venues.")
        elif budget == "luxury":
            tips.append("Consider Mandarin Oriental NYC or Four Seasons for the final.")
    return tips
