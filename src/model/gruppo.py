from dataclasses import dataclass, field
from datetime import datetime
from typing import Set


@dataclass
class Gruppo:
    id: str
    nomeGruppo: str
    descrizione: str
    listaUtenti: Set[str] = field(default_factory=set)          # id utenti
    amministratori: Set[str] = field(default_factory=set)  # id utenti
    materiali: Set[str] = field(default_factory=set)       # id materiali
    incontri: Set[str] = field(default_factory=set)        # id incontri
    messaggi: Set[str] = field(default_factory=set)        # id messaggi
    dataCreazione: datetime = field(default_factory=datetime.now)
