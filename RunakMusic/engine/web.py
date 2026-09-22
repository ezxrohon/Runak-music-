"""A minimal HTTP server whose only job is to exist.

Render's Web Service type expects something listening on $PORT and will
health-check it; a Telegram bot has no HTTP traffic of its own, so this
gives Render something to ping while the actual bot runs in the same
process. Not needed if you deploy this as a Background Worker instead.
"""

import os

from aiohttp import web


async def _health(request: web.Request) -> web.Response:
    return web.json_response({"status": "ok", "bot": "Runak Music Bot"})


async def start_web_server() -> web.AppRunner:
    app = web.Application()
    app.router.add_get("/", _health)
    app.router.add_get("/health", _health)

    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Health server listening on 0.0.0.0:{port}")
    return runner
