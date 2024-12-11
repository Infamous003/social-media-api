from sqlmodel import SQLModel, Field
from datetime import datetime

class PostBase(SQLModel):
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    isPublished: bool = True
    ratings: float = 0.0
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

class Post(PostBase, table=True):
    __tablename__ = "post"
    id: int | None = Field(default=None, primary_key=True)

class PostPublic(PostBase):
    id: int

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    title: str | None = None
    content: str | None = None
    isPublished: bool | None = None
    ratings: float | None = None
    created_at: datetime | None = None
