from __future__ import annotations
import uuid
from datetime import datetime
from typing import List

from persistence.datastore import DataStore, salva_datastore
from persistence.repositories import NotificaRepository, UtenteRepository
from model.notifica import Notifica, TipoNotifica


class NotificaService:
    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_notifiche = NotificaRepository(datastore)
        self.repo_utenti = UtenteRepository(datastore)

    # INVIA NOTIFICA
    def invia_notifica(
        self,
        id_destinatario: str,
        tipo: TipoNotifica,
        descrizione: str
    ) -> Notifica:

        # verifica utente
        if not self.repo_utenti.get_by_id(id_destinatario):
            raise ValueError("Destinatario non esistente")

        id_notifica = str(uuid.uuid4())

        n = Notifica(
            id=id_notifica,
            descrizione=descrizione,
            dataInvio=datetime.now(),
            tipo=tipo,
            destinatario=id_destinatario,
        )

        self.repo_notifiche.add(n)
        salva_datastore(self.datastore)
        return n

    # NOTIFICHE DI UN UTENTE
    def notifiche_utente(self, id_utente: str) -> List[Notifica]:
        return [
            n for n in self.repo_notifiche.get_all()
            if n.destinatario == id_utente
        ]

    # NOTIFICHE PER TIPO
    def notifiche_per_tipo(
        self, id_utente: str, tipo: TipoNotifica
    ) -> List[Notifica]:
        return [
            n for n in self.notifiche_utente(id_utente)
            if n.tipo == tipo
        ]

    # CANCELLA NOTIFICA
    def elimina_notifica(self, id_notifica: str) -> bool:
        n = self.repo_notifiche.get_by_id(id_notifica)
        if not n:
            return False

        self.repo_notifiche.remove(id_notifica)
        salva_datastore(self.datastore)
        return True
