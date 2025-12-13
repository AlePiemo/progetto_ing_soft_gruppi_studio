from __future__ import annotations
from typing import List, Optional
from datetime import datetime
import uuid

from persistence.datastore import DataStore, salva_datastore
from persistence.repositories import (
    MessaggioRepository,
    UtenteRepository,
    GruppoRepository
)

from model.messaggio import Messaggio
from model.utente import Utente


class ServizioMessaggio:
    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_messaggi = MessaggioRepository(datastore)
        self.repo_utenti = UtenteRepository(datastore)
        self.repo_gruppi = GruppoRepository(datastore)

    # INVIA MESSAGGIO DI GRUPPO 
    def invia_messaggio_gruppo(
        self, id_gruppo: int, id_mittente: int, testo: str
    ) -> bool:

        gruppo = self.repo_gruppi.get_by_id(id_gruppo)
        if not gruppo:
            return False

        if id_mittente not in gruppo.listaUtenti:
            return False  

        id_messaggio = str(uuid.uuid4())

        msg = Messaggio(
            id=id_messaggio,
            mittente=id_mittente,
            testo=testo,
            data=datetime.now()
        )

        # salva messaggio
        self.repo_messaggi.add(msg)

        # registra nella chat del gruppo
        gruppo.messaggi.add(id_messaggio)

        salva_datastore(self.datastore)
        return True
    
    # OTTIENI CHAT GRUPPO
    def chat_gruppo(self, id_gruppo: int) -> List[Messaggio]:
        gruppo = self.repo_gruppi.get_by_id(id_gruppo)
        if not gruppo:
            return[]
        
        messaggi = [
            self.repo_messaggi.get_by_id(mid)
            for mid in gruppo.messaggi
            if self.repo_messaggi.get_by_id(mid)
        ]

        messaggi.sort(key=lambda m: m.data)
        return messaggi

    # OTTIENI I MESSAGGI DI UN UTENTE
    def messaggi_di_utente(self, id_utente: int) -> List[Messaggio]:
        return self.repo_messaggi.get_by_user(id_utente)
