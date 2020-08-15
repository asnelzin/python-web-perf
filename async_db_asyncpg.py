import random
import asyncpg

pool = None


async def get_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(
            dns="dbname=test user=test password=test port=6432 host=127.0.0.1",
            min_size=1,
            max_size=4,
        )
    return pool


max_n = 1000_000 - 1


async def get_row():
    pool = await get_pool()
    async with pool.acquire() as conn:
        index = random.randint(1, max_n)
        row = await conn.fetchrow("select a, b from test where a = $1", index)
    return row['a'], row['b']

