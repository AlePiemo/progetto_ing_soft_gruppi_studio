from __future__ import annotations
import os
import pickle
import uuid
from datetime import datetime
from typing import Optional

from persistence.datastore import DataStore, salva_datastore
from persistence.repositories import BackupRepository
from model.backup import Backup, BackupStatus


class BackupService:
    def __init__(self, datastore: DataStore):
        self.datastore = datastore
        self.repo_backup = BackupRepository(datastore)

        # cartella dei backup
        self.cartella = os.path.join("data", "backup")
        os.makedirs(self.cartella, exist_ok=True)

    # BACKUP AUTOMATICO
    def backup_automatico(self) -> Backup:

        timestamp = datetime.now()
        filename = f"backup_auto_{timestamp.strftime('%Y%m%d_%H%M%S')}.pkl"
        path = os.path.join(self.cartella, filename)

        # genera id backup
        id_backup = str(uuid.uuid4())

        # stato iniziale
        info = Backup(
            id=id_backup,
            dataBackup=timestamp,
            statoBackup=BackupStatus.In_corso,
            esito=False
        )

        try:
            with open(path, "wb") as f:
                pickle.dump(self.datastore, f)

            info.esito = True

        except Exception:
            info.esito = False

        # fine backup
        info.statoBackup = BackupStatus.Completato

        self.repo_backup.add(info)
        salva_datastore(self.datastore)

        return info
    
    # BACKUP MANUALE
    def backup_manuale(self) -> Backup:
        timestamp = datetime.now()
        filename = f"backup_manual_{timestamp.strftime('%Y%m%d_%H%M%S')}.pkl"
        path = os.path.join(self.cartella, filename)

        id_backup = str(uuid.uuid4())

        info = Backup(
            id=id_backup,
            dataBackup=timestamp,
            statoBackup=BackupStatus.In_corso,
            esito=False
        )

        try:
            with open(path, "wb") as f:
                pickle.dump(self.datastore, f)
            info.esito = True

        except Exception:
            info.esito = False

        info.statoBackup = BackupStatus.Completato

        self.repo_backup.add(info)
        salva_datastore(self.datastore)

        return info

    # LISTA TUTTI I BACKUP
    def lista_backup(self):
        return self.repo_backup.get_all()
