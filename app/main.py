from fastapi import FastAPI

from app import __version__, events
from app.logger import logger
from app.routers import health, v1


def add_events(app: FastAPI) -> None:
    logger.info("-> Adding event on startup: events.startup_application")
    app.add_event_handler("startup", events.startup_application)

    logger.info("-> Adding event on shutdown: events.shutdown_application")
    app.add_event_handler("shutdown", events.shutdown_application)


def add_routers(app: FastAPI) -> None:
    app.include_router(health.router)
    app.include_router(v1.group_router.router)
    app.include_router(v1.password_router.router)
    app.include_router(v1.permission_router.router)
    app.include_router(v1.session_router.router)
    app.include_router(v1.user_router.router)


def add_handlers(app: FastAPI) -> None:
    pass


def add_middlewares(app: FastAPI) -> None:
    pass


def criar_app() -> FastAPI:
    logger.info("-> Creating app")
    app = FastAPI(
        title=__version__.__title__,
        version=str(__version__.__version__),
        openapi_url="/v2/api-docs",
        redoc_url=None,
    )

    logger.info("-> Adding events")
    add_events(app)

    logger.info("-> Adding handlers")
    add_handlers(app)

    logger.info("-> Adding routers")
    add_routers(app)

    logger.info("-> Adding middlewares")
    add_middlewares(app)

    return app
