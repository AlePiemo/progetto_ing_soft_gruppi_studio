from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Materiale:
    id: str
    titolo: str
    contenuto: str
    autore: str          
    nome_file: str          
    dimensione: int         # in byte
    path_file: str          # percorso sul filesystem

    dataCaricamento: datetime = field(default_factory=datetime.now)
