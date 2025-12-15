from abc import ABC
from uuid import UUID
from dataclasses import dataclass, field
from datetime import datetime

from src.utils.uuid_v7 import uuid7
from src.utils.get_datetime_utc_now import get_datetime_utc_now


@dataclass(kw_only=True)
class Entity(ABC):
    uuid: UUID = field(default_factory=uuid7)
    created_at: datetime = field(default_factory=get_datetime_utc_now)
    updated_at: datetime = field(default_factory=get_datetime_utc_now)
    # _events: list = field(default_factory=list)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.uuid == other.uuid

    def __hash__(self) -> int:
        return hash(self.uuid)