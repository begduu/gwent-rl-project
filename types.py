from typing import NotRequired, TypedDict
from enum import Enum

class CardData(TypedDict):
    name: str
    type: str
    ability: str

    strength: NotRequired[int]
    row: NotRequired[str]

class DeckInfo(TypedDict):
    name: str
    leader_id: str
    card_ids: list[str]

class RowType(Enum):
    CLOSE = "close"
    RANGED = "ranged"
    SIEGE = "siege"

class Ability(Enum):
    DECOY = "decoy"
    HORN = "horn"

