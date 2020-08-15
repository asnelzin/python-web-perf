import json
import multiprocessing
import os
import signal

from aiohttp import web

if os.getenv('USE_ASYNCPG', False):
    from async_db_asyncpg import get_row
else:
    from async_db import get_row


async def handle(_):
    a, b = get_row()
    return web.Response(text=json.dumps({"a": str(a).zfill(10), "b": b}))


def run_server():
    app = web.Application()
    app.add_routes([web.get('/test', handle)])
    web.run_app(
        app,
        host='localhost', port=8081, reuse_port=True,
        print=lambda _: None
    )


def serve(workers: int = 1) -> None:
    processes = []

    def sig_handler(sig, frame):
        for proc in processes:
            os.kill(proc.pid, signal.SIGTERM)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    mp = multiprocessing.get_context('fork')

    for _ in range(workers):
        proc = mp.Process(target=run_server, daemon=True)
        proc.start()
        processes.append(proc)

    for proc in processes:
        proc.join()

    for proc in processes:
        proc.terminate()


if __name__ == '__main__':
    serve(workers=os.getenv('PWPWORKERS', 4))
