import asyncio
from app.main import lifespan, app, db
from app.tools.action_tools import issue_operational_alert
from app.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

async def test_duplicates():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_DB]
    print("Clearing alerts collection...")
    await db["operational_alerts"].delete_many({})
    print("Cleared.")

    print("Initializing app context (This will ensure indexes are created)...")
    async with lifespan(app):
        print("\n--- Issuing First Alert ---")
        res1 = await issue_operational_alert(
            venue_name="Wembley Stadium",
            alert_type="crowd",
            severity="HIGH",
            message="Initial test alert for high crowd density.",
            recommended_actions="Deploy extra staff",
            city="London"
        )
        print("Result 1:", str(res1).encode('ascii', 'ignore').decode())
        
        print("\n--- Issuing Duplicate Alert (Same Venue & Severity) ---")
        res2 = await issue_operational_alert(
            venue_name="Wembley Stadium",
            alert_type="crowd",
            severity="HIGH",
            message="Secondary test alert trying to bypass constraints.",
            recommended_actions="Open more gates",
            city="London"
        )
        print("Result 2:", str(res2).encode('ascii', 'ignore').decode())

        print("\n--- Issuing Different Severity Alert (Same Venue) ---")
        res3 = await issue_operational_alert(
            venue_name="Wembley Stadium",
            alert_type="security",
            severity="CRITICAL",
            message="A completely different severity alert.",
            recommended_actions="Evacuate",
            city="London"
        )
        print("Result 3:", str(res3).encode('ascii', 'ignore').decode())
        
if __name__ == "__main__":
    asyncio.run(test_duplicates())
