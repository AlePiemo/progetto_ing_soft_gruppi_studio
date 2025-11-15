from __future__ import annotations
import os
import shutil
from typing import List, Optional

from persistence.datastore import DataStore
from persistence.repositories import GruppoRepository, UtenteRepository, MaterialeRepository
from services.materialeService import MaterialeService
from model.materiale import Materiale


class MaterialeController:

    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_gruppi = GruppoRepository(datastore)
        self.repo_utenti = UtenteRepository(datastore)
        self.repo_materiali = MaterialeRepository(datastore)
        self.service = MaterialeService(datastore)

    # CARICA MATERIALE IN UN GRUPPO
    def carica_materiale(
        self,
        id_gruppo: str,
        id_autore: str,
        titolo: str,
        descrizione: str,
        percorso_locale: str
    ) -> Optional[Materiale]:

        return self.service.carica_materiale(
            id_gruppo=id_gruppo,
            id_autore=id_autore,
            titolo=titolo,
            descrizione=descrizione,
            percorso_locale=percorso_locale
        )

    # LISTA MATERIALI DI UN GRUPPO
    def materiali_gruppo(self, id_gruppo: str) -> List[Materiale]:
        return self.service.materiali_gruppo(id_gruppo)

    # OTTIENI MATERIALE SPECIFICO
    def get_materiale(self, id_materiale: str) -> Optional[Materiale]:
        return self.repo_materiali.get_by_id(id_materiale)

    # SCARICA MATERIAL
    def scarica_materiale(self, id_materiale: str, destinazione: str) -> bool:

        materiale = self.repo_materiali.get_by_id(id_materiale)
        if not materiale:
            return False

        if not os.path.exists(materiale.path_file):
            return False

        # crea destinazione se non esiste
        os.makedirs(destinazione, exist_ok=True)
        nome_finale = os.path.join(destinazione, materiale.nome_file)

        try:
            shutil.copy2(materiale.path_file, nome_finale)
            return True
        except Exception:
            return False

    # ELIMINA MATERIALE 
    def elimina_materiale(self, id_gruppo: str, id_admin: str, id_materiale: str) -> bool:
        return self.service.elimina_materiale(id_gruppo, id_admin, id_materiale)
