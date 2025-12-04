import contextvars
import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional

# Context variables for request tracing
trace_id_ctx = contextvars.ContextVar("trace_id", default=None)
conversation_id_ctx = contextvars.ContextVar("conversation_id", default=None)
consignee_scope_ctx = contextvars.ContextVar("consignee_scope", default=None)


class JSONFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings with context.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "trace_id": trace_id_ctx.get(),
            "conversation_id": conversation_id_ctx.get(),
            "consignee_scope": consignee_scope_ctx.get(),
        }

        # Add extra fields from record if available
        if hasattr(record, "extra_data"):
            log_record.update(record.extra_data)

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)


def setup_logger(name: str = "shipment_qna_bot", level: str = "INFO") -> logging.Logger:
    """
    Configures and returns a logger with JSON formatting.
    """
    logger = logging.getLogger(name)

    # clear existing handlers to avoid duplicates
    if logger.handlers:
        logger.handlers.clear()

    logger.setLevel(level.upper())

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)

    # Prevent propagation to root logger to avoid double logging if root is configured
    logger.propagate = False

    return logger


# Global logger instance
logger = setup_logger()
