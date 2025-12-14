from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Cartella:
    id: str
    nome: str
    dataCreazione: datetime
    materiale_ids: list[str] = field(default_factory=list)  