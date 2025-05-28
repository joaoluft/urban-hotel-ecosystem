from fastapi import FastAPI
from .modules import external_router

external_app = FastAPI(
    title="Urban Hotel - External Gateway",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json"
)

external_app.include_router(external_router)