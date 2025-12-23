from .backetball import BasketballPayloadBuilder
from .dice import DicePayloadBuilder
from .darts import DartsPayloadBuilder
from .football import FootballPayloadBuilder
from .slot import SlotPayloadBuilder
from .bowling import BowlingPayloadBuilder


def get_payload_builders():
    return [
        DicePayloadBuilder(),
        FootballPayloadBuilder(),
        SlotPayloadBuilder(),
        BowlingPayloadBuilder(),
        BasketballPayloadBuilder(),
        DartsPayloadBuilder(),
    ]