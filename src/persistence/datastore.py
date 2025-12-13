from __future__ import annotations
import os
import pickle
from dataclasses import dataclass, field
from typing import Dict

from model.utente import Utente
from model.gruppo import Gruppo
from model.messaggio import Messaggio
from model.incontro import Incontro
from model.materiale import Materiale
from model.segnalazione import Segnalazione
from model.notifica import Notifica
from model.backup import Backup
from model.chat import Chat
from model.calendario import Calendario

DEFAULT_DATA_PATH = os.path.join("data", "data.pkl")

@dataclass
class DataStore:
    users: Dict[str, Utente] = field(default_factory=dict)
    groups: Dict[str, Gruppo] = field(default_factory=dict)
    messages: Dict[str, Messaggio] = field(default_factory=dict)
    meetings: Dict[str, Incontro] = field(default_factory=dict)
    materials: Dict[str, Materiale] = field(default_factory=dict)
    reports: Dict[str, Segnalazione] = field(default_factory=dict)
    notifications: Dict[str, Notifica] = field(default_factory=dict)
    backups: Dict[str, Backup] = field(default_factory=dict)
    chats: Dict[str, Chat] = field(default_factory=dict)
    calendars: Dict[str, Calendario] = field(default_factory=dict)


def carica_datastore(percorso: str = DEFAULT_DATA_PATH) -> DataStore:
    if not os.path.exists(percorso):
        # nessun file
        return DataStore()

    with open(percorso, "rb") as f:
        ds: DataStore = pickle.load(f)
    return ds

def salva_datastore(datastore: DataStore, percorso: str = DEFAULT_DATA_PATH) -> None:
    os.makedirs(os.path.dirname(percorso), exist_ok=True)

    with open(percorso, "wb") as f:
        pickle.dump(datastore, f)
