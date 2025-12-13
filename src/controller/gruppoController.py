from __future__ import annotations
from typing import List, Optional

from persistence.datastore import DataStore, salva_datastore
from persistence.repositories import GruppoRepository, UtenteRepository
from services.gruppoService import GruppoService
from model.gruppo import Gruppo


class GruppoController:

    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_gruppi = GruppoRepository(datastore)
        self.repo_utenti = UtenteRepository(datastore)
        self.service = GruppoService(datastore)

    # CREA GRUPPO
    def crea_gruppo(self, nome: str, descrizione: str, id_creatore: str) -> Optional[Gruppo]:
        return self.service.crea_gruppo(nome, descrizione, id_creatore)

    # MODIFICA GRUPPO
    def modifica_gruppo(self, id_gruppo: str, id_admin: str, **campi) -> bool:
        return self.service.modifica_gruppo(id_gruppo, id_admin, **campi)

    # ELIMINA GRUPPO
    def elimina_gruppo(self, id_gruppo: str, id_admin: str) -> bool:
        return self.service.elimina_gruppo(id_gruppo, id_admin)

    # AGGIUNGI MEMBRO
    def aggiungi_membro(self, id_gruppo: str, id_admin: str, id_membro: str) -> bool:
        return self.service.aggiungi_membro(id_gruppo, id_admin, id_membro)

    # RIMUOVI MEMBRO
    def rimuovi_membro(self, id_gruppo: str, id_admin: str, id_membro: str) -> bool:
        return self.service.rimuovi_membro(id_gruppo, id_admin, id_membro)
    # NOMINA ADMIN
    def nomina_admin(self, id_gruppo: str, id_admin: str, id_utente: str) -> bool:
        return self.service.nomina_admin(id_gruppo, id_admin, id_utente)

    # REVOCA ADMIN
    def revoca_admin(self, id_gruppo: str, id_admin: str, id_utente: str) -> bool:
        return self.service.revoca_admin(id_gruppo, id_admin, id_utente)

    # LISTA GRUPPI
    def lista_gruppi(self) -> List[Gruppo]:
        return self.service.lista_gruppi()

    # CERCA GRUPPI PER NOME
    def cerca_gruppi(self, nome: str) -> List[Gruppo]:
        return self.service.cerca_gruppi(nome)

    # DETTAGLI GRUPPO
    def get_gruppo(self, id_gruppo: str) -> Optional[Gruppo]:
        return self.repo_gruppi.get_by_id(id_gruppo)
