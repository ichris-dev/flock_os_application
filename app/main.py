from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.db_connection import connect, disconnect
from app.api.auth import router as auth_router
from app.api.intelligence import router as intelligence_router


@asynccontextmanager
async def Lifespan(app: FastAPI):

    await connect()

    yield

    await disconnect()


def get_application() -> FastAPI:
    application = FastAPI(lifespan=Lifespan)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    application.include_router(auth_router, prefix="/auth", tags=["auth"])
    application.include_router(intelligence_router, prefix="/intelligence", tags=["intelligence"])
    return application


app = get_application()