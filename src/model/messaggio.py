from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Messaggio:
    id: int
    mittente: int 
    testo: str
    data: datetime = field(default_factory=datetime.now)

