from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import EmailStr, BaseModel

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

class UserBase(SQLModel):
    username: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

class User(UserBase, table=True):
    __tablename__="users"
    id: int | None = Field(primary_key=True, default=None)

class UserCreate(UserBase):
    pass

class UserPublic(UserBase):
    id: int

class UserUpdate(UserBase):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
