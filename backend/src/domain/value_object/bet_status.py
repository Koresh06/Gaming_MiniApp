from enum import StrEnum


class BetStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"