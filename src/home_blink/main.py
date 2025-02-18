import asyncio
import logging
import os
from asyncio import sleep

from aiohttp import ClientSession
from blinkpy.auth import Auth
from blinkpy.blinkpy import Blink
from blinkpy.helpers.util import json_load

CREDENTIALS = "credentials.json"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "log", "home-blink.log"
            ),
            mode="a",
        ),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("home_blink.main")


async def main():
    async with ClientSession() as session:
        blink = Blink(session=session)
        credentials = await json_load(CREDENTIALS)
        blink.auth = Auth(credentials, session=session)

        await blink.start()
        await blink.save(CREDENTIALS)

        for camera_name, camera in blink.cameras.items():
            logger.info("==== START Processing Camera: %s ====", camera_name)
            try:
                camera_attributes = camera.attributes

                logger.debug(
                    "Camera details for %s: Thumbnail=%s, Video=%s, Temperature=%s, Battery=%s, WiFi Signal=%s",
                    camera_name,
                    camera_attributes.get("thumbnail"),
                    camera_attributes.get("video"),
                    camera_attributes.get("temperature"),
                    camera_attributes.get("battery"),
                    camera_attributes.get("wifi_strength"),
                )

                logger.info("Taking a new picture using %s", camera_name)

                new_thumbnail = await camera.snap_picture()
                thumbnail_id = new_thumbnail.get("id")

                logger.info(
                    "Updating thumbnail for %s with ID: %s", camera_name, thumbnail_id
                )

                await camera.update_images(
                    {"thumbnail": thumbnail_id}, force_cache=True
                )

                logger.info("SUCCESS: Updated thumbnail for %s", camera_name)
            except Exception as e:
                logger.error(
                    "Error processing camera %s: %s", camera_name, e, exc_info=True
                )

            logger.info("==== END Processing Camera: %s ====", camera_name)

            await sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
