from fastapi import HTTPException, Depends, status, Request
from typing import Optional
from sqlalchemy.orm import Session
from data import get_db
from schema import UserCreate, Client
from models import User, GameState
import json


# Utility functions

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate) -> Client:
    db_user = get_user_by_username(db, user.username)
    if db_user is not None:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Creează starea jocului cu tabloul serializat ca JSON
    db_game_state = GameState(user_id=db_user.id, board=json.dumps([[" " for _ in range(3)] for _ in range(3)]),
                              current_player="X")
    db.add(db_game_state)
    db.commit()
    db.refresh(db_game_state)
    return Client(user_id=db_user.id, username=db_user.username)


def get_game_state(db: Session, user_id: int, game_id: int) -> Optional[GameState]:
    return db.query(GameState).filter(GameState.user_id == user_id, GameState.id == game_id).first()

# Authenticated User dependency
def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user

