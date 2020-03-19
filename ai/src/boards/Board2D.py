from typing import List

import pydash as _

from boards.IBoard import IBoard
from common.Defs import Cell, Winner

Board2D = List[List[Cell]]


class Board2DOperations(IBoard[Board2D]):
    def createBoard(self, size: int = 3) -> Board2D:
        return [['E' for _ in range(size)] for _ in range(size)]

    def boardToString(self, board: Board2D) -> str:
        return '+' + ''.join(_.times(len(board), lambda x: '---+')) + '\n' + \
               ''.join(_.map_(board, lambda row: '| ' + ' | '.join(row) + ' |\n+' + ''.join(
                   _.times(len(board), lambda x: '---+')) + '\n'))

    def getBoardWinner(self, board: Board2D, toWin: int) -> Winner:
        for i in range(len(board)):
            for j in range(len(board) - toWin + 1):
                if board[i][j] == 'E':
                    continue
                cells = [board[i][j + k] for k in range(toWin)]
                if _.every(cells, lambda cell: cell == cells[0]):
                    return cells[0]
        for j in range(len(board)):
            for i in range(len(board) - toWin + 1):
                if board[i][j] == 'E':
                    continue
                cells = [board[i + k][j] for k in range(toWin)]
                if _.every(cells, lambda cell: cell == cells[0]):
                    return cells[0]
        for i in range(len(board) - toWin + 1):
            for j in range(len(board) - toWin + 1):
                if board[i][j] == 'E' or board[i + toWin - 1][j] == 'E':
                    continue
                cells = [board[i + k][j + k] for k in range(toWin)]
                if _.every(cells, lambda cell: cell == cells[0]):
                    return cells[0]
                cells = [board[i - k + toWin - 1][j + k] for k in range(toWin)]
                if _.every(cells, lambda cell: cell == cells[0]):
                    return cells[0]

        return 'Draw'

    def isBoardEmpty(self, board: Board2D) -> bool:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 'E':
                    return False
        return True

    def hasBoardAnyMoves(self, board: Board2D) -> bool:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 'E':
                    return True
        return False

    def forEachBoard(self, board: Board2D, func):
        for i in range(len(board)):
            for j in range(len(board)):
                func(board, i, j)

    def mapBoard(self, board: Board2D, func):
        for i in range(len(board)):
            for j in range(len(board)):
                board[i][j] = func(board, i, j)
