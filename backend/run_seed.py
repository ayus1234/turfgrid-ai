import asyncio
import os
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()
from app.data.seed_data import seed_database

async def run():
    print("Connecting to MongoDB Atlas...")
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGODB_URI'))
    db = client[os.getenv('MONGODB_DB', 'eventsphere')]
    print("Starting seed and embedding generation...")
    res = await seed_database(db)
    print("Successfully seeded:", res)

asyncio.run(run())
