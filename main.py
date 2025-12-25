from asynctor.contrib.fastapi import register_aioredis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from sqlalchemy.pool import AsyncAdaptedQueuePool
from starlette.middleware.cors import CORSMiddleware


from app.api.v1.api import v1_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    default_response_class=ORJSONResponse,
)

register_aioredis(app, host=settings.REDIS_HOST, port=settings.REDIS_PORT)
app.mount("/media", StaticFiles(directory=get_settings().MEDIA_ROOT), name="media")
app.mount("/static", StaticFiles(directory=get_settings().STATIC_ROOT), name="static")
app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=str(settings.ASYNC_DATABASE_URI),
    engine_args={"echo": False, "poolclass": AsyncAdaptedQueuePool},
)
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(v1_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    from asynctor.contrib.fastapi import runserver
    runserver(app, port=settings.PORT, reload=settings.RELOAD)
