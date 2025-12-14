from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Set

class RolePlatform(Enum):
    UTENTE = "UTENTE"
    ADMIN_GRUPPO = "ADMIN_GRUPPO"
    ADMIN_PIATTAFORMA = "ADMIN_PIATTAFORMA"


@dataclass
class Utente:
    id: str
    nome: str
    cognome: str
    email: str
    password: str
    sospeso: bool = False
    fineSospensione: date = None
    ultimoAccesso: datetime = None
    ruoloPiattaforma: RolePlatform = RolePlatform.UTENTE
    gruppi: Set[str] = field(default_factory=set)
    dataRegistrazione: datetime = field(default_factory=datetime.now)
