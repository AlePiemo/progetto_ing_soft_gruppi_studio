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

    def get_by_id(self, utente_id: str) -> Optional[Utente]:
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
        self._ds.groups[gruppo.id] = gruppo

    def get_by_id(self, gruppo_id: str) -> Optional[Gruppo]:
        return self._ds.groups.get(gruppo_id)
    
    def get_all(self) -> List[Gruppo]:
        return list(self._ds.groups.values())

    def remove(self, gruppo_id: str) -> None:
        self._ds.groups.pop(gruppo_id, None)

#  Messaggio REPOSITORY
class MessaggioRepository:
    def __init__(self, datastore: DataStore):
        self._ds = datastore

    def add(self, messaggio: Messaggio) -> None:
        self._ds.messages[messaggio.id] = messaggio

    def get_by_id(self, messaggio_id: str) -> Optional[Messaggio]:
        return self._ds.messages.get(messaggio_id)

    def get_all(self) -> List[Messaggio]:
        return list(self._ds.messages.values())

    def remove(self, messaggio_id: str) -> None:
        self._ds.messages.pop(messaggio_id, None)

#  Incontro REPOSITORY
class IncontroRepository:
    def __init__(self, datastore: DataStore):
        self._ds = datastore

    def add(self, incontro: Incontro) -> None:
        self._ds.meetings[incontro.id] = incontro

    def get_by_id(self, incontro_id: str) -> Optional[Incontro]:
        return self._ds.meetings.get(incontro_id)

    def get_all(self) -> List[Incontro]:
        return list(self._ds.meetings.values())

    def remove(self, incontro_id: str) -> None:
        self._ds.meetings.pop(incontro_id, None)

    def get_by_group(self, gruppo_id: str) -> List[Incontro]:
        return [m for m in self._ds.meetings.values() if m.gruppo_id == gruppo_id]

#  Materiale REPOSITORY
class MaterialeRepository:
    def __init__(self, datastore: DataStore):
        self._ds = datastore

    def add(self, material: Materiale) -> None:
        self._ds.materials[material.id] = material

    def get_by_id(self, material_id: str) -> Optional[Materiale]:
        return self._ds.materials.get(material_id)

    def get_all(self) -> List[Materiale]:
        return list(self._ds.materials.values())

    def remove(self, material_id: str) -> None:
        self._ds.materials.pop(material_id, None)

#  Segnalazione REPOSITORY
class SegnalazioneRepository:
    def __init__(self, datastore: DataStore):
        self._ds = datastore

    def add(self, segnalazione: Segnalazione) -> None:
        self._ds.reports[segnalazione.id] = segnalazione

    def get_by_id(self, segnalazione_id: str) -> Optional[Segnalazione]:
        return self._ds.reports.get(segnalazione_id)

    def get_all(self) -> List[Segnalazione]:
        return list(self._ds.reports.values())

    def remove(self, segnalazione_id: str) -> None:
        self._ds.reports.pop(segnalazione_id, None)

    def get_by_status(self, status) -> List[Segnalazione]:
        return [r for r in self._ds.reports.values() if r.stato == status]

#  Notifica REPOSITORY
class NotificaRepository:
    def __init__(self, datastore: DataStore):
        self._ds = datastore

    def add(self, notifica: Notifica) -> None:
        self._ds.notifications[notifica.id] = notifica

    def get_by_id(self, notifica_id: str) -> Optional[Notifica]:
        return self._ds.notifications.get(notifica_id)

    def get_all(self) -> List[Notifica]:
        return list(self._ds.notifications.values())

    def remove(self, notifica_id: str) -> None:
        self._ds.notifications.pop(notifica_id, None)

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
