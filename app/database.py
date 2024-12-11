from sqlmodel import SQLModel, create_engine, Session

engine = create_engine("mysql+mysqlconnector://root:itsokay03@localhost/MyDB")

def init_db():
    SQLModel.metadata.create_all(engine)

# def get_session():
#     with Session(engine) as session:
#         yield session