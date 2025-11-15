from __future__ import annotations
from typing import List, Optional

from persistence.datastore import DataStore
from persistence.repositories import NotificaRepository, UtenteRepository
from services.notificaService import NotificaService
from model.notifica import Notifica, TipoNotifica


class NotificaController:

    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_notifiche = NotificaRepository(datastore)
        self.repo_utenti = UtenteRepository(datastore)
        self.service = NotificaService(datastore)

    # INVIA NOTIFICA 
    def invia_notifica(
        self,
        id_destinatario: str,
        tipo: TipoNotifica,
        descrizione: str
    ) -> Notifica:

        return self.service.invia_notifica(
            id_destinatario=id_destinatario,
            tipo=tipo,
            descrizione=descrizione
        )

    # NOTIFICHE UTENTE
    def notifiche_utente(self, id_utente: str) -> List[Notifica]:
        return self.service.notifiche_utente(id_utente)

    # FILTRA NOTIFICHE PER TIPO
    def notifiche_per_tipo(self, id_utente: str, tipo: TipoNotifica) -> List[Notifica]:
        return self.service.notifiche_per_tipo(id_utente, tipo)

    # OTTIENI NOTIFICA
    def get_notifica(self, id_notifica: str) -> Optional[Notifica]:
        return self.repo_notifiche.get_by_id(id_notifica)

    # CANCELLA NOTIFICA
    def elimina_notifica(self, id_notifica: str) -> bool:
        return self.service.elimina_notifica(id_notifica)
