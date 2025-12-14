from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class TipoNotifica(Enum):
    SISTEMA = "SISTEMA"
    INCONTRO = "INCONTRO"
    MATERIALE = "MATERIALE"
    SEGNALAZIONE = "SEGNALAZIONE"
    SANZIONE = "SANZIONE"

@dataclass
class Notifica:
    id: str
    descrizione: str
    destinatario: int  
    tipo: TipoNotifica

    dataInvio: datetime = field(default_factory=datetime.now)

