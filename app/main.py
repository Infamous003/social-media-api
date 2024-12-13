from fastapi import FastAPI, status, HTTPException, Response
from sqlmodel import Session, select
from .models import Post, PostPublic, PostCreate, PostUpdate, User, UserCreate, UserUpdate, UserPublic
from .database import init_db, engine
from contextlib import asynccontextmanager
from bcrypt import hashpw, gensalt

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"Welcome": "to Blog"}

# GET posts
@app.get("/posts", status_code=status.HTTP_200_OK, response_model=list[Post])
def get_posts():
    with Session(engine) as session:
        statement = select(Post)
        result = session.exec(statement)
        posts = result.fetchall()
        return posts

# GET post
@app.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=PostPublic)
def get_post(id: int):

    with Session(engine) as session:
        statement = select(Post).where(Post.id == id)
        result = session.exec(statement)
        post = result.one_or_none()
        
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"post with id: {id} not found")
        return post


# CREATE posts
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostPublic)
def create_post(post: PostCreate):

    if not post.title or not post.content:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Title and content are required")

    new_post = Post(**post.model_dump())
    with Session(engine) as session:
        session.add(new_post)
        session.commit()
        session.refresh(new_post)

    return new_post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    with Session(engine) as session:
        statement = select(Post).where(Post.id == id)
        result = session.exec(statement)
        post = result.one_or_none()
        
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

        session.delete(post)
        session.commit()
    
@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=PostPublic)
def update_post(id: int, post: PostUpdate):

    with Session(engine) as session:
        statement = select(Post).where(Post.id == id)
        result = session.exec(statement)
        post_to_update = result.one_or_none()

        if not post_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        post_data = post.model_dump(exclude_defaults=True)
        
        post_to_update.sqlmodel_update(post_data)
        session.add(post_to_update)
        session.commit()
        session.refresh(post_to_update)

        return post_to_update
    
# ----------Users----------

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
def create_user(user: UserCreate):

    if not user.username or not user.password or not user.email:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="username, email and password are required")
    user.password = hashpw(user.password.encode('utf-8'), gensalt(14))
    new_user = User(**user.model_dump())

    with Session(engine) as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return new_user

@app.get("/users", status_code=status.HTTP_200_OK, response_model=list[UserPublic])
def get_users():
    with Session(engine) as session:
        statement = select(User)
        users = session.exec(statement).fetchall()
        return users
    
@app.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=UserPublic)
def get_user(id: int):
    with Session(engine) as session:
        statement = select(User).where(User.id == id)
        user = session.exec(statement).one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
        return user   
    
@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    with Session(engine) as session:
        statement = select(User).where(User.id == id)
        user = session.exec(statement).one_or_none()
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
        session.delete(user)
        session.commit()

@app.put("/users/{id}", status_code=status.HTTP_200_OK, response_model=UserPublic)
def update_user(id: int, user: UserUpdate):
    with Session(engine) as session:
        statement = select(User).where(User.id == id)
        user_to_update = session.exec(statement).one_or_none()

        if not user_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
        user_data = user.model_dump(exclude_unset=True)
        user_to_update.sqlmodel_update(user_data)
        session.add(user_to_update)
        session.commit()
        session.refresh(user_to_update)
        return user_to_update