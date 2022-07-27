from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class Shape(Enum):

    ALL_SHAPES = ""
    OUTLINE = "outline"
    FILL = "fill"
    LINEAL_COLOR = "lineal-color"
    HAND_DRAWN = "hand-drawn"


class OrderBy(Enum):

    POPULER = 4
    RECENT = 2


@dataclass
class Image:

    id: int
    name: str
    url: str

    pack: str
    downloads: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
