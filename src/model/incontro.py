from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class IncontroStatus(Enum):
    PROGRAMMATO = "PROGRAMMATO"
    ANNULLATO = "ANNULLATO"

@dataclass
class Incontro:
    id: str
    titolo: str
    descrizione: str
    dataIncontro: datetime 
    oraIncontro: datetime
    gruppo_id: str  

    statoIncontro: IncontroStatus = IncontroStatus.PROGRAMMATO

