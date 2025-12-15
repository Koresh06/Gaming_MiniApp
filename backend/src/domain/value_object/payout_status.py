from enum import StrEnum


class PayoutStatus(StrEnum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"