from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class StatoSegnalazione(Enum):
    Inviata = "Inviata"
    Valutata = "Valutata"
    Archiviata = "Archiviata"

@dataclass
class Segnalazione:
    id: str
    motivo: str
    autore: int         
    destinatario: int        # utente o messaggio segnalato 
    stato: StatoSegnalazione
    data: datetime = field(default_factory=datetime.now)
    #sanzione
    sanzione_tipo: str | None = None    
    sanzione_note: str | None = None
