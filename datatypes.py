from pydantic import BaseModel
from typing import List
from enum import Enum, auto


class StoreStatus(Enum):
    WRONG_PASSWORD = auto()
    EMPTY_LEMMA = auto()
    EMPTY_DEFINITION = auto()
    ALREADY_STORED = auto()
    SUCCESS = auto()


class Lexeme(BaseModel):
    lemma: str
    definition: str
    mentions: List[str] = []
    is_built_in: bool
