from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .core.config import Settings
from .modules import api_router
from .middlewares.auth_middleware import AuthMiddleware
from .external import external_app

load_dotenv()

config = Settings()
security = HTTPBearer()

app = FastAPI(
    title="Urban Hotel - Gateway",
    dependencies=[Depends(security)],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    AuthMiddleware,
    settings=config
)

app.include_router(api_router)

app.mount("/external", external_app)

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")

@app.get("/health", include_in_schema=False)
async def health():
    return "ok"
