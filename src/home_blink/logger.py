import logging
import os


def get_logger(name: str):
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

    logger = logging.getLogger(name)

    return logger
