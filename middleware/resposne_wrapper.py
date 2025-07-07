import json

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.models.response_model import ResponseModel


class ResponseWrapperMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Only wrap JSON
        if response.media_type != "application/json":
            return response

        raw_body = b""
        async for chunk in response.body_iterator:
            raw_body += chunk

        try:
            payload = json.loads(raw_body)
        except Exception:
            return response

        # If already wrapped, skip wrapping
        if isinstance(payload, dict) and {"status_code", "message", "data"}.issubset(payload):
            return JSONResponse(content=payload, status_code=payload["status_code"])

        # Check if user returned a custom status_code in payload
        status_code = payload.pop("status_code", response.status_code)
        message =  payload.pop("message", "Success" if 200 <= status_code < 300 else "Error")
        wrapped = ResponseModel(
            status_code=status_code,
            message=message,
            data=payload
        )

        return JSONResponse(content=wrapped.dict(), status_code=status_code)
