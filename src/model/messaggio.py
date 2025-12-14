from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Messaggio:
    id: str
    mittente: str 
    testo: str
    data: datetime = field(default_factory=datetime.now)

