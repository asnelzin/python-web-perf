import json
import os

from aiohttp import web

if os.getenv('USE_ASYNCPG', False):
    from async_db_asyncpg import get_row
else:
    from async_db import get_row


async def handle(request):
    a, b = await get_row()
    return web.Response(text=json.dumps({"a": str(a).zfill(10), "b": b}))


app = web.Application()
app.add_routes([web.get('/test', handle)])
