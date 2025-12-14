from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Promemoria:
    id: str
    testo: str
    data: datetime = field(default_factory=datetime.now)