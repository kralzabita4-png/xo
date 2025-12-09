from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
from HasiiMusic.logging import LOGGER

LOGGER.info("Connecting to your Mongo Database...")

try:
    _mongo_async_ = AsyncIOMotorClient(
        MONGO_DB_URI,
        serverSelectionTimeoutMS=5000
    )
    mongodb = _mongo_async_.Tune
    LOGGER.info("Connected to your Mongo Database ✅")
except Exception as e:
    LOGGER.error(f"Failed to connect to your Mongo Database ❌: {e}")
    exit(1)
