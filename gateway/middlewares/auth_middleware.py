from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jwt import decode, ExpiredSignatureError, InvalidTokenError

from gateway.core.config import Settings

EXCLUDED_PATHS = ["/", "/docs", "/openapi.json", "/redoc"]

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, settings: Settings):
        super().__init__(app)
        self.settings = settings

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return JSONResponse(status_code=200, content={}, headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
            })
    
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)
        
        if request.url.path.startswith("/external"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing or invalid token"})

        token = auth_header.removeprefix("Bearer ").strip()

        try:
            payload = decode(
                token, 
                self.settings.jwt_secret, 
                algorithms=[self.settings.jwt_algorithm], 
                issuer=self.settings.jwt_issuer
            )
            request.state.user = payload
        except (ExpiredSignatureError, InvalidTokenError):
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})
        except Exception:
            return JSONResponse(status_code=401, content={"detail": "Token validation error"})

        return await call_next(request)