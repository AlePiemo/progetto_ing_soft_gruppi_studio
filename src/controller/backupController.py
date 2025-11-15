from __future__ import annotations
from typing import List, Optional

from persistence.datastore import DataStore
from persistence.repositories import BackupRepository
from services.backupService import BackupService
from model.backup import Backup


class BackupController:

    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_backup = BackupRepository(datastore)
        self.service = BackupService(datastore)

    # ESEGUI BACKUP MANUALE
    def backup_manuale(self) -> Backup:
        return self.service.backup_manuale()

    # ESEGUI BACKUP AUTOMATICO 
    def backup_automatico(self) -> Backup:
        return self.service.backup_automatico()

    # LISTA BACKUP SALVATI
    def lista_backup(self) -> List[Backup]:
        return self.service.lista_backup()

    # OTTIENI DETTAGLI BACKUP
    def get_backup(self, id_backup: str) -> Optional[Backup]:
        return self.repo_backup.get_by_id(id_backup)
