import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()
db = AsyncIOMotorClient(os.getenv('MONGODB_URI'))[os.getenv('MONGODB_DB')]

async def r():
    print(await db['operational_alerts'].find_one({}))
    print(await db['staffing_plans'].find_one({}))
    print(await db['user_itineraries'].find_one({}))

asyncio.run(r())
