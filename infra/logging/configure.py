import json
import logging
import sys
from contextvars import ContextVar
from datetime import UTC, datetime

log_context: ContextVar[dict[str, object] | None] = ContextVar(
    "log_context",
    default=None,
)


def set_log_context(**fields: object) -> None:
    current = log_context.get() or {}
    log_context.set({**current, **fields})


def clear_log_context() -> None:
    log_context.set(None)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        data = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "context": getattr(record, "context", {}),
        }

        if record.exc_info:
            data["exception"] = self.formatException(record.exc_info)

        return json.dumps(data, ensure_ascii=False, default=str)


def configure_logging() -> None:
    previous_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = previous_factory(*args, **kwargs)
        record.context = dict(log_context.get() or {})
        return record

    logging.setLogRecordFactory(record_factory)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler],
        force=True,
    )
