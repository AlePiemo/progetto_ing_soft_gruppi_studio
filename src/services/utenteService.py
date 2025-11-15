from __future__ import annotations

from typing import Optional
from datetime import date

from persistence.datastore import DataStore, salva_datastore
from persistence.repositories import UtenteRepository
from model.utente import Utente, RolePlatform


class UtenteService:
    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo = UtenteRepository(datastore)
        self._utente_loggato: Optional[Utente] = None

    # REGISTRAZIONE UTENTE (RF1)
    def registra_utente(
        self,
        id: int,
        nome: str,
        cognome: str,
        email: str,
        password: str
    ) -> bool:

        if self.repo.find_by_email(email) is not None:
            return False 

        user = Utente(
            id=id,
            nome=nome,
            cognome=cognome,
            email=email,
            password=password
        )

        self.repo.add(user)
        salva_datastore(self.datastore)
        return True

    # LOGIN UTENTE (RF2)
    def login(self, email: str, password: str) -> Optional[Utente]:
        user = self.repo.find_by_email(email)
        if user is None:
            return None

        if user.password != password:
            return None

        self._utente_loggato = user
        return user

    # LOGOUT UTENTE (RF2)
    def logout(self) -> None:
        self._utente_loggato = None

    def get_utente_loggato(self) -> Optional[Utente]:
        return self._utente_loggato

    # admin: CREA UTENTE (RF4)
    def admin_crea_utente(
        self,
        admin: Utente,
        id: int,
        nome: str,
        cognome: str,
        email: str,
        password: str
    ) -> bool:

        if admin.ruoloPiattaforma != RolePlatform.ADMIN_PIATTAFORMA:
            return False

        if self.repo.find_by_email(email) is not None:
            return False

        nuovo = Utente(
            id=id,
            nome=nome,
            cognome=cognome,
            email=email,
            password=password
        )

        self.repo.add(nuovo)
        salva_datastore(self.datastore)
        return True

    # admin: MODIFICA UTENTE (RF4)
    def admin_modifica_utente(
        self,
        admin: Utente,
        id: int,
        **dati
    ) -> bool:

        if admin.ruoloPiattaforma != RolePlatform.ADMIN_PIATTAFORMA:
            return False

        user = self.repo.get_by_id(id)
        if user is None:
            return False

        for campo, valore in dati.items():
            if hasattr(user, campo):
                setattr(user, campo, valore)

        salva_datastore(self.datastore)
        return True

    # admin: ELIMINA UTENTE (RF4)
    def admin_elimina_utente(self, admin: Utente, id: int) -> bool:
        if admin.ruoloPiattaforma != RolePlatform.ADMIN_PIATTAFORMA:
            return False

        if self.repo.get_by_id(id) is None:
            return False

        self.repo.remove(id)
        salva_datastore(self.datastore)
        return True

    # RICERCA UTENTI (RF6)
    def cerca_utenti(self, nome: str = "", cognome: str = "", email: str = ""):
        risultati = []

        for user in self.repo.get_all():
            if (
                (not nome or nome.lower() in user.nome.lower())
                and (not cognome or cognome.lower() in user.cognome.lower())
                and (not email or email.lower() in user.email.lower())
            ):
                risultati.append(user)

        return risultati
