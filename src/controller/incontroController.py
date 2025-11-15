from __future__ import annotations
from typing import List, Optional
from datetime import datetime, date

from persistence.datastore import DataStore
from persistence.repositories import IncontroRepository, GruppoRepository
from services.incontroService import IncontroService
from services.calendarioService import CalendarioService
from model.incontro import Incontro, IncontroStatus


class IncontroController:

    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_incontri = IncontroRepository(datastore)
        self.repo_gruppi = GruppoRepository(datastore)
        self.service = IncontroService(datastore)
        self.calendario = CalendarioService(datastore)

    # CREA INCONTRO
    def crea_incontro(
        self,
        id_gruppo: str,
        id_admin: str,
        titolo: str,
        descrizione: str,
        data: datetime,
        ora: datetime
    ) -> Optional[Incontro]:

        return self.service.crea_incontro(
            id_gruppo=id_gruppo,
            id_admin=id_admin,
            titolo=titolo,
            descrizione=descrizione,
            data=data,
            ora=ora
        )

    # MODIFICA INCONTRO
    def modifica_incontro(self, id_incontro: str, id_admin: str, **campi) -> bool:
        return self.service.modifica_incontro(id_incontro, id_admin, **campi)

    # ANNULLA INCONTRO
    def annulla_incontro(self, id_incontro: str, id_admin: str) -> bool:
        return self.service.annulla_incontro(id_incontro, id_admin)

    # ELIMINA INCONTRO
    def elimina_incontro(self, id_incontro: str, id_admin: str) -> bool:
        return self.service.elimina_incontro(id_incontro, id_admin)

    # OTTIENI INCONTRO
    def get_incontro(self, id_incontro: str) -> Optional[Incontro]:
        return self.repo_incontri.get_by_id(id_incontro)

    # LISTA INCONTRI
    def incontri_gruppo(self, id_gruppo: str) -> List[Incontro]:
        return self.service.incontri_di_gruppo(id_gruppo)


