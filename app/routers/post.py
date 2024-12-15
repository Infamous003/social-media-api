from fastapi import status, HTTPException, APIRouter
from ..models import Post, PostPublic, PostCreate, PostUpdate
from sqlmodel import Session, select
from ..database import engine

router = APIRouter()

# GET posts
@router.get("/posts", status_code=status.HTTP_200_OK, response_model=list[Post])
def get_posts():
    with Session(engine) as session:
        statement = select(Post)
        result = session.exec(statement)
        posts = result.fetchall()
        return posts

# GET post
@router.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=PostPublic)
def get_post(id: int):

    with Session(engine) as session:
        statement = select(Post).where(Post.id == id)
        result = session.exec(statement)
        post = result.one_or_none()
        
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"post with id: {id} not found")
        return post


# CREATE posts
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostPublic)
def create_post(post: PostCreate):

    if not post.title or not post.content:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Title and content are required")

    new_post = Post(**post.model_dump())
    with Session(engine) as session:
        session.add(new_post)
        session.commit()
        session.refresh(new_post)

    return new_post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    with Session(engine) as session:
        statement = select(Post).where(Post.id == id)
        result = session.exec(statement)
        post = result.one_or_none()
        
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

        session.delete(post)
        session.commit()
    
@router.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=PostPublic)
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
    