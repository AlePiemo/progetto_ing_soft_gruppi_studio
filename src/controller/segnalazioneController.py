from __future__ import annotations
from typing import List, Optional

from persistence.datastore import DataStore
from persistence.repositories import (
    SegnalazioneRepository,
    UtenteRepository,
    MessaggioRepository,
)
from services.segnalazioneService import SegnalazioneService
from model.segnalazione import Segnalazione, StatoSegnalazione
from model.utente import Utente, RolePlatform


class SegnalazioneController:

    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_segnalazioni = SegnalazioneRepository(datastore)
        self.repo_utenti = UtenteRepository(datastore)
        self.repo_messaggi = MessaggioRepository(datastore)
        self.service = SegnalazioneService(datastore)

    # CREA SEGNALAZIONE UTENTE
    def segnala_utente(
        self,
        id_autore: str,
        id_utente: str,
        motivo: str,
    ) -> Optional[Segnalazione]:

        return self.service.segnala_utente(
            id_autore=id_autore,
            id_utente_segnalato=id_utente,
            motivo=motivo
        )

    # CREA SEGNALAZIONE MESSAGGIO
    def segnala_messaggio(
        self,
        id_autore: str,
        id_messaggio: str,
        motivo: str,
    ) -> Optional[Segnalazione]:

        return self.service.segnala_messaggio(
            id_autore=id_autore,
            id_messaggio=id_messaggio,
            motivo=motivo
        )

    # VALUTA SEGNALAZIONE 
    def valuta_segnalazione(
        self,
        admin_id: str,
        id_segnalazione: str
    ) -> bool:

        admin = self.repo_utenti.get_by_id(admin_id)
        if not admin:
            return False

        return self.service.cambia_stato(
            admin=admin,
            id_segnalazione=id_segnalazione,
            nuovo_stato=StatoSegnalazione.Valutata
        )

    # ARCHIVIA SEGNALAZIONE 
    def archivia_segnalazione(
        self,
        admin_id: str,
        id_segnalazione: str
    ) -> bool:

        admin = self.repo_utenti.get_by_id(admin_id)
        if not admin:
            return False

        return self.service.cambia_stato(
            admin=admin,
            id_segnalazione=id_segnalazione,
            nuovo_stato=StatoSegnalazione.Archiviata
        )

    # APPLICA SANZIONE 
    def applica_sanzione(
        self,
        admin_id: str,
        id_segnalazione: str,
        tipo: str,
        note: str
    ) -> bool:

        admin = self.repo_utenti.get_by_id(admin_id)
        if not admin:
            return False

        return self.service.applica_sanzione(
            admin=admin,
            id_segnalazione=id_segnalazione,
            tipo_sanzione=tipo,
            note=note
        )

    # LISTE DI SEGNALAZIONI 
    def segnalazioni_in_attesa(self) -> List[Segnalazione]:
        return self.service.segnalazioni_in_attesa()

    def segnalazioni_valutate(self) -> List[Segnalazione]:
        return self.service.segnalazioni_valutate()

    def segnalazioni_archiviate(self) -> List[Segnalazione]:
        return self.service.segnalazioni_archiviate()

    # OTTIENI SINGOLA SEGNALAZIONE
    def get_segnalazione(self, id_segnalazione: str) -> Optional[Segnalazione]:
        return self.repo_segnalazioni.get_by_id(id_segnalazione)
