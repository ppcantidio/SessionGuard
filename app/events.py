from app.logger import logger


async def startup_application() -> None:
    logger.info("Starting the application")


async def shutdown_application() -> None:
    logger.info("Shutting down the application")
