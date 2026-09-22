import asyncio

from RunakMusic.command import commands  # noqa: F401  (registers all the handlers)
from RunakMusic.engine.bot import app, calls, userbot
from RunakMusic.engine.web import start_web_server


async def main():
    await start_web_server()
    await app.start()
    await userbot.start()
    await calls.start()
    print("Runak Music Bot is up.")
    await asyncio.Event().wait()


if __name__ == "__main__":
    # Not asyncio.run() — that always creates a brand-new event loop, but
    # the Client/PyTgCalls objects in engine.bot bound themselves to
    # whatever loop existed at import time. Reusing that same loop here
    # keeps everything on one loop; asyncio.run() would put them on two
    # different ones and raise "attached to a different loop".
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
