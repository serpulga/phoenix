import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from phoenix.services.database import create_all
from phoenix.api.primes import router as primes_router
from phoenix.api.tasks import router as tasks_router
import settings


logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(levelname)s: %(message)s",
)


app = FastAPI(title="Phoenix Prime Number Calculator")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)


@app.on_event("startup")
async def initialize_db():
    await create_all()


# API routers
app.include_router(primes_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")


@app.get("/")
async def root():
    return ""


if __name__ == "__main__":
    port = settings.PORT
    workers = settings.WORKERS
    reload = settings.RELOAD

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=reload, workers=workers)
