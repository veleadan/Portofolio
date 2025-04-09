from pydantic import BaseModel
from typing import List, Optional

# Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str


class Client(BaseModel):
    user_id: int
    username: str


class Move(BaseModel):
    row: int
    col: int

