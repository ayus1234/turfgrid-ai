"""
MongoDB MCP Server for TurfGrid AI
Exposes MongoDB tools via Model Context Protocol (MCP).
"""
import os
import asyncio
from mcp.server.fastmcp import FastMCP
from app.tools.fan_tools import semantic_search
from app.tools.action_tools import save_itinerary, create_staffing_plan, issue_operational_alert
from app.config import settings

# Initialize FastMCP Server
mcp = FastMCP("TurfGrid MongoDB Server")

@mcp.tool()
async def tool_semantic_search(query: str, search_type: str = "venues") -> dict:
    """Search for venues or matches using natural language semantic meaning and MongoDB Vector Search."""
    return await semantic_search(query, search_type)

@mcp.tool()
async def tool_save_itinerary(user_name: str, event: str, origin: str, destination_city: str, matches: str, hotel: str = "", transport_route: str = "", budget: str = "", notes: str = "") -> dict:
    """Save a confirmed travel itinerary to MongoDB."""
    return await save_itinerary(user_name, event, origin, destination_city, matches, hotel, transport_route, budget, notes)

@mcp.tool()
async def tool_create_staffing_plan(business_name: str, business_type: str, venue_name: str, match_description: str, match_date: str, normal_staff: int, recommended_staff: int, peak_hours: str = "", inventory_notes: str = "", special_preparations: str = "") -> dict:
    """Create and save a staffing plan for a local business to MongoDB."""
    return await create_staffing_plan(business_name, business_type, venue_name, match_description, match_date, normal_staff, recommended_staff, peak_hours, inventory_notes, special_preparations)

@mcp.tool()
async def tool_issue_operational_alert(venue_name: str, alert_type: str, severity: str, message: str, recommended_actions: str = "") -> dict:
    """Issue an operational alert for a venue to MongoDB."""
    return await issue_operational_alert(venue_name, alert_type, severity, message, recommended_actions)

def run():
    print("Starting MongoDB MCP Server...")
    mcp.run(transport="stdio")

if __name__ == "__main__":
    run()
