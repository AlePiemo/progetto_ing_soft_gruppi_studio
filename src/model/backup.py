from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class BackupStatus(Enum):
    In_corso = "In_corso"
    Completato = "Completato"

@dataclass
class Backup:
    id: str
    dataBackup: datetime
    esito: bool            

    statoBackup: BackupStatus
