from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import routers as v1_routers
from config import settings
from container import Container
from core.exceptions import BaseError
from logger_config import logger


class AppFactory:
    def __init__(self, project_name, api_prefix, backend_cors_origins=None):
        self.container = Container()
        self.project_name = project_name
        self.api_prefix = api_prefix
        self.backend_cors_origins = backend_cors_origins

    async def connect_to_rabbitmq(self):
        try:
            await self.container.rabbitmq().connect()
            return True
        except Exception as e:
            logger.error(f"Error connecting to RabbitMQ: {e}")
            return False

    # async def start_consumers(self):
    #     if await self.connect_to_rabbitmq():
    #         queue = self.container.rabbitmq_consumer()
    #         await queue.consume_messages(queue_name=settings.characters_queue)
    #         await queue.consume_messages(
    #             queue_name=constants.QUEUES["CHARACTERS"]
    #         )
    #
    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        await self.connect_to_rabbitmq()
        yield

    def create_app(self):
        app = FastAPI(
            title=self.project_name,
            openapi_url=f"{self.api_prefix}/openapi.json",
            version="0.0.1",
            lifespan=self.lifespan,
        )

        @app.exception_handler(BaseError)
        async def base_error_handler(request: Request, exc: BaseError):
            return JSONResponse(
                status_code=getattr(exc, "status_code", 500),
                content={
                    "code": exc.code,
                    "message": exc.message,
                    "description": exc.description
                },
            )

        @app.get("/")
        def status():
            return f"API: {self.project_name} is working"

        app.include_router(v1_routers, prefix=settings.prefix)

        if self.backend_cors_origins:
            app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in self.backend_cors_origins],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        return app

app_factory = AppFactory(
    settings.project_name, settings.prefix, settings.backend_cors_origins
)
app = app_factory.create_app()
