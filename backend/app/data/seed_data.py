"""Seed data for TurfGrid AI - FIFA World Cup 2026 & ICC Women's T20 World Cup 2026."""
import os
import json
try:
    from google import genai
    from google.genai import errors
except ImportError:
    genai = None
EVENTS = [
    {
        "_id": "fifa_wc_2026",
        "name": "FIFA World Cup 2026",
        "short_name": "FIFA WC 2026",
        "sport": "football",
        "start_date": "2026-06-11",
        "end_date": "2026-07-19",
        "host_countries": ["United States", "Mexico", "Canada"],
        "teams": 48,
        "total_matches": 104,
        "format": "Group Stage (12 groups of 4) → Round of 32 → Knockout",
        "description": "The first FIFA World Cup with 48 teams, co-hosted by three nations across 16 cities in North America.",
        "icon": "⚽",
        "color": "#e11d48"
    },
    {
        "_id": "icc_wt20_2026",
        "name": "ICC Women's T20 World Cup 2026",
        "short_name": "ICC WT20 2026",
        "sport": "cricket",
        "start_date": "2026-06-12",
        "end_date": "2026-07-05",
        "host_countries": ["England"],
        "teams": 12,
        "total_matches": 33,
        "format": "Group Stage (3 groups of 4) → Super Six → Semi-Finals → Final",
        "description": "The premier women's T20 cricket tournament, hosted across 7 iconic English cricket grounds.",
        "icon": "🏏",
        "color": "#2563eb"
    }
]

VENUES = [
    # FIFA World Cup 2026 Venues - United States (11)
    {"_id": "metlife_stadium", "name": "MetLife Stadium", "city": "East Rutherford", "state": "New Jersey", "country": "United States", "capacity": 82500, "event_id": "fifa_wc_2026", "lat": 40.8128, "lng": -74.0742, "hosts_final": True, "timezone": "America/New_York", "transport": ["NJ Transit", "PATH Train", "Shuttle Bus"], "nearby_attractions": ["Times Square", "Central Park", "Statue of Liberty"]},
    {"_id": "sofi_stadium", "name": "SoFi Stadium", "city": "Inglewood", "state": "California", "country": "United States", "capacity": 70240, "event_id": "fifa_wc_2026", "lat": 33.9535, "lng": -118.3392, "hosts_final": False, "timezone": "America/Los_Angeles", "transport": ["Metro C Line", "LAX Shuttle", "Uber/Lyft"], "nearby_attractions": ["Hollywood", "Santa Monica", "Venice Beach"]},
    {"_id": "att_stadium", "name": "AT&T Stadium", "city": "Arlington", "state": "Texas", "country": "United States", "capacity": 80000, "event_id": "fifa_wc_2026", "lat": 32.7473, "lng": -97.0945, "hosts_final": False, "timezone": "America/Chicago", "transport": ["TRE Rail", "Shuttle Bus", "Rideshare"], "nearby_attractions": ["Dallas Arts District", "Fort Worth Stockyards"]},
    {"_id": "nrg_stadium", "name": "NRG Stadium", "city": "Houston", "state": "Texas", "country": "United States", "capacity": 72220, "event_id": "fifa_wc_2026", "lat": 29.6847, "lng": -95.4107, "hosts_final": False, "timezone": "America/Chicago", "transport": ["METRORail", "Park & Ride", "Shuttle"], "nearby_attractions": ["Space Center Houston", "Museum District"]},
    {"_id": "hard_rock_stadium", "name": "Hard Rock Stadium", "city": "Miami Gardens", "state": "Florida", "country": "United States", "capacity": 64767, "event_id": "fifa_wc_2026", "lat": 25.958, "lng": -80.2389, "hosts_final": False, "timezone": "America/New_York", "transport": ["Tri-Rail", "Express Bus", "Rideshare"], "nearby_attractions": ["South Beach", "Art Deco District", "Everglades"]},
    {"_id": "mercedes_benz_stadium", "name": "Mercedes-Benz Stadium", "city": "Atlanta", "state": "Georgia", "country": "United States", "capacity": 71000, "event_id": "fifa_wc_2026", "lat": 33.7554, "lng": -84.4005, "hosts_final": False, "timezone": "America/New_York", "transport": ["MARTA Rail", "Streetcar", "Shuttle"], "nearby_attractions": ["Georgia Aquarium", "World of Coca-Cola"]},
    {"_id": "lumen_field", "name": "Lumen Field", "city": "Seattle", "state": "Washington", "country": "United States", "capacity": 69000, "event_id": "fifa_wc_2026", "lat": 47.5952, "lng": -122.3316, "hosts_final": False, "timezone": "America/Los_Angeles", "transport": ["Link Light Rail", "Sounder Train", "Ferry"], "nearby_attractions": ["Pike Place Market", "Space Needle"]},
    {"_id": "levis_stadium", "name": "Levi's Stadium", "city": "Santa Clara", "state": "California", "country": "United States", "capacity": 68500, "event_id": "fifa_wc_2026", "lat": 37.4033, "lng": -121.9694, "hosts_final": False, "timezone": "America/Los_Angeles", "transport": ["Caltrain", "VTA Light Rail", "Shuttle"], "nearby_attractions": ["Silicon Valley", "San Francisco"]},
    {"_id": "gillette_stadium", "name": "Gillette Stadium", "city": "Foxborough", "state": "Massachusetts", "country": "United States", "capacity": 65878, "event_id": "fifa_wc_2026", "lat": 42.0909, "lng": -71.2643, "hosts_final": False, "timezone": "America/New_York", "transport": ["MBTA Commuter Rail", "Shuttle Bus"], "nearby_attractions": ["Boston Harbor", "Freedom Trail"]},
    {"_id": "lincoln_financial", "name": "Lincoln Financial Field", "city": "Philadelphia", "state": "Pennsylvania", "country": "United States", "capacity": 69176, "event_id": "fifa_wc_2026", "lat": 39.9008, "lng": -75.1675, "hosts_final": False, "timezone": "America/New_York", "transport": ["SEPTA Subway", "NJ Transit", "Shuttle"], "nearby_attractions": ["Liberty Bell", "Independence Hall"]},
    {"_id": "arrowhead_stadium", "name": "Arrowhead Stadium", "city": "Kansas City", "state": "Missouri", "country": "United States", "capacity": 76416, "event_id": "fifa_wc_2026", "lat": 39.0489, "lng": -94.484, "hosts_final": False, "timezone": "America/Chicago", "transport": ["KC Streetcar", "Express Bus", "Rideshare"], "nearby_attractions": ["Country Club Plaza", "National WWI Museum"]},
    # FIFA - Mexico (3)
    {"_id": "estadio_azteca", "name": "Estadio Azteca", "city": "Mexico City", "state": "CDMX", "country": "Mexico", "capacity": 87523, "event_id": "fifa_wc_2026", "lat": 19.3029, "lng": -99.1505, "hosts_final": False, "timezone": "America/Mexico_City", "transport": ["Metro Line 2", "Metrobus", "Taxi"], "nearby_attractions": ["Zocalo", "Teotihuacan", "Chapultepec"]},
    {"_id": "estadio_bbva", "name": "Estadio BBVA", "city": "Monterrey", "state": "Nuevo Leon", "country": "Mexico", "capacity": 53500, "event_id": "fifa_wc_2026", "lat": 25.6663, "lng": -100.2447, "hosts_final": False, "timezone": "America/Monterrey", "transport": ["Metrorrey", "Bus", "Uber"], "nearby_attractions": ["Cerro de la Silla", "Macroplaza"]},
    {"_id": "estadio_akron", "name": "Estadio Akron", "city": "Guadalajara", "state": "Jalisco", "country": "Mexico", "capacity": 49850, "event_id": "fifa_wc_2026", "lat": 20.6821, "lng": -103.4626, "hosts_final": False, "timezone": "America/Mexico_City", "transport": ["Mi Macro", "Bus", "Taxi"], "nearby_attractions": ["Tequila Town", "Lake Chapala"]},
    # FIFA - Canada (2)
    {"_id": "bmo_field", "name": "BMO Field", "city": "Toronto", "state": "Ontario", "country": "Canada", "capacity": 45736, "event_id": "fifa_wc_2026", "lat": 43.6332, "lng": -79.4186, "hosts_final": False, "timezone": "America/Toronto", "transport": ["TTC Streetcar", "GO Transit", "UP Express"], "nearby_attractions": ["CN Tower", "Royal Ontario Museum"]},
    {"_id": "bc_place", "name": "BC Place", "city": "Vancouver", "state": "British Columbia", "country": "Canada", "capacity": 54500, "event_id": "fifa_wc_2026", "lat": 49.2768, "lng": -123.112, "hosts_final": False, "timezone": "America/Vancouver", "transport": ["SkyTrain", "SeaBus", "Bus"], "nearby_attractions": ["Stanley Park", "Granville Island"]},
    # ICC Women's T20 World Cup 2026 Venues (7)
    {"_id": "lords", "name": "Lord's Cricket Ground", "city": "London", "state": "England", "country": "England", "capacity": 30000, "event_id": "icc_wt20_2026", "lat": 51.5294, "lng": -0.1728, "hosts_final": True, "timezone": "Europe/London", "transport": ["Jubilee Line", "Metropolitan Line", "Bus 13/82"], "nearby_attractions": ["Regent's Park", "Baker Street", "Camden Market"]},
    {"_id": "the_oval", "name": "The Oval", "city": "London", "state": "England", "country": "England", "capacity": 25500, "event_id": "icc_wt20_2026", "lat": 51.4837, "lng": -0.1149, "hosts_final": False, "timezone": "Europe/London", "transport": ["Northern Line", "Bus 36/185", "Vauxhall Station"], "nearby_attractions": ["Big Ben", "London Eye", "Westminster"]},
    {"_id": "edgbaston", "name": "Edgbaston Cricket Ground", "city": "Birmingham", "state": "England", "country": "England", "capacity": 25000, "event_id": "icc_wt20_2026", "lat": 52.4559, "lng": -1.9025, "hosts_final": False, "timezone": "Europe/London", "transport": ["Train to Five Ways", "Bus 45/47", "Tram"], "nearby_attractions": ["Cadbury World", "Bullring", "Library of Birmingham"]},
    {"_id": "old_trafford", "name": "Old Trafford Cricket Ground", "city": "Manchester", "state": "England", "country": "England", "capacity": 26000, "event_id": "icc_wt20_2026", "lat": 53.4569, "lng": -2.2872, "hosts_final": False, "timezone": "Europe/London", "transport": ["Metrolink Tram", "Train to Old Trafford", "Bus"], "nearby_attractions": ["Old Trafford Football", "Manchester Museum"]},
    {"_id": "headingley", "name": "Headingley", "city": "Leeds", "state": "England", "country": "England", "capacity": 18350, "event_id": "icc_wt20_2026", "lat": 53.8178, "lng": -1.5822, "hosts_final": False, "timezone": "Europe/London", "transport": ["Bus 56/19", "Train to Headingley", "Walk from Burley Park"], "nearby_attractions": ["Royal Armouries", "Leeds City Centre"]},
    {"_id": "hampshire_bowl", "name": "Hampshire Bowl", "city": "Southampton", "state": "England", "country": "England", "capacity": 25000, "event_id": "icc_wt20_2026", "lat": 50.9244, "lng": -1.3222, "hosts_final": False, "timezone": "Europe/London", "transport": ["Train to Southampton", "Bus", "Shuttle from Station"], "nearby_attractions": ["Titanic Museum", "New Forest", "Isle of Wight Ferry"]},
    {"_id": "bristol_county", "name": "Bristol County Ground", "city": "Bristol", "state": "England", "country": "England", "capacity": 17500, "event_id": "icc_wt20_2026", "lat": 51.4571, "lng": -2.5833, "hosts_final": False, "timezone": "Europe/London", "transport": ["Bus from Temple Meads", "Walk from City Centre"], "nearby_attractions": ["Clifton Suspension Bridge", "SS Great Britain", "Harbourside"]},
]

MATCHES = [
    # FIFA World Cup 2026 - Key Matches
    {"_id": "fifa_opening", "event_id": "fifa_wc_2026", "round": "Group Stage - Opening Match", "date": "2026-06-11T18:00:00Z", "venue_id": "estadio_azteca", "teams": ["Mexico", "TBD"], "expected_attendance": 87000, "significance": "Opening Ceremony & Match"},
    {"_id": "fifa_usa_opener", "event_id": "fifa_wc_2026", "round": "Group Stage", "date": "2026-06-12T21:00:00Z", "venue_id": "sofi_stadium", "teams": ["United States", "TBD"], "expected_attendance": 70000, "significance": "USA's first home World Cup match since 1994"},
    {"_id": "fifa_brazil_arg", "event_id": "fifa_wc_2026", "round": "Group Stage", "date": "2026-06-18T18:00:00Z", "venue_id": "hard_rock_stadium", "teams": ["Brazil", "Argentina"], "expected_attendance": 64000, "significance": "South American classic rivalry"},
    {"_id": "fifa_eng_fra", "event_id": "fifa_wc_2026", "round": "Group Stage", "date": "2026-06-20T21:00:00Z", "venue_id": "metlife_stadium", "teams": ["England", "France"], "expected_attendance": 82000, "significance": "European heavyweight clash"},
    {"_id": "fifa_ind_group", "event_id": "fifa_wc_2026", "round": "Group Stage", "date": "2026-06-15T15:00:00Z", "venue_id": "mercedes_benz_stadium", "teams": ["India", "TBD"], "expected_attendance": 71000, "significance": "India's historic first World Cup match"},
    {"_id": "fifa_r16_1", "event_id": "fifa_wc_2026", "round": "Round of 16", "date": "2026-06-28T18:00:00Z", "venue_id": "att_stadium", "teams": ["TBD", "TBD"], "expected_attendance": 80000, "significance": "Knockout stage begins"},
    {"_id": "fifa_qf_1", "event_id": "fifa_wc_2026", "round": "Quarter-Final", "date": "2026-07-04T21:00:00Z", "venue_id": "sofi_stadium", "teams": ["TBD", "TBD"], "expected_attendance": 70000, "significance": "Quarter-Final on July 4th"},
    {"_id": "fifa_sf_1", "event_id": "fifa_wc_2026", "round": "Semi-Final", "date": "2026-07-14T21:00:00Z", "venue_id": "metlife_stadium", "teams": ["TBD", "TBD"], "expected_attendance": 82500, "significance": "Semi-Final 1"},
    {"_id": "fifa_sf_2", "event_id": "fifa_wc_2026", "round": "Semi-Final", "date": "2026-07-15T21:00:00Z", "venue_id": "att_stadium", "teams": ["TBD", "TBD"], "expected_attendance": 80000, "significance": "Semi-Final 2"},
    {"_id": "fifa_final", "event_id": "fifa_wc_2026", "round": "Final", "date": "2026-07-19T20:00:00Z", "venue_id": "metlife_stadium", "teams": ["TBD", "TBD"], "expected_attendance": 82500, "significance": "FIFA World Cup 2026 Final"},
    # ICC Women's T20 World Cup 2026 - Key Matches
    {"_id": "icc_opening", "event_id": "icc_wt20_2026", "round": "Group Stage - Opening Match", "date": "2026-06-12T14:00:00Z", "venue_id": "edgbaston", "teams": ["England", "South Africa"], "expected_attendance": 25000, "significance": "Opening Ceremony & Match"},
    {"_id": "icc_ind_eng", "event_id": "icc_wt20_2026", "round": "Group Stage", "date": "2026-06-15T14:00:00Z", "venue_id": "lords", "teams": ["India", "England"], "expected_attendance": 30000, "significance": "Marquee group match — India vs hosts England"},
    {"_id": "icc_aus_nz", "event_id": "icc_wt20_2026", "round": "Group Stage", "date": "2026-06-16T10:30:00Z", "venue_id": "old_trafford", "teams": ["Australia", "New Zealand"], "expected_attendance": 22000, "significance": "Trans-Tasman rivalry"},
    {"_id": "icc_ind_pak", "event_id": "icc_wt20_2026", "round": "Group Stage", "date": "2026-06-20T14:00:00Z", "venue_id": "the_oval", "teams": ["India", "Pakistan"], "expected_attendance": 25500, "significance": "Most-watched women's cricket match"},
    {"_id": "icc_ind_aus", "event_id": "icc_wt20_2026", "round": "Super Six", "date": "2026-06-25T14:00:00Z", "venue_id": "edgbaston", "teams": ["India", "Australia"], "expected_attendance": 25000, "significance": "India vs reigning champions"},
    {"_id": "icc_sf_1", "event_id": "icc_wt20_2026", "round": "Semi-Final 1", "date": "2026-07-01T14:00:00Z", "venue_id": "the_oval", "teams": ["TBD", "TBD"], "expected_attendance": 25500, "significance": "Semi-Final 1"},
    {"_id": "icc_sf_2", "event_id": "icc_wt20_2026", "round": "Semi-Final 2", "date": "2026-07-02T14:00:00Z", "venue_id": "the_oval", "teams": ["TBD", "TBD"], "expected_attendance": 25500, "significance": "Semi-Final 2"},
    {"_id": "icc_final", "event_id": "icc_wt20_2026", "round": "Final", "date": "2026-07-05T14:00:00Z", "venue_id": "lords", "teams": ["TBD", "TBD"], "expected_attendance": 30000, "significance": "ICC Women's T20 World Cup 2026 Final at the Home of Cricket"},
]

BUSINESSES = [
    # Near Lord's
    {"_id": "biz_lords_1", "name": "The Lord's Tavern", "type": "restaurant", "cuisine": "British Pub", "venue_id": "lords", "distance_km": 0.3, "capacity": 120, "normal_daily_covers": 80, "rating": 4.3},
    {"_id": "biz_lords_2", "name": "Primrose Bakery", "type": "cafe", "cuisine": "Bakery & Cafe", "venue_id": "lords", "distance_km": 0.5, "capacity": 40, "normal_daily_covers": 60, "rating": 4.5},
    {"_id": "biz_lords_3", "name": "Danubius Hotel Regent's Park", "type": "hotel", "cuisine": None, "venue_id": "lords", "distance_km": 0.4, "capacity": 365, "normal_daily_covers": None, "rating": 4.1},
    # Near MetLife Stadium
    {"_id": "biz_metlife_1", "name": "Benny Tudino's Pizzeria", "type": "restaurant", "cuisine": "Italian", "venue_id": "metlife_stadium", "distance_km": 3.0, "capacity": 80, "normal_daily_covers": 100, "rating": 4.6},
    {"_id": "biz_metlife_2", "name": "Marriott Meadowlands", "type": "hotel", "cuisine": None, "venue_id": "metlife_stadium", "distance_km": 1.5, "capacity": 227, "normal_daily_covers": None, "rating": 4.2},
    {"_id": "biz_metlife_3", "name": "The Biergarten", "type": "restaurant", "cuisine": "German", "venue_id": "metlife_stadium", "distance_km": 2.0, "capacity": 200, "normal_daily_covers": 120, "rating": 4.4},
    # Near Edgbaston
    {"_id": "biz_edg_1", "name": "The Physician Pub", "type": "restaurant", "cuisine": "British Gastropub", "venue_id": "edgbaston", "distance_km": 0.6, "capacity": 150, "normal_daily_covers": 90, "rating": 4.2},
    {"_id": "biz_edg_2", "name": "Hotel du Vin Birmingham", "type": "hotel", "cuisine": None, "venue_id": "edgbaston", "distance_km": 0.8, "capacity": 66, "normal_daily_covers": None, "rating": 4.4},
    # Near SoFi Stadium
    {"_id": "biz_sofi_1", "name": "Woody's Diner", "type": "restaurant", "cuisine": "American", "venue_id": "sofi_stadium", "distance_km": 1.2, "capacity": 90, "normal_daily_covers": 70, "rating": 4.3},
    {"_id": "biz_sofi_2", "name": "SoFi Hotel & Suites", "type": "hotel", "cuisine": None, "venue_id": "sofi_stadium", "distance_km": 0.8, "capacity": 180, "normal_daily_covers": None, "rating": 4.0},
    # Near The Oval
    {"_id": "biz_oval_1", "name": "Kennington Tandoori", "type": "restaurant", "cuisine": "Indian", "venue_id": "the_oval", "distance_km": 0.2, "capacity": 60, "normal_daily_covers": 50, "rating": 4.5},
    {"_id": "biz_oval_2", "name": "Clayton Hotel City of London", "type": "hotel", "cuisine": None, "venue_id": "the_oval", "distance_km": 2.0, "capacity": 212, "normal_daily_covers": None, "rating": 4.3},
]

CROWD_DATA = [
    # Historical/predicted crowd data
    {"_id": "crowd_metlife_final", "venue_id": "metlife_stadium", "match_id": "fifa_final", "predicted_attendance": 82500, "venue_capacity": 82500, "utilization_pct": 100, "peak_hours": ["17:00-20:00"], "congestion_level": "extreme", "recommended_arrival_hours_before": 4, "estimated_queue_minutes": 45, "parking_availability": "limited", "public_transport_load": "extreme", "alternative_routes": ["Take NJ Transit to Secaucus Junction, then shuttle", "PATH to Hoboken, then bus NJT 165"]},
    {"_id": "crowd_lords_final", "venue_id": "lords", "match_id": "icc_final", "predicted_attendance": 30000, "venue_capacity": 30000, "utilization_pct": 100, "peak_hours": ["12:00-14:00"], "congestion_level": "high", "recommended_arrival_hours_before": 2, "estimated_queue_minutes": 25, "parking_availability": "none", "public_transport_load": "high", "alternative_routes": ["Walk from Baker Street (10 min)", "Bus 13 from Oxford Circus"]},
    {"_id": "crowd_lords_ind_eng", "venue_id": "lords", "match_id": "icc_ind_eng", "predicted_attendance": 30000, "venue_capacity": 30000, "utilization_pct": 100, "peak_hours": ["12:00-14:00"], "congestion_level": "high", "recommended_arrival_hours_before": 2, "estimated_queue_minutes": 30, "parking_availability": "none", "public_transport_load": "very_high", "alternative_routes": ["Jubilee Line to St John's Wood", "Metropolitan Line + walk"]},
    {"_id": "crowd_oval_ind_pak", "venue_id": "the_oval", "match_id": "icc_ind_pak", "predicted_attendance": 25500, "venue_capacity": 25500, "utilization_pct": 100, "peak_hours": ["12:00-14:00"], "congestion_level": "extreme", "recommended_arrival_hours_before": 3, "estimated_queue_minutes": 40, "parking_availability": "none", "public_transport_load": "extreme", "alternative_routes": ["Northern Line to Oval Station", "Walk from Vauxhall (15 min)"]},
    {"_id": "crowd_metlife_sf", "venue_id": "metlife_stadium", "match_id": "fifa_sf_1", "predicted_attendance": 82000, "venue_capacity": 82500, "utilization_pct": 99, "peak_hours": ["18:00-21:00"], "congestion_level": "very_high", "recommended_arrival_hours_before": 3, "estimated_queue_minutes": 35, "parking_availability": "limited", "public_transport_load": "very_high", "alternative_routes": ["NJ Transit + Shuttle from Secaucus", "Ferry from Manhattan to Hoboken, bus"]},
    {"_id": "crowd_azteca_opening", "venue_id": "estadio_azteca", "match_id": "fifa_opening", "predicted_attendance": 87000, "venue_capacity": 87523, "utilization_pct": 99, "peak_hours": ["15:00-18:00"], "congestion_level": "extreme", "recommended_arrival_hours_before": 4, "estimated_queue_minutes": 50, "parking_availability": "moderate", "public_transport_load": "extreme", "alternative_routes": ["Metro Line 2 to Tasqueña, then shuttle", "Metrobus Line 1"]},
]


async def seed_database(db):
    """Seed the MongoDB database with event data."""
    collections_data = {
        "events": EVENTS,
        "venues": VENUES,
        "matches": MATCHES,
        "businesses": BUSINESSES,
        "crowd_data": CROWD_DATA,
    }

    results = {}
    
    # Check if we can generate embeddings
    client = None
    if genai and os.getenv("GOOGLE_API_KEY"):
        try:
            client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            print("🚀 Generating Vector Embeddings for Semantic Search...")
        except Exception:
            pass

    for collection_name, data in collections_data.items():
        collection = db[collection_name]
        # Clear existing data
        await collection.delete_many({})
        # Insert new data
        if data:
            # Generate embeddings for venues and matches if client exists
            if client and collection_name in ["venues", "matches"]:
                for item in data:
                    text_to_embed = ""
                    if collection_name == "venues":
                        text_to_embed = f"Venue {item['name']} located in {item['city']}, {item['country']}. " \
                                      f"Capacity is {item.get('capacity', 'unknown')}. " \
                                      f"Transport options: {', '.join(item.get('transport', []))}. " \
                                      f"Nearby attractions: {', '.join(item.get('nearby_attractions', []))}."
                    elif collection_name == "matches":
                        text_to_embed = f"Match between {' and '.join(item.get('teams', []))} " \
                                      f"for {item.get('round', '')}. " \
                                      f"Significance: {item.get('significance', '')}. " \
                                      f"Expected attendance: {item.get('expected_attendance', '')}."
                    
                    try:
                        resp = client.models.embed_content(
                            model="gemini-embedding-2", 
                            contents=text_to_embed
                        )
                        # Depending on SDK version, embeddings could be in resp.embeddings[0].values
                        # For genai 2.8.0, it is usually a list of embeddings.
                        if hasattr(resp, 'embeddings') and resp.embeddings:
                            item['embedding'] = resp.embeddings[0].values
                        else:
                            # Fallback if structure differs
                            pass
                    except Exception as e:
                        print(f"Failed to embed item {item.get('name') or item.get('_id')}: {e}")

            await collection.insert_many(data)
        results[collection_name] = len(data)

    # Create indexes for performance
    await db["venues"].create_index("event_id")
    await db["matches"].create_index("event_id")
    await db["matches"].create_index("venue_id")
    await db["businesses"].create_index("venue_id")
    await db["crowd_data"].create_index("venue_id")
    await db["crowd_data"].create_index("match_id")
    await db["itineraries"].create_index("fan_id")
    await db["fans"].create_index("event_id")

    return results
