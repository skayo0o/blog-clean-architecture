from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Comment:
    id: int
    post_id: int
    author_id: int
    content: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_deleted: bool = False
    parent_comment_id: Optional[int] = None  # For nested comments