from __future__ import annotations
from typing import List, Optional

from persistence.datastore import DataStore
from persistence.repositories import MessaggioRepository, GruppoRepository, UtenteRepository
from services.messaggioService import ServizioMessaggio
from model.messaggio import Messaggio


class MessaggioController:

    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_messaggi = MessaggioRepository(datastore)
        self.repo_gruppi = GruppoRepository(datastore)
        self.repo_utenti = UtenteRepository(datastore)
        self.service = ServizioMessaggio(datastore)

    # INVIA MESSAGGIO A UN GRUPPO
    def invia_messaggio_gruppo(self, id_gruppo: str, id_mittente: str, testo: str) -> bool:
        return self.service.invia_messaggio_gruppo(id_gruppo, id_mittente, testo)

    # OTTIENI CHAT DI UN GRUPPO 
    def chat_gruppo(self, id_gruppo: str) -> List[Messaggio]:
        return self.service.chat_gruppo(id_gruppo)

    # OTTIENI MESSAGGIO 
    def get_messaggio(self, id_messaggio: str) -> Optional[Messaggio]:
        return self.repo_messaggi.get_by_id(id_messaggio)

    # ELIMINA MESSAGGIO 
    def elimina_messaggio(self, id_gruppo: str, id_admin: str, id_messaggio: str) -> bool:
        gruppo = self.repo_gruppi.get_by_id(id_gruppo)
        if not gruppo:
            return False

        # controllo admin
        if id_admin not in gruppo.amministratori:
            return False

        # rimuovi messaggio dal gruppo
        if id_messaggio in gruppo.messaggi:
            gruppo.messaggi.remove(id_messaggio)

        # rimuovi messaggio dal repository
        self.repo_messaggi.remove(id_messaggio)

        return True
