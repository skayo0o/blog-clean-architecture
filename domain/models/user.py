from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    id: int
    username: str
    email: str
    registered_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True
