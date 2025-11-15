from dataclasses import dataclass, field

@dataclass
class Calendario:
    id: int
    incontri: list[int] = field(default_factory=list)
    promemoria: list[int] = field(default_factory=list)