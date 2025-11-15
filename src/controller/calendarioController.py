from __future__ import annotations
from typing import List, Optional
from datetime import date

from persistence.datastore import DataStore
from persistence.repositories import (
    CalendarioRepository,
    IncontroRepository,
    GruppoRepository,
    UtenteRepository
)

from services.calendarioService import CalendarioService
from services.incontroService import IncontroService

from model.incontro import Incontro


class CalendarioController:

    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_calendari = CalendarioRepository(datastore)
        self.repo_incontri = IncontroRepository(datastore)
        self.repo_gruppi = GruppoRepository(datastore)
        self.repo_utenti = UtenteRepository(datastore)

        self.service = CalendarioService(datastore)
        self.incontro_service = IncontroService(datastore)

    # CALENDARIO UTENTE
    def calendario_utente(self, id_utente: str) -> List[Incontro]:
        return self.service.calendario_utente(id_utente)

    # CALENDARIO GRUPPO
    def calendario_gruppo(self, id_gruppo: str) -> List[Incontro]:
        return self.service.calendario_gruppo(id_gruppo)

    # INCONTRI FUTURI UTENTE
    def incontri_futuri_utente(self, id_utente: str) -> List[Incontro]:
        return self.service.incontri_futuri_utente(id_utente)

    # INCONTRI FUTURI GRUPPO
    def incontri_futuri_gruppo(self, id_gruppo: str) -> List[Incontro]:
        return self.service.incontri_futuri_gruppo(id_gruppo)

    # PROSSIMO INCONTRO UTENTE
    def prossimo_incontro_utente(self, id_utente: str) -> Optional[Incontro]:
        return self.service.prossimo_incontro_utente(id_utente)
    
    # PROSSIMO INCONTRO GRUPPO
    def prossimo_incontro_gruppo(self, id_gruppo: str) -> Optional[Incontro]:
        return self.service.prossimo_incontro_gruppo(id_gruppo)

    # INCONTRI PER DATA
    def incontri_per_data(self, id_utente: str, giorno: date) -> List[Incontro]:
        return self.service.incontri_per_data(id_utente, giorno)
