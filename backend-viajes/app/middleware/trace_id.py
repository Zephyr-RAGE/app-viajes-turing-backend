import time
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging_config import logger


class TraceIDMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next) -> Response:

        trace_id = str(uuid4())
        request.state.trace_id = trace_id

        start_time = time.perf_counter()

        try:
            response = await call_next(request)

            process_time = time.perf_counter() - start_time

            response.headers["X-Trace-ID"] = trace_id

            response.headers["X-Process-Time"] = (
                f"{process_time:.4f}"
            )

            logger.info(
                "Request completed | trace_id=%s | method=%s | "
                "path=%s | status_code=%s | duration=%.4fs",
                trace_id,
                request.method,
                request.url.path,
                response.status_code,
                process_time,
            )

            return response

        except Exception:
            process_time = time.perf_counter() - start_time

            logger.exception(
                "Request failed | trace_id=%s | method=%s | "
                "path=%s | duration=%.4fs",
                trace_id,
                request.method,
                request.url.path,
                process_time,
            )

            raise