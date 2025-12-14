from dataclasses import dataclass, field

@dataclass
class Chat:
    id: str
    messaggi: list[str] = field(default_factory=list) 
    partecipanti: list[str] = field(default_factory=list) 