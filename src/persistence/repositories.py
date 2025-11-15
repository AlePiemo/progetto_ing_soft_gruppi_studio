from __future__ import annotations
from typing import List, Optional

from .datastore import DataStore

from model.utente import Utente
from model.gruppo import Gruppo
from model.messaggio import Messaggio   
from model.incontro import Incontro
from model.materiale import Materiale
from model.segnalazione import Segnalazione
from model.notifica import Notifica
from model.backup import Backup
from model.chat import Chat
from model.calendario import Calendario

#  Utente REPOSITORY
class UtenteRepository:
    def __init__(self, datastore: DataStore):
        self._ds = datastore

    def add(self, utente: Utente) -> None:
        self._ds.users[utente.id] = utente

    def get_by_id(self, utente_id: int) -> Optional[Utente]:
        return self._ds.users.get(utente_id)

    def get_all(self) -> List[Utente]:
        return list(self._ds.users.values())

    def remove(self, utente_id: int) -> None:
        self._ds.users.pop(utente_id, None)

    def find_by_email(self, email: str) -> Optional[Utente]:
        for u in self._ds.users.values():
            if u.email == email:
                return u
        return None

#  Gruppo REPOSITORY
class GruppoRepository:
    def __init__(self, datastore: DataStore):
        self._ds = datastore

    def add(self, gruppo: Gruppo) -> None:
        self._ds.gruppi[gruppo.id] = gruppo

    def get_by_id(self, gruppo_id: str) -> Optional[Gruppo]:
        return self._ds.gruppi.get(gruppo_id)
    
    def get_all(self) -> List[Gruppo]:
        return list(self._ds.gruppi.values())

    def remove(self, gruppo_id: str) -> None:
        self._ds.gruppi.pop(gruppo_id, None)

#  Messaggio REPOSITORY
class MessaggioRepository:
    def __init__(self, datastore: DataStore):
        self._ds = datastore

    def add(self, messaggio: Messaggio) -> None:
        self._ds.messaggi[messaggio.id] = messaggio

    def get_by_id(self, messaggio_id: str) -> Optional[Messaggio]:
        return self._ds.messaggi.get(messaggio_id)

    def get_all(self) -> List[Messaggio]:
        return list(self._ds.messaggi.values())

    def remove(self, messaggio_id: str) -> None:
        self._ds.messaggi.pop(messaggio_id, None)

    def get_by_group(self, gruppo_id: str) -> List[Messaggio]:
        return [m for m in self._ds.messaggi.values() if m.destinatario_id == gruppo_id]

#  Incontro REPOSITORY
class IncontroRepository:
    def __init__(self, datastore: DataStore):
        self._ds = datastore

    def add(self, incontro: Incontro) -> None:
        self._ds.incontri[incontro.id] = incontro

    def get_by_id(self, incontro_id: str) -> Optional[Incontro]:
        return self._ds.incontri.get(incontro_id)

    def get_all(self) -> List[Incontro]:
        return list(self._ds.incontri.values())

    def remove(self, incontro_id: str) -> None:
        self._ds.incontri.pop(incontro_id, None)

    def get_by_group(self, gruppo_id: str) -> List[Incontro]:
        return [m for m in self._ds.incontri.values() if m.gruppo_id == gruppo_id]

#  Materiale REPOSITORY
class MaterialeRepository:
    def __init__(self, datastore: DataStore):
        self._ds = datastore

    def add(self, material: Materiale) -> None:
        self._ds.materiali[material.id] = material

    def get_by_id(self, material_id: str) -> Optional[Materiale]:
        return self._ds.materiali.get(material_id)

    def get_all(self) -> List[Materiale]:
        return list(self._ds.materiali.values())

    def remove(self, material_id: str) -> None:
        self._ds.materiali.pop(material_id, None)

    def get_by_group(self, gruppo_id: str) -> List[Materiale]:
        return [m for m in self._ds.materiali.values() if m.gruppo_id == gruppo_id]

#  Segnalazione REPOSITORY
class SegnalazioneRepository:
    def __init__(self, datastore: DataStore):
        self._ds = datastore

    def add(self, segnalazione: Segnalazione) -> None:
        self._ds.segnalazioni[segnalazione.id] = segnalazione

    def get_by_id(self, segnalazione_id: str) -> Optional[Segnalazione]:
        return self._ds.segnalazioni.get(segnalazione_id)

    def get_all(self) -> List[Segnalazione]:
        return list(self._ds.segnalazioni.values())

    def remove(self, segnalazione_id: str) -> None:
        self._ds.segnalazioni.pop(segnalazione_id, None)

    def get_by_status(self, status) -> List[Segnalazione]:
        return [r for r in self._ds.segnalazioni.values() if r.stato == status]

#  Notifica REPOSITORY
class NotificaRepository:
    def __init__(self, datastore: DataStore):
        self._ds = datastore

    def add(self, notifica: Notifica) -> None:
        self._ds.notifiche[notifica.id] = notifica

    def get_by_id(self, notifica_id: str) -> Optional[Notifica]:
        return self._ds.notifiche.get(notifica_id)

    def get_all(self) -> List[Notifica]:
        return list(self._ds.notifiche.values())

    def remove(self, notifica_id: str) -> None:
        self._ds.notifiche.pop(notifica_id, None)

    def get_by_user(self, user_id: str) -> List[Notifica]:
        return [n for n in self._ds.notifiche.values() if n.destinatario_id == user_id]

#  BACKUP REPOSITORY
class BackupRepository:
    def __init__(self, datastore: DataStore):
        self._ds = datastore

    def add(self, backup: Backup) -> None:
        self._ds.backups[backup.id] = backup

    def get_by_id(self, backup_id: str) -> Optional[Backup]:
        return self._ds.backups.get(backup_id)

    def get_all(self) -> List[Backup]:
        return list(self._ds.backups.values())

    def remove(self, backup_id: str) -> None:
        self._ds.backups.pop(backup_id, None)

#  Chat REPOSITORY
class ChatRepository:
    def __init__(self, datastore: DataStore):
        self._ds = datastore

    def add(self, chat: Chat) -> None:
        self._ds.chats[chat.id] = chat

    def get_by_id(self, chat_id: str) -> Optional[Chat]:
        return self._ds.chats.get(chat_id)

    def get_all(self) -> List[Chat]:
        return list(self._ds.chats.values())

    def remove(self, chat_id: str) -> None:
        self._ds.chats.pop(chat_id, None)

#  Calendario REPOSITORY
class CalendarioRepository:
    def __init__(self, datastore: DataStore):
        self._ds = datastore

    def add(self, calendario: Calendario) -> None:
        self._ds.calendars[calendario.id] = calendario

    def get_by_id(self, calendario_id: str) -> Optional[Calendario]:
        return self._ds.calendars.get(calendario_id)

    def get_all(self) -> List[Calendario]:
        return list(self._ds.calendars.values())

    def remove(self, calendario_id: str) -> None:
        self._ds.calendars.pop(calendario_id, None)
