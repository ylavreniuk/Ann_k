import os
import asyncpg
from typing import Optional

DATABASE_URL = os.environ.get(
    'DATABASE_URL', 
    'postgresql://booking_user:booking_password@localhost:5432/booking_db'
)

class Database:
    pool: Optional[asyncpg.Pool] = None

db = Database()

async def create_pool():
    db.pool = await asyncpg.create_pool(DATABASE_URL)

async def close_pool():
    if db.pool:
        await db.pool.close()

async def get_db():
    if not db.pool:
        await create_pool()
    async with db.pool.acquire() as connection:
        yield connection