import asyncio

from aiohttp import ClientSession
from blinkpy.blinkpy import Blink

from config import CREDENTIALS
from logger import get_logger

logger = get_logger("home_blink.setup")


async def setup():
    async with ClientSession() as session:
        logger.info("Setting up Blink credentials and saving to %s", CREDENTIALS)

        blink = Blink(session=session)

        await blink.start()
        await blink.save(CREDENTIALS)

        logger.info("Success, updated %s with latest details", CREDENTIALS)


if __name__ == "__main__":
    asyncio.run(setup())
