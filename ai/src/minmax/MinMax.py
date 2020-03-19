from typing import List, Tuple
import random
import sys

import pydash as _

from boards.Board import Board, BoardOperations, Move
from boards.Board3D import Board3D, Board3DOperations
from common.Defs import Player, getOtherPlayer, Winner, Move3D


class MinMax:
    def __init__(self, board: Board, operations: BoardOperations, toWin: int = None, player: Player = 'X',
                 maxDepth: int = -1):
        self._board = board
        self._maxDepth = maxDepth
        self._size = len(board)
        self._toWin = toWin if toWin is not None else self._size
        self._operations = operations
        self._operations3D = Board3DOperations()
        self._player = player
        self._opponent = getOtherPlayer(self._player)
        self._onMove = self._player

    def _projectBoard(self, board: Board) -> Board3D:
        return board if isinstance(board[0][0], list) else [board]

    def _unprojectMove(self, board: Board, move: Move) -> Move:
        return move if isinstance(board[0][0], list) else (move[0], move[2], move[3])

    def getWinner(self) -> Winner:
        value = self._evaluateBoard(self._board)
        if value < 0:
            return self._opponent
        elif value > 0:
            return self._player
        else:
            return 'Draw'

    def isDraw(self) -> bool:
        return self.getWinner() == 'Draw'

    def _evaluateBoard(self, board: Board, customWinner=None) -> int:
        winner = self._operations.getBoardWinner(board, self._toWin) if customWinner is None else \
            customWinner(board, self._toWin)
        if winner == 'Draw':
            return 0
        return 1 if winner == self._player else -1

    def _minMax(self, gameBoard: Board3D, maximizing: bool, depth: int = 0) -> int:
        board = _.clone_deep(gameBoard)
        score = self._evaluateBoard(board, customWinner=self._operations3D.getBoardWinner)
        if score > 0 or score < 0 or (score == 0 and not self._operations3D.hasBoardAnyMoves(board)):
            return score

        bestValue = -sys.maxsize if maximizing else sys.maxsize
        for i in range(len(board)):
            for j in range(len(board[i])):
                for k in range(len(board[i][j])):
                    if board[i][j][k] == 'E' and (self._maxDepth <= 0 or depth + 1 <= self._maxDepth):
                        board[i][j][k] = self._player if maximizing else self._opponent
                        newValue = self._minMax(board, not maximizing, depth + 1)
                        bestValue = max(bestValue, newValue) if maximizing else min(bestValue, newValue)
                        board[i][j][k] = 'E'
        return bestValue

    def _possibleMoves2D(self, board: Board3D) -> List[Tuple[int, int]]:
        return [(i, j) for i in range(self._size) for j in range(self._size) if board[0][i][j] == 'E']

    def _findBestMove(self, gameBoard: Board, player: Player = None) -> Move:
        forPlayer = self._onMove if player is None else player
        isPlayerOnMove = forPlayer == self._player
        bestValue = -sys.maxsize if isPlayerOnMove else sys.maxsize
        bestMove: Move3D = (forPlayer, -1, -1, -1)
        board = self._projectBoard(_.clone_deep(gameBoard))

        if self._operations3D.isBoardEmpty(board):
            return forPlayer, random.randint(0, self._size - 1), random.randint(0, self._size - 1), \
                   random.randint(0, self._size - 1)

        for i in range(len(board)):
            for j in range(len(board[i])):
                for k in range(len(board[i][j])):
                    if board[i][j][k] == 'E':
                        board[i][j][k] = forPlayer
                        newVal = self._minMax(board, isPlayerOnMove, 0)
                        if (isPlayerOnMove and newVal > bestValue) or \
                                (not isPlayerOnMove and newVal < bestValue):
                            bestValue = newVal
                            bestMove = (forPlayer, i, j, k)
        return self._unprojectMove(self._board, bestMove)

    def bestMove(self, player: Player = None) -> Move:
        return self._findBestMove(self._board, player)

    def performMove(self, move: Move):
        self._onMove = getOtherPlayer(move[0])
        if isinstance(self._board[0][0], list):
            self._board[move[1]][move[2]][move[3]] = move[0]
        else:
            self._board[move[1]][move[2]] = move[0]

    def clearBoard(self):
        self._board = self._operations.createBoard(self._size)
