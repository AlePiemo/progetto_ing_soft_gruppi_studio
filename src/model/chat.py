from dataclasses import dataclass, field

@dataclass
class Chat:
    id: int
    messaggi: list[int] = field(default_factory=list) 
    partecipanti: list[int] = field(default_factory=list) 
