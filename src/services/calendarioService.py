from __future__ import annotations
from typing import List, Optional
from datetime import datetime, date

from persistence.datastore import DataStore
from persistence.repositories import (
    UtenteRepository,
    GruppoRepository,
    IncontroRepository,
    CalendarioRepository
)

from model.incontro import Incontro, IncontroStatus
from model.calendario import Calendario


class CalendarioService:
    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_utenti = UtenteRepository(datastore)
        self.repo_gruppi = GruppoRepository(datastore)
        self.repo_incontri = IncontroRepository(datastore)
        self.repo_calendari = CalendarioRepository(datastore)

    # CALENDARIO DI UN GRUPPO
    def calendario_gruppo(self, id_gruppo: str) -> List[Incontro]:
        gruppo = self.repo_gruppi.get_by_id(id_gruppo)
        if not gruppo:
            return []

        incontri = [
            self.repo_incontri.get_by_id(iid)
            for iid in gruppo.incontri
            if self.repo_incontri.get_by_id(iid)
        ]

        # ordina per data e ora
        incontri.sort(key=lambda x: (x.dataIncontro, x.oraIncontro))
        return incontri
    
    # CALENDARIO DI UN UTENTE
    def calendario_utente(self, id_utente: str) -> List[Incontro]:

        ut = self.repo_utenti.get_by_id(id_utente)
        if not ut:
            return []

        incontri = []

        for id_gruppo in ut.gruppi:
            incontri.extend(self.calendario_gruppo(id_gruppo))

        # ordina globalmente
        incontri.sort(key=lambda x: (x.dataIncontro, x.oraIncontro))
        return incontri
    
    # INCONTRI FUTURI DI UN GRUPPO
    def incontri_futuri_gruppo(self, id_gruppo: str) -> List[Incontro]:
        now = datetime.now()
        return [
            inc for inc in self.calendario_gruppo(id_gruppo)
            if inc.statoIncontro == IncontroStatus.PROGRAMMATO
            and inc.dataIncontro >= now
        ]

    # INCONTRI FUTURI DI UN UTENTE
    def incontri_futuri_utente(self, id_utente: str) -> List[Incontro]:
        now = datetime.now()
        return [
            inc for inc in self.calendario_utente(id_utente)
            if inc.statoIncontro == IncontroStatus.PROGRAMMATO
            and inc.dataIncontro >= now
        ]

    # PROSSIMO INCONTRO GRUPPO
    def prossimo_incontro_gruppo(self, id_gruppo: str) -> Optional[Incontro]:
        futuri = self.incontri_futuri_gruppo(id_gruppo)
        return futuri[0] if futuri else None

    # PROSSIMO INCONTRO UTENTE
    def prossimo_incontro_utente(self, id_utente: str) -> Optional[Incontro]:
        futuri = self.incontri_futuri_utente(id_utente)
        return futuri[0] if futuri else None

    # INCONTRI PER UNA DATA SPECIFICA
    def incontri_per_data(self, id_utente: str, giorno: date) -> List[Incontro]:

        return [
            inc for inc in self.calendario_utente(id_utente)
            if inc.dataIncontro.date() == giorno
            and inc.statoIncontro == IncontroStatus.PROGRAMMATO
        ]
