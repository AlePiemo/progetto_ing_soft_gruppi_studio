from __future__ import annotations
from typing import List
from datetime import datetime
import uuid

from persistence.datastore import DataStore, salva_datastore
from persistence.repositories import GruppoRepository, UtenteRepository
from model.gruppo import Gruppo


class GruppoService:
    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_gruppi = GruppoRepository(datastore)
        self.repo_utenti = UtenteRepository(datastore)

    # CREAZIONE GRUPPO     
    def crea_gruppo(self, nome: str, descrizione: str, id_creatore: str) -> Gruppo:

        id_gruppo = str(uuid.uuid4())

        nuovoGruppo = Gruppo(
            id=id_gruppo,
            nomeGruppo=nome,
            descrizione=descrizione,
            listaUtenti=set(),
            amministratori=set(),
            materiali=set(),
            incontri=set(),
            messaggi=set(),
            dataCreazione=datetime.now()
        )

        # il creatore diventa membro e admin
        nuovoGruppo.listaUtenti.add(id_creatore)
        nuovoGruppo.amministratori.add(id_creatore)

        # salva
        self.repo_gruppi.add(nuovoGruppo)

        # aggiorna utente
        ut = self.repo_utenti.get_by_id(id_creatore)
        if ut:
            ut.gruppi.add(id_gruppo)

        salva_datastore(self.datastore)
        return nuovoGruppo

    # MODIFICA GRUPPO 
    def modifica_gruppo(self, id_gruppo: str, id_admin: str, **dati) -> bool:
        gruppo = self.repo_gruppi.get_by_id(id_gruppo)
        if not gruppo:
            return False

        if id_admin not in gruppo.amministratori:
            return False  

        for campo, valore in dati.items():
            if hasattr(gruppo, campo):
                setattr(gruppo, campo, valore)

        salva_datastore(self.datastore)
        return True

    # ELIMINAZIONE GRUPPO 
    def elimina_gruppo(self, id_gruppo: str, id_admin: str) -> bool:
        gruppo = self.repo_gruppi.get_by_id(id_gruppo)
        if not gruppo:
            return False

        if id_admin not in gruppo.amministratori:
            return False

        # rimuovi il gruppo dagli utenti membri
        for uid in gruppo.listaUtenti:
            ut = self.repo_utenti.get_by_id(uid)
            if ut:
                ut.gruppi.discard(id_gruppo)

        self.repo_gruppi.remove(id_gruppo)
        salva_datastore(self.datastore)
        return True

    # AGGIUNGI MEMBRO 
    def aggiungi_membro(self, id_gruppo: str, id_admin: str, id_membro: str) -> bool:
        gruppo = self.repo_gruppi.get_by_id(id_gruppo)
        if not gruppo:
            return False

        if id_admin not in gruppo.amministratori:
            return False 

        gruppo.listaUtenti.add(id_membro)

        # aggiorna utente
        user = self.repo_utenti.get_by_id(id_membro)
        if user:
            user.gruppi.add(id_gruppo)

        salva_datastore(self.datastore)
        return True

    # RIMUOVI MEMBRO 
    def rimuovi_membro(self, id_gruppo: str, id_admin: str, id_membro: str) -> bool:
        gruppo = self.repo_gruppi.get_by_id(id_gruppo)
        if not gruppo:
            return False

        if id_admin not in gruppo.amministratori:
            return False

        gruppo.listaUtenti.discard(id_membro)
        gruppo.amministratori.discard(id_membro)

        ut = self.repo_utenti.get_by_id(id_membro)
        if ut:
            ut.gruppi.discard(id_gruppo)

        salva_datastore(self.datastore)
        return True

    # NOMINA AMMINISTRATORE
    def nomina_admin(self, id_gruppo: str, id_admin: str, id_membro: str) -> bool:
        gruppo = self.repo_gruppi.get_by_id(id_gruppo)
        if not gruppo:
            return False

        if id_admin not in gruppo.amministratori:
            return False

        if id_membro not in gruppo.listaUtenti:
            return False

        gruppo.amministratori.add(id_membro)
        salva_datastore(self.datastore)
        return True

    # REVOCA AMMINISTRATORE
    def revoca_admin(self, id_gruppo: str, id_admin: str, id_membro: str) -> bool:
        gruppo = self.repo_gruppi.get_by_id(id_gruppo)
        if not gruppo:
            return False

        if id_admin not in gruppo.amministratori:
            return False

        gruppo.amministratori.discard(id_membro)
        salva_datastore(self.datastore)
        return True

    # LISTA GRUPPI
    def lista_gruppi(self) -> List[Gruppo]:
        return self.repo_gruppi.get_all()

    # RICERCA GRUPPI 
    def cerca_gruppi(self, nome: str = "") -> List[Gruppo]:
        risultati = []

        for g in self.lista_gruppi():
            if (
                (not nome or nome.lower() in g.nomeGruppo.lower())
            ):
                risultati.append(g)

        return risultati