from dataclasses import dataclass, field

@dataclass
class Calendario:
    id: str
    incontri: list[str] = field(default_factory=list)
    promemoria: list[int] = field(default_factory=list)