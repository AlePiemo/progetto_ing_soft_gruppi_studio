from __future__ import annotations
import uuid
from datetime import datetime, timedelta
from typing import Optional, List

from persistence.datastore import DataStore, salva_datastore
from persistence.repositories import UtenteRepository
from model.utente import Utente
from model.utente import RolePlatform


class UtenteController:

    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_utenti = UtenteRepository(datastore)
        self.utente_attivo: Optional[Utente] = None

    # REGISTRAZIONE
    def registra_utente(
        self,
        nome: str,
        cognome: str,
        email: str,
        password: str
    ) -> Optional[Utente]:

        for u in self.repo_utenti.get_all():
            if u.email == email:
                return None  

        id_utente = str(uuid.uuid4())

        nuovo = Utente(
            id=id_utente,
            nome=nome,
            cognome=cognome,
            email=email,
            password=password,
            ruoloPiattaforma=RolePlatform.UTENTE,
            sospeso=False,
            fineSospensione=None,
            ultimoAccesso=None,
        )

        self.repo_utenti.add(nuovo)
        salva_datastore(self.datastore)
        return nuovo

    # LOGIN
    def login(self, email: str, password: str) -> Optional[Utente]:

        for u in self.repo_utenti.get_all():

            if u.email == email and u.password == password:

                # controllo sospensione
                if u.sospeso:
                    if u.fineSospensione and u.fineSospensione <= datetime.now().date():
                        u.sospeso = False
                        u.fineSospensione = None
                    else:
                        return None

                u.ultimoAccesso = datetime.now()
                salva_datastore(self.datastore)

                self.utente_attivo = u
                return u

        return None

    # LOGOUT
    def logout(self):
        self.utente_attivo = None

    # GET UTENTE ATTIVO
    def get_utente_attivo(self) -> Optional[Utente]:
        return self.utente_attivo

    # LISTA UTENTI
    def lista_utenti(self) -> List[Utente]:
        return self.repo_utenti.get_all()

    # AGGIORNA PROFILO
    def aggiorna_profilo(
        self,
        id_utente: str,
        nome: Optional[str] = None,
        cognome: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None
    ) -> bool:

        u = self.repo_utenti.get_by_id(id_utente)
        if not u:
            return False

        if nome is not None:
            u.nome = nome
        if cognome is not None:
            u.cognome = cognome
        if email is not None:
            u.email = email
        if password is not None:
            u.password = password

        salva_datastore(self.datastore)
        return True

    # SOSPENDI UTENTE 
    def sospendi_utente(
        self,
        admin_id: str,
        id_utente: str,
        giorni: int
    ) -> bool:

        admin = self.repo_utenti.get_by_id(admin_id)
        if not admin or admin.ruoloPiattaforma != RolePlatform.ADMIN_PIATTAFORMA:
            return False

        u = self.repo_utenti.get_by_id(id_utente)
        if not u:
            return False

        u.sospeso = True
        u.fineSospensione = (datetime.now() + timedelta(days=giorni)).date()

        salva_datastore(self.datastore)
        return True

    # RIATTIVA UTENTE 
    def riattiva_utente(self, admin_id: str, id_utente: str) -> bool:

        admin = self.repo_utenti.get_by_id(admin_id)
        if not admin or admin.ruoloPiattaforma != RolePlatform.ADMIN_PIATTAFORMA:
            return False

        u = self.repo_utenti.get_by_id(id_utente)
        if not u:
            return False

        u.sospeso = False
        u.fineSospensione = None

        salva_datastore(self.datastore)
        return True
