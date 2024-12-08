import asyncio
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

    async def connect_to_rabbitmq(self, retries=5, delay=3):
        """Conectar a RabbitMQ con reintentos."""
        for attempt in range(retries):
            try:
                logger.info("Attempting to connect to RabbitMQ...")
                await self.container.rabbitmq().connect()
                logger.info("Successfully connected to RabbitMQ.")
                return True
            except Exception as e:
                logger.error(f"Error connecting to RabbitMQ (attempt {attempt + 1}): {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(delay)
                else:
                    return False

    async def start_consumers(self):
        """Iniciar consumidores de RabbitMQ."""
        if await self.connect_to_rabbitmq():
            try:
                consumer = self.container.rabbitmq_consumer()
                await consumer.consume_messages(queue_name=settings.characters_queue)
                logger.info("Consumers started successfully.")
            except Exception as e:
                logger.error(f"Error starting consumers: {e}")

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        """Lógica de inicialización y cierre de la aplicación."""
        try:
            logger.info("Application startup...")
            await self.start_consumers()
            yield
        finally:
            logger.info("Application shutdown...")
            try:
                await self.container.rabbitmq().close()
                logger.info("RabbitMQ connection closed.")
            except Exception as e:
                logger.error(f"Error closing RabbitMQ connection: {e}")

    def create_app(self):
        """Crear la instancia de FastAPI."""
        app = FastAPI(
            title=self.project_name,
            openapi_url=f"{self.api_prefix}/openapi.json",
            version="0.0.1",
            lifespan=self.lifespan,
        )

        @app.exception_handler(BaseError)
        async def base_error_handler(request: Request, exc: BaseError):
            logger.error(f"Error encountered: {exc}")
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


# Crear la instancia de la aplicación
app_factory = AppFactory(
    settings.project_name, settings.prefix, settings.backend_cors_origins
)
app = app_factory.create_app()

