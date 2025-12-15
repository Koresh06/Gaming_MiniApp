import logging
from logging import StreamHandler


class ExtraFormatter(logging.Formatter):
    IGNORE_EXTRA_KEYS = {
        "taskName",
        "task", 
        "span_id",
        "trace_id",
        "client_addr",
        "scope",
    }

    def format(self, record: logging.LogRecord) -> str:
        standard = set(logging.makeLogRecord({}).__dict__.keys())

        extras = {
            key: value for key, value in record.__dict__.items()
            if key not in standard
            and key not in self.IGNORE_EXTRA_KEYS
            and not key.startswith("_")
        }

        if extras:
            extras_str = " | " + ", ".join(f"{k}={v}" for k, v in extras.items())
            record.msg = f"{record.msg}{extras_str}"

        return super().format(record)


def setup_logging() -> None:
    log_level = logging.INFO

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(log_level)

    handler = StreamHandler()
    handler.setLevel(log_level)

    formatter = ExtraFormatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    root.addHandler(handler)
