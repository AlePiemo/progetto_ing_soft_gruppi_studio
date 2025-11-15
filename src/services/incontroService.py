from __future__ import annotations
from typing import Optional, List
import uuid
from datetime import datetime

from persistence.datastore import DataStore, salva_datastore
from persistence.repositories import IncontroRepository, GruppoRepository
from model.incontro import Incontro, IncontroStatus


class IncontroService:

    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_incontri = IncontroRepository(datastore)
        self.repo_gruppi = GruppoRepository(datastore)

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

        gruppo = self.repo_gruppi.get_by_id(id_gruppo)
        if not gruppo:
            return None

        if id_admin not in gruppo.amministratori:
            return None

        id_incontro = str(uuid.uuid4())

        nuovo = Incontro(
            id=id_incontro,
            titolo=titolo,
            descrizione=descrizione,
            statoIncontro=IncontroStatus.PROGRAMMATO,
            dataIncontro=data,
            oraIncontro=ora,
            gruppo_id=id_gruppo
        )

        # salva incontro
        self.repo_incontri.add(nuovo)

        # aggiungi al gruppo
        gruppo.incontri.add(id_incontro)

        salva_datastore(self.datastore)
        return nuovo
    
    # MODIFICA INCONTRO
    def modifica_incontro(self, id_incontro: str, id_admin: str, **dati) -> bool:

        inc = self.repo_incontri.get_by_id(id_incontro)
        if not inc:
            return False

        gruppo = self.repo_gruppi.get_by_id(inc.gruppo_id)
        if not gruppo:
            return False

        if id_admin not in gruppo.amministratori:
            return False

        for campo, valore in dati.items():
            if hasattr(inc, campo):
                setattr(inc, campo, valore)

        salva_datastore(self.datastore)
        return True

    # ANNULLA INCONTRO
    def annulla_incontro(self, id_incontro: str, id_admin: str) -> bool:

        inc = self.repo_incontri.get_by_id(id_incontro)
        if not inc:
            return False

        gruppo = self.repo_gruppi.get_by_id(inc.gruppo_id)
        if not gruppo:
            return False

        if id_admin not in gruppo.amministratori:
            return False

        inc.statoIncontro = IncontroStatus.ANNULLATO

        salva_datastore(self.datastore)
        return True

    # ELIMINA INCONTRO
    def elimina_incontro(self, id_incontro: str, id_admin: str) -> bool:

        inc = self.repo_incontri.get_by_id(id_incontro)
        if not inc:
            return False

        gruppo = self.repo_gruppi.get_by_id(inc.gruppo_id)
        if not gruppo:
            return False

        if id_admin not in gruppo.amministratori:
            return False

        # rimuovi dal gruppo
        gruppo.incontri.discard(id_incontro)
        self.repo_incontri.remove(id_incontro)

        salva_datastore(self.datastore)
        return True

    # LISTA INCONTRI DI UN GRUPPO
    def incontri_di_gruppo(self, id_gruppo: str) -> List[Incontro]:

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
