from fastapi import FastAPI, HTTPException, Depends, status, Request
from sqlalchemy.orm import Session
import json, models
from schema import UserCreate, Move, Client
from crud import get_current_user, get_user_by_username, create_user, get_game_state,get_db
from starlette.middleware.sessions import SessionMiddleware
from fastapi.openapi.utils import get_openapi
from data import engine
from models import User, GameState
from utils import TicTacToe

models.Base.metadata.create_all(bind=engine)
app = FastAPI()  # O singură instanță de FastAPI

# Add session middleware for handling sessions (using a secure random secret key)
app.add_middleware(SessionMiddleware, secret_key="supersecretkey123")



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    # Generăm schema OpenAPI implicită
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="API description",
        routes=app.routes
    )

    # Asigură-te că 'components' există în schema generată
    if "components" in openapi_schema:
        # Eliminăm secțiunea de 'securitySchemes'
        openapi_schema["components"].pop("securitySchemes", None)

    # Eliminăm securitatea globală, dacă a fost setată
    openapi_schema.pop("security", None)

    # Salvăm schema OpenAPI modificată
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Aplicăm funcția customizată pentru OpenAPI la aplicația FastAPI
app.openapi = custom_openapi


@app.post("/login")
def login(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user is None or db_user.password != user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    request.session['user_id'] = db_user.id  # Set user_id in session

    games = db.query(GameState).filter(GameState.user_id == db_user.id).all()
    game_list = [{"game_id": game.id, "board": json.loads(game.board), "current_player": game.current_player} for game in games]

    return {"message": "Login successful", "games": game_list}


@app.post("/logout")
def logout(request: Request):
    request.session.clear()  # Clear session
    return {"message": "Logout successful"}

# Protected endpoints

@app.post("/register", response_model=Client)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@app.get("/run-game/{game_id}", tags=["Games"], summary="Run a game")
def run_game(game_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Obține starea jocului din baza de date
    db_game_state = get_game_state(db, current_user.id, game_id)

    # Dacă nu există o stare a jocului, creează una nouă
    if not db_game_state:
        new_board = [[" " for _ in range(3)] for _ in range(3)]
        db_game_state = GameState(user_id=current_user.id, board=json.dumps(new_board), current_player="X")
        db.add(db_game_state)
        db.commit()
        db.refresh(db_game_state)

    # Deserializare a tabloului de joc
    board = json.loads(db_game_state.board)  # Asigură-te că tabloul se deserializează corect

    # Crearea obiectului TicTacToe
    game = TicTacToe(board=board, current_player=db_game_state.current_player)

    # Returnarea tabloului și a jucătorului curent
    return {"board": game.board.display(), "current_player": game.current_player}


@app.post("/move/{game_id}", tags=["Games"], summary="Make a move")
def make_move(game_id: int, move: Move, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_game_state = get_game_state(db, current_user.id, game_id)
    if not db_game_state:
        raise HTTPException(status_code=404, detail="Game not found")

    board = json.loads(db_game_state.board)
    game = TicTacToe(board=board, current_player=db_game_state.current_player)

    # Verificarea coordonatelor mutării
    if not (0 <= move.row < 3 and 0 <= move.col < 3):
        return {"error": "Invalid move coordinates", "board": game.board.display(),
                "current_player": game.current_player}

    # Efectuarea mutării
    if not game.board.make_move(move.row, move.col, game.current_player):
        return {"error": "Cell already occupied", "board": game.board.display(), "current_player": game.current_player}

    # Verificarea câștigătorului
    winner = game.board.check_winner()
    if winner:
        db_game_state.board = json.dumps(game.board.display())  # Salvăm tabloul ca JSON
        db.commit()
        return {"board": game.board.display(), "winner": winner}

    # Verificarea dacă tabloul este plin
    if game.board.is_full():
        db_game_state.board = json.dumps(game.board.display())  # Salvăm tabloul ca JSON
        db.commit()
        return {"board": game.board.display(), "winner": "Tie"}

    # Schimbarea jucătorului
    game.switch_player()

    # Mutarea AI-ului
    ai_move = game.find_best_move()
    if ai_move:
        game.board.make_move(ai_move[0], ai_move[1], game.current_player)

    # Verificarea câștigătorului din nou
    winner = game.board.check_winner()
    if winner:
        db_game_state.board = json.dumps(game.board.display())  # Salvăm tabloul ca JSON
        db.commit()
        return {"board": game.board.display(), "winner": winner}

    # Verificarea dacă tabloul este plin din nou
    if game.board.is_full():
        db_game_state.board = json.dumps(game.board.display())  # Salvăm tabloul ca JSON
        db.commit()
        return {"board": game.board.display(), "winner": "Tie"}

    # Salvăm tabloul și jucătorul curent
    db_game_state.board = json.dumps(game.board.display())  # Salvăm tabloul ca JSON
    db_game_state.current_player = game.current_player
    db.commit()

    return {"board": game.board.display(), "winner": None}



@app.get("/board/{game_id}", tags=["Games"], summary="Get board state")
def get_board(game_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_game_state = get_game_state(db, current_user.id, game_id)
    if not db_game_state:
        raise HTTPException(status_code=404, detail="Game not found")

    board = json.loads(db_game_state.board)
    return {"board": board}

@app.delete("/delete-user", tags=["User Management"], summary="Delete user")
def delete_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(GameState).filter(GameState.user_id == current_user.id).delete()
    db.delete(current_user)
    db.commit()
    return {"message": "User and associated game states deleted successfully"}

@app.post("/reset/{game_id}", tags=["Games"], summary="Reset game")
def reset_game(game_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_game_state = get_game_state(db, current_user.id, game_id)
    if not db_game_state:
        raise HTTPException(status_code=404, detail="Game not found")

    # Resetează tabloul și jucătorul curent
    db_game_state.board = json.dumps([[" " for _ in range(3)] for _ in range(3)])  # Corectare aici
    db_game_state.current_player = "X"
    db.commit()
    return {"message": "Game reset successfully"}

@app.post("/new-game", tags=["Games"], summary="Start a new game")
def start_new_game(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Crearea unei noi instanțe de GameState pentru utilizatorul curent
    new_board = [[" " for _ in range(3)] for _ in range(3)]
    db_game_state = GameState(user_id=current_user.id, board=json.dumps(new_board), current_player="X")
    db.add(db_game_state)
    db.commit()
    db.refresh(db_game_state)

    return {"message": "New game created", "game_id": db_game_state.id, "board": new_board, "current_player": "X"}


@app.get("/my-games", tags=["Games"], summary="Get all active games for the current user")
def get_all_games(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    games = db.query(GameState).filter(GameState.user_id == current_user.id).all()

    if not games:
        return {"message": "No active games"}

    game_list = [{"game_id": game.id, "board": json.loads(game.board), "current_player": game.current_player} for game
                 in games]

    return {"games": game_list}

@app.delete("/delete-game/{game_id}", tags=["Games"], summary="Delete a specific game")
def delete_game(game_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Find the game for the current user by its game_id
    db_game_state = get_game_state(db, current_user.id, game_id)
    if not db_game_state:
        raise HTTPException(status_code=404, detail="Game not found")

    # Delete the game from the database
    db.delete(db_game_state)
    db.commit()

    return {"message": f"Game {game_id} deleted successfully"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)