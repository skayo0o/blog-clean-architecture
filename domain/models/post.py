from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Post:
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "draft"  # "draft" or "published"
    tags: List[str] = field(default_factory=list)
    comments_count: int = 0