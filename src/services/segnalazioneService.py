from __future__ import annotations
import uuid
from typing import List, Optional

from persistence.datastore import DataStore, salva_datastore
from persistence.repositories import (
    UtenteRepository,
    GruppoRepository,
    SegnalazioneRepository,
    MessaggioRepository,
)

from model.segnalazione import Segnalazione, StatoSegnalazione
from model.utente import Utente, RolePlatform


class SegnalazioneService:
    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_utenti = UtenteRepository(datastore)
        self.repo_gruppi = GruppoRepository(datastore)
        self.repo_segnalazioni = SegnalazioneRepository(datastore)
        self.repo_messaggi = MessaggioRepository(datastore)

    # SEGNALA UTENTE
    def segnala_utente(
        self,
        id_autore: str,
        id_utente_segnalato: str,
        motivo: str,
    ) -> Optional[Segnalazione]:

        # controlla che autore e segnalato esistano
        if not self.repo_utenti.get_by_id(id_autore):
            return None

        if not self.repo_utenti.get_by_id(id_utente_segnalato):
            return None

        id_segnalazione = str(uuid.uuid4())

        seg = Segnalazione(
            id=id_segnalazione,
            motivo=motivo,
            autore=id_autore,
            destinatario=id_utente_segnalato,
            stato=StatoSegnalazione.Inviata,
        )

        self.repo_segnalazioni.add(seg)
        salva_datastore(self.datastore)
        return seg

    # SEGNALA MESSAGGIO
    def segnala_messaggio(
        self,
        id_autore: str,
        id_messaggio: str,
        motivo: str,
    ) -> Optional[Segnalazione]:

        if not self.repo_utenti.get_by_id(id_autore):
            return None

        if not self.repo_messaggi.get_by_id(id_messaggio):
            return None

        id_segnalazione = str(uuid.uuid4())

        seg = Segnalazione(
            id=id_segnalazione,
            motivo=motivo,
            autore=id_autore,
            destinatario=id_messaggio,
            stato=StatoSegnalazione.Inviata,
        )

        self.repo_segnalazioni.add(seg)
        salva_datastore(self.datastore)
        return seg

    # CAMBIA STATO SEGNALAZIONE 
    def cambia_stato(
        self,
        admin: Utente,
        id_segnalazione: str,
        nuovo_stato: StatoSegnalazione,
    ) -> bool:

        if admin.ruoloPiattaforma != RolePlatform.ADMIN_PIATTAFORMA:
            return False

        seg = self.repo_segnalazioni.get_by_id(id_segnalazione)
        if not seg:
            return False

        seg.stato = nuovo_stato
        salva_datastore(self.datastore)
        return True

    # APPLICA SANZIONE
    def applica_sanzione(
        self,
        admin: Utente,
        id_segnalazione: str,
        tipo_sanzione: str,
        note: str,
    ) -> bool:

        if admin.ruoloPiattaforma != RolePlatform.ADMIN_PIATTAFORMA:
            return False

        seg = self.repo_segnalazioni.get_by_id(id_segnalazione)
        if not seg:
            return False

        seg.sanzione_tipo = tipo_sanzione
        seg.sanzione_note = note
        seg.stato = StatoSegnalazione.Archiviata

        salva_datastore(self.datastore)
        return True

    # LISTE DI SEGNALAZIONI PER STATO
    def segnalazioni_in_attesa(self) -> List[Segnalazione]:
        return [
            r
            for r in self.repo_segnalazioni.get_all()
            if r.stato == StatoSegnalazione.Inviata
        ]

    def segnalazioni_valutate(self) -> List[Segnalazione]:
        return [
            r
            for r in self.repo_segnalazioni.get_all()
            if r.stato == StatoSegnalazione.Valutata
        ]

    def segnalazioni_archiviate(self) -> List[Segnalazione]:
        return [
            r
            for r in self.repo_segnalazioni.get_all()
            if r.stato == StatoSegnalazione.Archiviata
        ]
