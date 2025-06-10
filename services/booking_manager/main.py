from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .modules import api_router
from .core.lifespan import lifespan

app = FastAPI(title="Urban Hotel - Booking Manager", lifespan=lifespan)

app.include_router(api_router)

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")

@app.get("/health", include_in_schema=False)
async def health():
    return "ok"
