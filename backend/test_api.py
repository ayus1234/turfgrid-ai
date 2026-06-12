import asyncio
from app.main import lifespan, app, get_analytics, get_alerts, get_staffing_plans
import sys

async def test_endpoints():
    print("Initializing app context...")
    async with lifespan(app):
        print("\n--- Testing /api/alerts ---")
        alerts = await get_alerts()
        print(f"Alerts found: {alerts.get('count')}")
        
        print("\n--- Testing /api/staffing-plans ---")
        plans = await get_staffing_plans()
        print(f"Plans found: {plans.get('count')}")
        
        print("\n--- Testing /api/analytics ---")
        analytics = await get_analytics()
        print(f"Analytics Data: {analytics}")
        
        if "error" in analytics:
            print("FAILED: Analytics returned an error")
            sys.exit(1)
        print("\n✅ All endpoints tested successfully!")

if __name__ == "__main__":
    asyncio.run(test_endpoints())
