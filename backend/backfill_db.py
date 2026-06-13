import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()
db = AsyncIOMotorClient(os.getenv('MONGODB_URI'))[os.getenv('MONGODB_DB')]

VENUE_CITY_MAP = {
    "wembley": "London",
    "lord's": "London",
    "the oval": "London",
    "tottenham": "London",
    "metlife": "New York",
    "edgbaston": "Birmingham",
    "old trafford": "Manchester",
    "sofi": "Los Angeles",
    "azteca": "Mexico City"
}

async def run():
    # Update Staffing Plans
    cursor = db['staffing_plans'].find({"city": {"$exists": False}})
    async for plan in cursor:
        venue = plan.get('venue_name', '').lower()
        city = "Global"
        for k, v in VENUE_CITY_MAP.items():
            if k in venue:
                city = v
                break
        print(f"Updating STP {plan['_id']} with city {city}")
        await db['staffing_plans'].update_one({"_id": plan['_id']}, {"$set": {"city": city}})

    # Update User Itineraries
    cursor = db['user_itineraries'].find({"city": {"$exists": False}})
    async for it in cursor:
        city = it.get('destination_city', 'Global')
        print(f"Updating ITN {it['_id']} with city {city}")
        await db['user_itineraries'].update_one({"_id": it['_id']}, {"$set": {"city": city}})

    # Update Operational Alerts
    cursor = db['operational_alerts'].find({"city": {"$exists": False}})
    async for alert in cursor:
        venue = alert.get('venue_name', '').lower()
        city = "Global"
        for k, v in VENUE_CITY_MAP.items():
            if k in venue:
                city = v
                break
        print(f"Updating ALT {alert['_id']} with city {city}")
        await db['operational_alerts'].update_one({"_id": alert['_id']}, {"$set": {"city": city}})

asyncio.run(run())
