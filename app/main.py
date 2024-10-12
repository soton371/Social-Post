from fastapi import FastAPI
from .config import settings
from . import models
from .database import engine
from .routers import post, user, auth

print(f"se database_password: {settings.database_password}")

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 8:15
