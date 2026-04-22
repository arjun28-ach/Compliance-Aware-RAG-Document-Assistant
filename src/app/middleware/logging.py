import time
from starlette.middleware.base import BaseHTTPMiddleware


class AuditLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration_ms = round((time.time() - start) * 1000, 2)

        print(
            f"[AUDIT] method={request.method} path={request.url.path} "
            f"status={response.status_code} latency_ms={duration_ms}"
        )
        return response