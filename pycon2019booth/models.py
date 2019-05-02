from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class BoothEvent:
    start: str
    finish: str
    title: str
    who: str


@dataclass
class Facility:
    title: str
    thursday: Optional[List[BoothEvent]] = field(default_factory=list)
    friday: Optional[List[BoothEvent]] = field(default_factory=list)
    saturday: Optional[List[BoothEvent]] = field(default_factory=list)
