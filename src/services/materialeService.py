from __future__ import annotations
import uuid
import os
from typing import List, Optional
from datetime import datetime

from persistence.datastore import DataStore, salva_datastore
from persistence.repositories import (
    MaterialeRepository,
    GruppoRepository,
    UtenteRepository,
)

from model.materiale import Materiale


class MaterialeService:
    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_materiali = MaterialeRepository(datastore)
        self.repo_gruppi = GruppoRepository(datastore)
        self.repo_utenti = UtenteRepository(datastore)

        self.cartella_materiali = os.path.join("data","materiali")
        os.makedirs(self.cartella_materiali, exist_ok=True)

    # CARICA MATERIALE 
    def carica_materiale(
        self,
        id_gruppo: str,
        titolo: str,
        contenuto: str,
        autore: int,    
        nome_file: str,
        dimensione: int,
        path_file: str,
    ) -> Optional[Materiale]:
        
        gruppo = self.repo_gruppi.get_by_id(id_gruppo)
        if not gruppo:
            return None
        
        if autore not in gruppo.listaUtenti:
            return None
        
        if not os.path.exists(path_file):
            return None

        id_materiale = str(uuid.uuid4())
        nome_file = os.path.basename(path_file)
        dimensione = os.path.getsize(path_file)

        nuovo_nome = f"{id_materiale}_{nome_file}"
        percorso_salvato = os.path.join(self.cartella_materiali, nuovo_nome)

        # copia file 
        with open(path_file, "rb") as src:
            with open(percorso_salvato, "wb") as dst:
                dst.write(src.read())

        materiale = Materiale(
            id=id_materiale,
            autore=autore,
            titolo=titolo,
            contenuto=contenuto,
            nome_file=nome_file,
            path_file=percorso_salvato,
            dimensione=dimensione,
            dataCaricamento=datetime.now()
        )

        self.repo_materiali.add(materiale)
        gruppo.materiali.add(id_materiale)

        salva_datastore(self.datastore)
        return materiale

    # LISTA MATERIALI DI UN GRUPPO 
    def lista_materiali_gruppo(self, id_gruppo: str) -> List[Materiale]:
        gruppo = self.repo_gruppi.get_by_id(id_gruppo)
        if not gruppo:
            return []

        materiali = [
            self.repo_materiali.get_by_id(id_mat)
            for id_mat in gruppo.materiali
            if self.repo_materiali.get_by_id(id_mat)
        ]

        return materiali

    # VISUALIZZA DETTAGLI MATERIALE 
    def dettaglio_materiale(self, id_materiale: str) -> Optional[Materiale]:
        return self.repo_materiali.get_by_id(id_materiale)

    # SCARICA MATERIALE
    def scarica_materiale(self, id_materiale: str, percorso_destinazione: str) -> bool:

        materiale = self.repo_materiali.get_by_id(id_materiale)
        if not materiale:
            return False

        if not os.path.exists(materiale.path_file):
            return False

        os.makedirs(os.path.dirname(percorso_destinazione), exist_ok=True)

        with open(materiale.path_file, "rb") as src:
            with open(percorso_destinazione, "wb") as dst:
                dst.write(src.read())

        return True

    # ELIMINA MATERIALE         
    def elimina_materiale(self, id_materiale: str, id_gruppo: str, id_admin: str) -> bool:

        gruppo = self.repo_gruppi.get_by_id(id_gruppo)
        if not gruppo:
            return False

        if id_admin not in gruppo.amministratori:
            return False

        materiale = self.repo_materiali.get_by_id(id_materiale)
        if not materiale:
            return False

        # rimuovi file dal disco
        if os.path.exists(materiale.path_file):
            os.remove(materiale.path_file)

        # rimuovi dagli elenchi
        self.repo_materiali.remove(id_materiale)
        gruppo.materiali.discard(id_materiale)

        salva_datastore(self.datastore)
        return True
