"""
TurfGrid AI — FastAPI Backend

Main application serving the multi-agent API for global sporting event management.
"""
import asyncio
import json
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.data.seed_data import seed_database

# ─── MongoDB Client ──────────────────────────────────────────────────────────

mongo_client = None
db = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    global mongo_client, db
    # Startup
    try:
        mongo_client = AsyncIOMotorClient(settings.MONGODB_URI)
        db = mongo_client[settings.MONGODB_DB]
        # Test connection
        await mongo_client.admin.command("ping")
        print("[OK] Connected to MongoDB Atlas")
        
        # Drop the old incorrect index if it exists
        try:
            await db["operational_alerts"].drop_index("venue_name_1_severity_1")
            print("[OK] Dropped incorrect severity index")
        except Exception:
            pass

        # Create unique compound index for alerts to prevent duplicates of the same type
        await db["operational_alerts"].create_index(
            [("venue_name", 1), ("alert_type", 1)],
            unique=True
        )
        # Create TTL index to expire alerts after 24 hours (86400 seconds)
        await db["operational_alerts"].create_index(
            "expires_at",
            expireAfterSeconds=86400
        )
        print("[OK] MongoDB Indexes ensured")
    except Exception as e:
        print(f"[WARN] MongoDB connection failed: {e}")
        print("   Running without database -- using in-memory seed data")
        db = None

    yield

    # Shutdown
    if mongo_client:
        mongo_client.close()
        print("[INFO] MongoDB connection closed")


# ─── FastAPI App ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="TurfGrid AI",
    description="Multi-agent platform for global sporting event management",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for hackathon demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request/Response Models ─────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    session_id: str = ""


class ChatResponse(BaseModel):
    response: str
    session_id: str
    agent_used: str = ""
    agent_steps: list = []


# ─── Agent Runner ─────────────────────────────────────────────────────────────

async def run_agent(message: str, session_id: str) -> dict:
    """Run the TurfGrid AI agent with a user message."""
    try:
        from google.adk.agents import LlmAgent
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        from google.genai import types

        from app.agents.orchestrator import root_agent

        session_service = InMemorySessionService()

        runner = Runner(
            agent=root_agent,
            app_name="turfgrid_ai",
            session_service=session_service,
        )

        session = await session_service.create_session(
            app_name="turfgrid_ai",
            user_id="user_" + (session_id or str(uuid.uuid4())[:8]),
        )

        user_message = types.Content(
            role="user",
            parts=[types.Part(text=message)]
        )

        response_text = ""
        agent_name = ""
        agent_steps = []

        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=user_message,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text
                    # Capture tool calls for transparency
                    if hasattr(part, 'function_call') and part.function_call:
                        func_name = part.function_call.name
                        agent_steps.append({
                            "agent": event.author if hasattr(event, 'author') and event.author else "Agent",
                            "action": f"Calling {func_name}()",
                            "status": "done"
                        })
                        
                        # --- MULTI-AGENT WORKFLOW TRIGGER ---
                        if func_name == "save_itinerary":
                            import asyncio
                            print("[WORKFLOW] save_itinerary detected. Triggering Business Agent in background.")
                            asyncio.create_task(run_agent(
                                "A new fan itinerary was just saved. Automatically generate a staffing plan for a cafe near the venue. Assume normal staff is 4.", 
                                "system_workflow_bot"
                            ))
                    if hasattr(part, 'function_response') and part.function_response:
                        agent_steps.append({
                            "agent": event.author if hasattr(event, 'author') and event.author else "Agent",
                            "action": f"Tool returned results",
                            "status": "done"
                        })
            if hasattr(event, 'author') and event.author:
                if event.author != agent_name:
                    agent_steps.append({
                        "agent": event.author,
                        "action": f"Activated",
                        "status": "done"
                    })
                agent_name = event.author

        return {
            "response": response_text or "I'm processing your request. Could you provide more details?",
            "session_id": session_id or session.id,
            "agent_used": agent_name,
            "agent_steps": agent_steps
        }

    except ImportError as e:
        # Fallback if ADK not installed — use direct Gemini
        return await run_fallback_agent(message, session_id)
    except Exception as e:
        print(f"Agent error: {e}")
        return await run_fallback_agent(message, session_id)


async def run_fallback_agent(message: str, session_id: str) -> dict:
    """Fallback agent using direct Gemini API when ADK is unavailable."""
    try:
        from google import genai

        client = genai.Client(api_key=settings.GOOGLE_API_KEY)

        # Import tools to use directly
        from app.tools.fan_tools import search_matches, list_venues, get_event_info
        from app.tools.crowd_tools import get_crowd_forecast
        from app.tools.business_tools import predict_match_day_demand
        from app.data.seed_data import EVENTS, VENUES, MATCHES

        # Build context
        events_summary = "\n".join([f"- {e['name']}: {e['start_date']} to {e['end_date']}, {e['host_countries']}" for e in EVENTS])
        venues_summary = "\n".join([f"- {v['name']} ({v['city']}, {v['country']}) — capacity {v['capacity']}" for v in VENUES[:10]])

        system_prompt = f"""You are TurfGrid AI, a multi-agent platform for managing global sporting events.

CURRENT EVENTS:
{events_summary}

SAMPLE VENUES:
{venues_summary}

You help fans plan travel, businesses prepare for match days, predict crowd congestion, and manage event operations.

Be specific with data, enthusiastic about sports, and actionable in your advice. Use the event data provided."""

        # Try tool-based approach
        msg_lower = message.lower()
        tool_context = ""

        if any(w in msg_lower for w in ["match", "schedule", "game", "play", "fixture"]):
            if "icc" in msg_lower or "cricket" in msg_lower or "t20" in msg_lower:
                result = search_matches(event_id="icc_wt20_2026")
            elif "fifa" in msg_lower or "football" in msg_lower or "soccer" in msg_lower or "world cup" in msg_lower:
                result = search_matches(event_id="fifa_wc_2026")
            else:
                result = search_matches()
            tool_context = f"\n\nRELEVANT MATCH DATA:\n{json.dumps(result, indent=2, default=str)}"

        if any(w in msg_lower for w in ["venue", "stadium", "ground", "where"]):
            if "icc" in msg_lower or "cricket" in msg_lower:
                result = list_venues(event_id="icc_wt20_2026")
            elif "fifa" in msg_lower or "football" in msg_lower:
                result = list_venues(event_id="fifa_wc_2026")
            else:
                result = list_venues()
            tool_context += f"\n\nVENUE DATA:\n{json.dumps(result, indent=2, default=str)}"

        if any(w in msg_lower for w in ["crowd", "congestion", "busy", "queue", "arrive"]):
            result = get_crowd_forecast()
            tool_context += f"\n\nCROWD DATA:\n{json.dumps(result, indent=2, default=str)}"

        if any(w in msg_lower for w in ["business", "restaurant", "prepare", "staff", "demand"]):
            for vid in ["lords", "metlife_stadium", "edgbaston"]:
                result = predict_match_day_demand(venue_id=vid)
                if result.get("predictions"):
                    tool_context += f"\n\nBUSINESS DATA ({vid}):\n{json.dumps(result, indent=2, default=str)}"
                    break

        # Dynamic City Extraction for all ICC and FIFA venues
        detected_iata = "JFK" # Default
        detected_city = "NYC" # Default
        
        city_mappings = {
            "LHR": ["london", "lord's", "lords", "oval", "uk", "england"],
            "BHX": ["birmingham", "edgbaston"],
            "MAN": ["manchester", "old trafford"],
            "JFK": ["new york", "east rutherford", "metlife", "usa", "us", "united states"],
            "LAX": ["los angeles", "la", "inglewood", "sofi"],
            "MEX": ["mexico", "azteca", "mexico city"]
        }
        
        hotel_mappings = {"LHR": "LON", "BHX": "BHX", "MAN": "MAN", "JFK": "NYC", "LAX": "LAX", "MEX": "MEX"}
        
        for iata, keywords in city_mappings.items():
            if any(k in msg_lower for k in keywords):
                detected_iata = iata
                detected_city = hotel_mappings[iata]
                break

        if any(w in msg_lower for w in ["flight", "fly", "airplane"]):
            from app.tools.fan_tools import search_live_flights
            result = search_live_flights(origin_iata="ANY", destination_iata=detected_iata, departure_date="2026-06-15")
            tool_context += f"\n\nLIVE FLIGHT DATA (To {detected_iata}):\n{json.dumps(result, indent=2, default=str)}"

        if any(w in msg_lower for w in ["hotel", "stay", "accommodation"]):
            from app.tools.fan_tools import search_live_hotels
            result = search_live_hotels(city_code=detected_city, check_in_date="2026-06-15", check_out_date="2026-06-20")
            tool_context += f"\n\nLIVE HOTEL DATA ({detected_city}):\n{json.dumps(result, indent=2, default=str)}"

        full_prompt = system_prompt + tool_context + f"\n\nUser query: {message}"

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=full_prompt
        )

        # Build synthetic agent steps for fallback mode
        fallback_steps = [{"agent": "TurfGridAI", "action": "Orchestrator activated", "status": "done"}]
        if tool_context:
            fallback_steps.append({"agent": "TurfGridAI", "action": "Data tools queried", "status": "done"})
        fallback_steps.append({"agent": "TurfGridAI", "action": "Response generated", "status": "done"})

        return {
            "response": response.text,
            "session_id": session_id or str(uuid.uuid4())[:8],
            "agent_used": "TurfGridAI (direct)",
            "agent_steps": fallback_steps
        }

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            # FALLBACK TO GROQ: If Gemini quota is hit, try Groq
            import os
            groq_key = os.getenv("GROQ_API_KEY")
            
            if groq_key:
                try:
                    from groq import Groq
                    groq_client = Groq(api_key=groq_key)
                    
                    from app.tools.action_tools import issue_operational_alert, create_staffing_plan, save_itinerary

                    groq_messages = [
                        {"role": "system", "content": system_prompt + tool_context},
                        {"role": "user", "content": message}
                    ]

                    groq_tools = [
                        {
                            "type": "function",
                            "function": {
                                "name": "issue_operational_alert",
                                "description": "Issue an operational alert for a venue.",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "venue_name": {"type": "string"},
                                        "alert_type": {"type": "string", "enum": ["crowd", "security", "medical", "weather", "facility", "transport"]},
                                        "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                                        "message": {"type": "string"},
                                        "recommended_actions": {"type": "string"}
                                    },
                                    "required": ["venue_name", "alert_type", "severity", "message"]
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "create_staffing_plan",
                                "description": "Create and save a staffing plan for a local business.",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "business_name": {"type": "string"},
                                        "business_type": {"type": "string"},
                                        "venue_name": {"type": "string"},
                                        "match_description": {"type": "string"},
                                        "match_date": {"type": "string"},
                                        "normal_staff": {"type": "integer"},
                                        "recommended_staff": {"type": "integer"},
                                        "peak_hours": {"type": "string"},
                                        "inventory_notes": {"type": "string"},
                                        "special_preparations": {"type": "string"}
                                    },
                                    "required": ["business_name", "business_type", "venue_name", "match_description", "match_date", "normal_staff", "recommended_staff"]
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "save_itinerary",
                                "description": "Save a confirmed travel itinerary.",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "user_name": {"type": "string"},
                                        "event": {"type": "string"},
                                        "origin": {"type": "string"},
                                        "destination_city": {"type": "string"},
                                        "matches": {"type": "string"},
                                        "hotel": {"type": "string"},
                                        "transport_route": {"type": "string"},
                                        "budget": {"type": "string"},
                                        "notes": {"type": "string"}
                                    },
                                    "required": ["user_name", "event", "origin", "destination_city", "matches"]
                                }
                            }
                        }
                    ]

                    chat_completion = groq_client.chat.completions.create(
                        messages=groq_messages,
                        model="llama-3.3-70b-versatile",
                        temperature=0.7,
                        tools=groq_tools,
                        tool_choice="auto"
                    )

                    response_message = chat_completion.choices[0].message
                    final_response_text = response_message.content or "I have processed your request and updated the system."
                    
                    agent_steps = [
                        {"agent": "TurfGridAI", "action": "Gemini 429 Limit Hit", "status": "warning"},
                        {"agent": "TurfGridAI", "action": "Failover to Groq Llama-3", "status": "done"}
                    ]

                    # Handle Groq tool calls!
                    if response_message.tool_calls:
                        for tool_call in response_message.tool_calls:
                            func_name = tool_call.function.name
                            args = json.loads(tool_call.function.arguments)
                            
                            agent_steps.append({"agent": "GroqFallback", "action": f"Calling {func_name}()", "status": "done"})
                            
                            try:
                                if func_name == "issue_operational_alert":
                                    result = await issue_operational_alert(**args)
                                elif func_name == "create_staffing_plan":
                                    result = await create_staffing_plan(**args)
                                elif func_name == "save_itinerary":
                                    result = await save_itinerary(**args)
                                    # --- MULTI-AGENT WORKFLOW TRIGGER (Fallback) ---
                                    import asyncio
                                    print("[WORKFLOW] save_itinerary detected in Fallback. Triggering Business Agent in background.")
                                    asyncio.create_task(run_fallback_agent(
                                        "A new fan itinerary was just saved. Automatically generate a staffing plan for a cafe near the venue. Assume normal staff is 4.", 
                                        "system_workflow_bot"
                                    ))
                                
                                agent_steps.append({"agent": "GroqFallback", "action": "MongoDB Write Successful", "status": "done"})
                                final_response_text += f"\n\n🚨 *{func_name} was successfully executed by the backup AI! Dashboard updated.*"
                            except Exception as tool_err:
                                agent_steps.append({"agent": "GroqFallback", "action": f"Tool failed: {str(tool_err)}", "status": "warning"})

                    agent_steps.append({"agent": "TurfGridAI", "action": "Response generated via Groq", "status": "done"})

                    return {
                        "response": final_response_text,
                        "session_id": session_id or str(uuid.uuid4())[:8],
                        "agent_used": "TurfGridAI (Groq Failover - Llama3)",
                        "agent_steps": agent_steps
                    }
                except Exception as groq_err:
                    return {
                        "response": f"Gemini Quota Exceeded. Groq Failover also failed: {str(groq_err)}",
                        "session_id": session_id or str(uuid.uuid4())[:8],
                        "agent_used": "error"
                    }
            else:
                # MOCK MODE if no Groq key
                return {
                    "response": "I see you're asking about our events! I've checked the latest data: The match is completely sold out, but public transport via the Metro is currently running smoothly with no delays. The weather at the venue is clear. (Note: Gemini Quota Exceeded. Add GROQ_API_KEY to .env for AI fallback!)",
                    "session_id": session_id or str(uuid.uuid4())[:8],
                    "agent_used": "TurfGridAI (Mock Mode - Quota Exceeded)"
                }
        
        return {
            "response": f"I apologize, but I'm having trouble connecting to my AI backend. Error: {error_msg}. Please ensure your GOOGLE_API_KEY is set correctly in the .env file.",
            "session_id": session_id or str(uuid.uuid4())[:8],
            "agent_used": "error"
        }


# ─── API Routes ───────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "name": "TurfGrid AI",
        "version": "1.0.0",
        "status": "running",
        "description": "Multi-agent platform for global sporting event management",
        "events": [
            "FIFA World Cup 2026",
            "ICC Women's T20 World Cup 2026"
        ]
    }


@app.get("/api/health")
async def health():
    """Detailed health check."""
    mongo_status = "connected"
    error_msg = None
    if db is not None:
        try:
            await mongo_client.admin.command("ping")
        except Exception as e:
            mongo_status = "disconnected"
            error_msg = str(e)
    else:
        # Check if it failed during startup lifespan
        if settings.MONGODB_URI and "localhost" not in settings.MONGODB_URI:
            mongo_status = "connection_failed"
            try:
                # Attempt to ping right now to catch the exact error
                temp_client = AsyncIOMotorClient(settings.MONGODB_URI, serverSelectionTimeoutMS=2000)
                await temp_client.admin.command("ping")
                mongo_status = "connected_now"
            except Exception as e:
                error_msg = str(e)
        else:
            mongo_status = "not_configured"

    return {
        "status": "healthy",
        "mongodb": mongo_status,
        "mongodb_error": error_msg,
        "mongodb_uri_set": bool(settings.MONGODB_URI and "localhost" not in settings.MONGODB_URI),
        "gemini_configured": bool(settings.GOOGLE_API_KEY),
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to TurfGrid AI."""
    result = await run_agent(request.message, request.session_id)
    return ChatResponse(**result)


@app.websocket("/api/chat/stream")
async def chat_stream(websocket: WebSocket):
    """WebSocket endpoint for streaming chat responses."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            message = message_data.get("message", "")
            session_id = message_data.get("session_id", "")

            result = await run_agent(message, session_id)

            await websocket.send_text(json.dumps(result))
    except WebSocketDisconnect:
        pass


@app.post("/api/seed")
async def seed_data():
    """Seed the MongoDB database with event data."""
    if db is None:
        return JSONResponse(
            status_code=503,
            content={"error": "MongoDB not connected. Set MONGODB_URI in .env"}
        )
    try:
        results = await seed_database(db)
        return {"status": "success", "collections_seeded": results}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Seeding failed: {str(e)}"}
        )


@app.get("/api/events")
async def get_events():
    """Get all events."""
    from app.data.seed_data import EVENTS
    return {"events": EVENTS}


@app.get("/api/events/{event_id}")
async def get_event(event_id: str):
    """Get a specific event."""
    from app.data.seed_data import EVENTS
    event = next((e for e in EVENTS if e["_id"] == event_id), None)
    if not event:
        return JSONResponse(status_code=404, content={"error": "Event not found"})
    return event


@app.get("/api/venues")
async def get_venues(event_id: str = ""):
    """Get venues, optionally filtered by event."""
    from app.data.seed_data import VENUES
    venues = VENUES
    if event_id:
        venues = [v for v in venues if v["event_id"] == event_id]
    return {"venues": venues, "count": len(venues)}


@app.get("/api/matches")
async def get_matches(event_id: str = ""):
    """Get matches, optionally filtered by event."""
    from app.data.seed_data import MATCHES, VENUES
    matches = MATCHES
    if event_id:
        matches = [m for m in matches if m["event_id"] == event_id]

    # Enrich with venue names
    enriched = []
    for m in matches:
        venue = next((v for v in VENUES if v["_id"] == m["venue_id"]), {})
        enriched.append({**m, "venue_name": venue.get("name", ""), "venue_city": venue.get("city", "")})

    return {"matches": enriched, "count": len(enriched)}


@app.get("/api/crowd/{venue_id}")
async def get_crowd(venue_id: str):
    """Get crowd forecasts for a venue."""
    from app.tools.crowd_tools import get_crowd_forecast
    return get_crowd_forecast(venue_id=venue_id)


@app.get("/api/businesses/{venue_id}")
async def get_businesses(venue_id: str):
    """Get businesses near a venue."""
    from app.tools.fan_tools import get_nearby_businesses
    return get_nearby_businesses(venue_id=venue_id)


@app.get("/api/weather/{venue_id}")
async def api_get_weather(venue_id: str):
    """Get live weather for a venue."""
    from app.tools.crowd_tools import get_live_weather
    return get_live_weather(venue_id=venue_id)


@app.get("/api/distance")
async def api_get_distance(origin: str, venue_id: str):
    """Get live travel distance to a venue."""
    from app.tools.fan_tools import calculate_live_travel_time
    return calculate_live_travel_time(origin=origin, venue_id=venue_id)


# ─── v2.0: State-Altering Data Routes ────────────────────────────────────────

@app.get("/api/itineraries")
async def get_itineraries(city: str = None):
    """Get all saved fan itineraries."""
    if db is None:
        return {"itineraries": [], "count": 0}
    try:
        query = {"city": city} if city and city != "Global" else {}
        cursor = db["user_itineraries"].find(query).sort("created_at", -1).limit(50)
        results = await cursor.to_list(length=50)
        for r in results:
            r["_id"] = str(r["_id"])
        return {"itineraries": results, "count": len(results)}
    except Exception as e:
        return {"itineraries": [], "count": 0, "error": str(e)}


@app.get("/api/staffing-plans")
async def get_staffing_plans(city: str = None):
    """Get all active staffing plans."""
    if db is None:
        return {"plans": [], "count": 0}
    try:
        query = {"city": city} if city and city != "Global" else {}
        cursor = db["staffing_plans"].find(query).sort("created_at", -1).limit(50)
        results = await cursor.to_list(length=50)
        for r in results:
            r["_id"] = str(r["_id"])
        return {"plans": results, "count": len(results)}
    except Exception as e:
        return {"plans": [], "count": 0, "error": str(e)}


@app.get("/api/alerts")
async def get_alerts(city: str = None):
    """Get all operational alerts."""
    if db is None:
        return {"alerts": [], "count": 0}
    try:
        query = {"city": city} if city and city != "Global" else {}
        cursor = db["operational_alerts"].find(query).sort("created_at", -1).limit(50)
        results = await cursor.to_list(length=50)
        for r in results:
            r["_id"] = str(r["_id"])
        return {"alerts": results, "count": len(results)}
    except Exception as e:
        return {"alerts": [], "count": 0, "error": str(e)}

@app.get("/api/analytics")
async def get_analytics(city: str = None):
    """Get historical analytics via MongoDB aggregation."""
    if db is None:
        return {"error": "MongoDB not connected"}
    try:
        match_stage = {"$match": {"city": city}} if city and city != "Global" else {"$match": {}}
        
        # 1. Alert Frequency per Venue
        alerts_pipeline = [
            match_stage,
            {"$group": {"_id": "$venue_name", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        alerts_cursor = db["operational_alerts"].aggregate(alerts_pipeline)
        alerts_by_venue = await alerts_cursor.to_list(length=10)
        
        # 2. Staffing Impact
        staffing_pipeline = [
            match_stage,
            {"$group": {
                "_id": "$business_type", 
                "total_extra_staff": {"$sum": "$additional_staff_needed"},
                "plans_count": {"$sum": 1}
            }},
            {"$sort": {"total_extra_staff": -1}}
        ]
        staffing_cursor = db["staffing_plans"].aggregate(staffing_pipeline)
        staffing_impact = await staffing_cursor.to_list(length=10)
        
        # 3. Popular Itinerary Destinations
        itinerary_pipeline = [
            match_stage,
            {"$group": {"_id": "$destination_city", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        itinerary_cursor = db["user_itineraries"].aggregate(itinerary_pipeline)
        popular_destinations = await itinerary_cursor.to_list(length=10)

        return {
            "alerts_by_venue": [{"venue": r["_id"], "count": r["count"]} for r in alerts_by_venue if r["_id"]],
            "staffing_impact": [{"type": r["_id"], "extra_staff": r["total_extra_staff"]} for r in staffing_impact if r["_id"]],
            "popular_destinations": [{"city": r["_id"], "count": r["count"]} for r in popular_destinations if r["_id"]]
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/user-profile/{user_id}")
async def get_user_profile_route(user_id: str):
    """Get a user's stored preferences."""
    if db is None:
        return {"preferences": {}, "status": "no_db"}
    try:
        profile = await db["user_profiles"].find_one({"_id": user_id})
        if profile:
            profile["_id"] = str(profile["_id"])
            return profile
        return {"preferences": {}, "status": "new_user"}
    except Exception as e:
        return {"preferences": {}, "error": str(e)}
