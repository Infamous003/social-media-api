from fastapi import status, HTTPException, APIRouter
from ..models import UserUpdate, User, UserPublic
from bcrypt import hashpw, gensalt
from sqlmodel import Session, select
from ..database import engine

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
def create_user(user: User):

    if not user.username or not user.password or not user.email:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="username, email and password are required")
    user.password = hashpw(user.password.encode('utf-8'), gensalt(14))
    new_user = User(**user.model_dump())

    with Session(engine) as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return new_user

@router.get("/users", status_code=status.HTTP_200_OK, response_model=list[UserPublic])
def get_users():
    with Session(engine) as session:
        statement = select(User)
        users = session.exec(statement).fetchall()
        return users
    
@router.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=UserPublic)
def get_user(id: int):
    with Session(engine) as session:
        statement = select(User).where(User.id == id)
        user = session.exec(statement).one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
        return user   
    
@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    with Session(engine) as session:
        statement = select(User).where(User.id == id)
        user = session.exec(statement).one_or_none()
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
        session.delete(user)
        session.commit()

@router.put("/users/{id}", status_code=status.HTTP_200_OK, response_model=UserPublic)
def update_user(id: int, user: UserUpdate):
    with Session(engine) as session:
        statement = select(User).where(User.id == id)
        user_to_update = session.exec(statement).one_or_none()

        if not user_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
        if user.password:
            user.password= hashpw(user.password.encode("utf-8"), gensalt(14))
        user_data = user.model_dump(exclude_unset=True)
        user_to_update.sqlmodel_update(user_data)
        session.add(user_to_update)
        session.commit()
        session.refresh(user_to_update)
        return user_to_update