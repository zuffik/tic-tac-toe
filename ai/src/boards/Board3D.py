from typing import List, Tuple, Union, TypeVar

import numpy as np
import pydash as _

from boards.Board2D import Board2DOperations
from boards.IBoard import IBoard
from common.Convert import toDec
from common.Defs import Cell, Winner

Board3D = List[List[List[Cell]]]

Rows = TypeVar('Rows')
BoardDiagonals = TypeVar('BoardDiagonals')
SpaceDiagonals = TypeVar('SpaceDiagonals')
IndexEnum = Union[Rows, BoardDiagonals, SpaceDiagonals]


class Board3DOperations(IBoard[Board3D]):
    def __init__(self):
        self._operations2D = Board2DOperations()

    def createBoard(self, size: int = 3) -> Board3D:
        return [[['E' for _ in range(size)] for _ in range(size)] for _ in range(size)]

    def boardToString(self, board: Board3D) -> str:
        def rowDelim(size: int) -> str:
            r: str = '+'
            for _ in board:
                r += '-' * size + '+'
            return r + '\n'

        size = len(board)
        result: str = rowDelim(size)
        for i in range(size):
            wall = board[i]
            for j in range(len(wall)):
                row = wall[j]
                result += '|'
                for k in range(len(row)):
                    cell = row[k]
                    result += cell
            result += '|\n'
            result += rowDelim(size)
        return result

    def getBoardWinner(self, board: Board3D, toWin: int) -> Winner:
        # this is just for helpings
        if len(board) != len(board[0]):
            for i in range(len(board)):
                winner = self._operations2D.getBoardWinner(board[i], toWin)
                if winner != 'Draw':
                    return winner
            return 'Draw'

        return self._checkForWinnerRecursively(board, toWin, 0, 0, 0, [])

    def _checkForWinnerRecursively(self, board: Board3D, toWin: int, x: int, y: int, z: int,
                                   checked: List[Tuple[int, int, int]]) -> Winner:
        size = len(board)
        if x + toWin > size or y + toWin > size or z + toWin > size:
            return 'Draw'
        winner = self._getBoardWinner(board, toWin, x, y, z) if (x, y, z) not in checked else 'Draw'
        checked.append((x, y, z))
        if winner != 'Draw':
            return winner

        winner = self._checkForWinnerRecursively(board, toWin, x + 1, y, z, checked)
        if winner != 'Draw':
            return winner

        winner = self._checkForWinnerRecursively(board, toWin, x, y + 1, z, checked)
        if winner != 'Draw':
            return winner

        winner = self._checkForWinnerRecursively(board, toWin, x, y, z + 1, checked)
        if winner != 'Draw':
            return winner

        winner = self._checkForWinnerRecursively(board, toWin, x + 1, y, z + 1, checked)
        if winner != 'Draw':
            return winner

        winner = self._checkForWinnerRecursively(board, toWin, x + 1, y + 1, z, checked)
        if winner != 'Draw':
            return winner

        winner = self._checkForWinnerRecursively(board, toWin, x, y + 1, z + 1, checked)
        if winner != 'Draw':
            return winner

        winner = self._checkForWinnerRecursively(board, toWin, x + 1, y + 1, z + 1, checked)
        if winner != 'Draw':
            return winner

        return 'Draw'

    # check for winner in {toWin X toWin X toWin} cube
    def _getBoardWinner(self, board: Board3D, toWin: int, x: int, y: int, z: int) -> Winner:
        possibilities = np.full((toWin ** 3 * 3 + 4, toWin), ord('E'))

        for i in range(x, x + toWin):
            for j in range(y, y + toWin):
                for k in range(z, z + toWin):
                    # rows
                    index = self._possibilitiesIndex(Rows, toWin, i, j, 0)
                    possibilities[index][k - z] = ord(board[i][j][k])
                    index = self._possibilitiesIndex(Rows, toWin, i, 0, k)
                    possibilities[index][j - y] = ord(board[i][j][k])
                    index = self._possibilitiesIndex(Rows, toWin, 0, j, k)
                    possibilities[index][i - x] = ord(board[i][j][k])

                    # LTR diagonals
                    index = self._possibilitiesIndex(BoardDiagonals, toWin, i, j, 0)
                    possibilities[index][k - z] = ord(board[i][k][k])
                    index = self._possibilitiesIndex(BoardDiagonals, toWin, i, 0, k)
                    possibilities[index][j - y] = ord(board[j][j][k])
                    index = self._possibilitiesIndex(BoardDiagonals, toWin, 0, j, k)
                    possibilities[index][i - x] = ord(board[i][j][i])

                    # RTL diagonals
                    index = self._possibilitiesIndex(BoardDiagonals, toWin, i, j, 0, 1)
                    possibilities[index][k - z] = ord(board[i][k][toWin - k - 1])
                    index = self._possibilitiesIndex(BoardDiagonals, toWin, i, 0, k, 1)
                    possibilities[index][j - y] = ord(board[j][toWin - j - 1][k])
                    index = self._possibilitiesIndex(BoardDiagonals, toWin, 0, j, k, 1)
                    possibilities[index][i - x] = ord(board[toWin - i - 1][j][i])

            # space diagonals
            index = self._possibilitiesIndex(SpaceDiagonals, toWin, 0, 0, 0, 0)
            possibilities[index][i - x] = ord(board[i][i][i])
            index = self._possibilitiesIndex(SpaceDiagonals, toWin, 0, 0, 0, 1)
            possibilities[index][i - x] = ord(board[toWin - i - 1][i][i])
            index = self._possibilitiesIndex(SpaceDiagonals, toWin, 0, 0, 0, 2)
            possibilities[index][i - x] = ord(board[i][toWin - i - 1][i])
            index = self._possibilitiesIndex(SpaceDiagonals, toWin, 0, 0, 0, 3)
            possibilities[index][i - x] = ord(board[i][i][toWin - i - 1])

        # print('\n'.join(['{:3}  '.format(i) + ''.join(['{:4}'.format(chr(item)) for item in possibilities[i]]) for i in range(len(possibilities))]))
        arr: List[np.ndarray] = possibilities.tolist()
        winner = _.find(arr, lambda p: p[0] != ord('E') and _.every(p, lambda x: x == p[0]))
        return 'Draw' if winner is None else chr(winner[0])

    def _possibilitiesIndex(self, indexType: IndexEnum, toWin: int, x: int, y: int, z: int, extra: int = 0) -> int:
        if indexType == Rows:
            return toDec(int(''.join([str(z), str(y), str(x)])), toWin) + extra
        if indexType == BoardDiagonals and extra <= 0:
            return toWin ** 3 + toDec(int(''.join([str(z), str(y), str(x)])), toWin)
        if indexType == BoardDiagonals and extra > 0:
            return 2 * toWin ** 3 + toDec(int(''.join([str(z), str(y), str(x)])), toWin)
        if indexType == SpaceDiagonals:
            return 3 * toWin ** 3 + extra

    def isBoardEmpty(self, board: Board3D) -> bool:
        for i in range(len(board)):
            for j in range(len(board[i])):
                for k in range(len(board[i][j])):
                    if board[i][j][k] != 'E':
                        return False
        return True

    def hasBoardAnyMoves(self, board: Board3D) -> bool:
        for i in range(len(board)):
            for j in range(len(board[i])):
                for k in range(len(board[i][j])):
                    if board[i][j][k] == 'E':
                        return True
        return False

    def forEachBoard(self, board: Board3D, func):
        for i in range(len(board)):
            for j in range(len(board)):
                for k in range(len(board)):
                    func(board, i, j, k)

    def mapBoard(self, board: Board3D, func):
        for i in range(len(board)):
            for j in range(len(board)):
                for k in range(len(board)):
                    board[i][j] = func(board, i, j, k)
