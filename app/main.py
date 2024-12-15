from fastapi import FastAPI
from .database import init_db
from contextlib import asynccontextmanager
from .routers import post, user

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def home():
    return {"Welcome": "to Blog"}
