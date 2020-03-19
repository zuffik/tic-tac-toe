import numpy as np

"""
Symbols for cell:
0 - nobody
1 - X
2 - O

Symbols for game state:
-1 - in progress
0 - draw
1 - X
2 - 0
"""


class Game:
    def __init__(self, size=10, requiredToWin=3) -> None:
        super().__init__()
        self._requiredToWin = requiredToWin
        self._size = size
        self._board = np.zeros(size, size)

    def validMoves(self):
        result = []
        for i in range(self._size):
            for j in range(i, self._size):
                if self._board[i][j] == 0:
                    result.append((i, j))
        return result

    def winner(self):
        for i in range(self._size):
            possibleWinnerForRow = 0
            possibleWinnerForCol = 0
            possibleWinnerForPrimaryDiagonal = 0
            possibleWinnerForSecondaryDiagonal = 0
            for j in range(self._size):
                if self._board[i][j] == 0:
                    break



