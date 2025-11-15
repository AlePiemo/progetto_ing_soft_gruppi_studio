from __future__ import annotations
from typing import List, Optional
import uuid
from datetime import datetime

from persistence.datastore import DataStore, salva_datastore
from persistence.repositories import (
    GruppoRepository,
    UtenteRepository,
    MessaggioRepository,
)

from model.messaggio import Messaggio


class ChatService:
    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_gruppi = GruppoRepository(datastore)
        self.repo_utenti = UtenteRepository(datastore)
        self.repo_messaggi = MessaggioRepository(datastore)

    # INVIA MESSAGGIO DI GRUPPO
    def invia_gruppo(self, id_gruppo: int, id_mittente: int, contenuto: str) -> bool:

        gruppo = self.repo_gruppi.get_by_id(id_gruppo)
        if not gruppo:
            return False

        # deve essere membro del gruppo
        if id_mittente not in gruppo.membri:
            return False

        id_messaggio = int(uuid.uuid4())

        msg = Messaggio(
            id=id_messaggio,
            mittente_id=id_mittente,
            contenuto=contenuto,
            timestamp=datetime.now()
        )

        self.repo_messaggi.add(msg)
        gruppo.messaggi.add(id_messaggio)

        salva_datastore(self.datastore)
        return True

    # CHAT DI GRUPPO
    def chat_gruppo(self, id_gruppo: int) -> List[Messaggio]:
        gruppo = self.repo_gruppi.get_by_id(id_gruppo)
        if not gruppo:
            return []

        messaggi = [
            self.repo_messaggi.get_by_id(id_msg)
            for id_msg in gruppo.messaggi
            if self.repo_messaggi.get_by_id(id_msg)
        ]

        messaggi.sort(key=lambda x: x.timestamp)
        return messaggi

    # MESSAGGI NON LETTI 
    def non_letti(self, id_utente: int) -> List[Messaggio]:

        tutti = []

        # messaggi nei gruppi a cui appartiene
        utente = self.repo_utenti.get_by_id(id_utente)
        if utente:
            for id_gruppo in utente.gruppi:
                gruppo = self.repo_gruppi.get_by_id(id_gruppo)
                if gruppo:
                    for id_msg in gruppo.messaggi:
                        msg = self.repo_messaggi.get_by_id(id_msg)
                        if msg and msg.mittente_id != id_utente and not msg.letto:
                            tutti.append(msg)

        tutti.sort(key=lambda x: x.timestamp)
        return tutti

    # SEGNARE MESSAGGIO COME LETTO
    def segna_letto(self, id_messaggio: int) -> bool:
        msg = self.repo_messaggi.get_by_id(id_messaggio)
        if not msg:
            return False
        msg.letto = True
        salva_datastore(self.datastore)
        return True

    # ULTIMO MESSAGGIO DI UNA CHAT 
    def ultimo_messaggio_gruppo(self, id_gruppo: int) -> Optional[Messaggio]:
        chat = self.chat_gruppo(id_gruppo)
        return chat[-1] if chat else None
