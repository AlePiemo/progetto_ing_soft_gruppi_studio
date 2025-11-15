from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class IncontroStatus(Enum):
    PROGRAMMATO = "PROGRAMMATO"
    ANNULLATO = "ANNULLATO"

@dataclass
class Incontro:
    id: int
    titolo: str
    descrizione: str
    dataIncontro: datetime 
    oraIncontro: datetime
    gruppo_id: int  

    statoIncontro: IncontroStatus = IncontroStatus.PROGRAMMATO

