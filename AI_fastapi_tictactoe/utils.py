from typing import List, Optional, Tuple

class Board:


    def __init__(self, board: Optional[List[List[str]]] = None):
        self.board = board or [[" " for _ in range(3)] for _ in range(3)]

    def display(self) -> List[List[str]]:
        return self.board

    def is_full(self) -> bool:
        return all(cell != " " for row in self.board for cell in row)

    def check_winner(self) -> Optional[str]:
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != " ":
                return row[0]

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != " ":
                return self.board[0][col]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != " ":
            return self.board[0][2]

        return None

    def make_move(self, row: int, col: int, player: str) -> bool:
        if self.board[row][col] == " ":
            self.board[row][col] = player
            return True
        return False


# TicTacToe game management
class TicTacToe:
    def __init__(self, board: Optional[List[List[str]]] = None, current_player: str = "X"):
        self.board = Board(board)
        self.current_player = current_player

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def minimax(self, depth: int, is_maximizing: bool) -> int:
        winner = self.board.check_winner()
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif self.board.is_full():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board.board[i][j] == " ":
                        self.board.board[i][j] = "O"
                        score = self.minimax(depth + 1, False)
                        self.board.board[i][j] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board.board[i][j] == " ":
                        self.board.board[i][j] = "X"
                        score = self.minimax(depth + 1, True)
                        self.board.board[i][j] = " "
                        best_score = min(score, best_score)
            return best_score

    def find_best_move(self) -> Optional[Tuple[int, int]]:
        best_move = None
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if self.board.board[i][j] == " ":
                    self.board.board[i][j] = "O"
                    score = self.minimax(0, False)
                    self.board.board[i][j] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        return best_move

