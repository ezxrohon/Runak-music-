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
    asyncio.run(main())
