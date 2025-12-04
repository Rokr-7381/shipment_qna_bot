import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from shipment_qna_bot.logging.logger import (consignee_scope_ctx,
                                             conversation_id_ctx, logger,
                                             trace_id_ctx)


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware to initialize logging context for each request.
    """

    async def dispatch(self, request: Request, call_next):
        # Generate or extract trace_id
        trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
        token_trace = trace_id_ctx.set(trace_id)

        # Reset other context vars
        token_conv = conversation_id_ctx.set(None)
        token_scope = consignee_scope_ctx.set(None)

        logger.info(
            f"Incoming request: {request.method} {request.url.path}",
            extra={"extra_data": {"method": request.method, "path": request.url.path}},
        )

        try:
            response = await call_next(request)
            response.headers["X-Trace-ID"] = trace_id
            return response
        except Exception as e:
            logger.error(f"Request failed: {str(e)}", exc_info=True)
            raise e
        finally:
            # Clean up context
            trace_id_ctx.reset(token_trace)
            conversation_id_ctx.reset(token_conv)
            consignee_scope_ctx.reset(token_scope)
