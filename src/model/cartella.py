from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Cartella:
    id: int
    nome: str
    dataCreazione: datetime
    materiale_ids: list[int] = field(default_factory=list)  