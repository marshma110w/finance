from fastapi import FastAPI
from pydantic import BaseModel
from logging import Logger

logger = Logger(__name__)


app = FastAPI()

class User(BaseModel):
    tg_id: int
    name: str


@app.post("/new_user")
def new_user(user: User):
    logger.warning(f"New user here: {user}")
    return "OK"
