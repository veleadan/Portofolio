from sqlalchemy import Text, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import json
from data import Base


# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    games = relationship("GameState", back_populates="owner")

class GameState(Base):
    __tablename__ = "game_state"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    board = Column(Text, default=json.dumps([[" " for _ in range(3)] for _ in range(3)]))
    current_player = Column(String)
    owner = relationship("User", back_populates="games")
