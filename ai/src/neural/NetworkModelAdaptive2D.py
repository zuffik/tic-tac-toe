import random
from typing import List, Tuple

import numpy as np
import tensorflow.keras as keras

from boards.Board2D import Board2D, Board2DOperations
from common.Defs import Player, Winner, Move2D
from neural.NetworkModel import NetworkModel

GameResult = Tuple[List[Move2D], Winner]


class NetworkModelAdaptive2D(NetworkModel):
    def __init__(self, board: Board2D, operations: Board2DOperations, toWin: int = 3, player: Player = 'X'):
        super().__init__(board, operations, toWin, player)

    def _createModel(self) -> keras.Model:
        inputs = len(self.board) ** 2 * 3
        hidden = len(self.board) ** 2
        # count of output must be size^2 because categorical_crossentropy returns one-hot array
        output = len(self.board) ** 2
        model = keras.Sequential()
        model.add(keras.layers.Dense(inputs, activation='relu', input_shape=(inputs,)))
        model.add(keras.layers.Dense(hidden, activation='relu'))
        model.add(keras.layers.Dense(output, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])
        return model

    def _vectorMoveIndex(self, move: Move2D) -> int:
        return self._vectorIndex(move[1], move[2])

    def _vectorIndex(self, i: int, j: int) -> int:
        return i * self._size + j

    def _indexToMove(self, index: int) -> Tuple[int, int]:
        return index // self._size, index % self._size

    def _boardHash(self, board: Board2D) -> List[int]:
        result: List[int] = list(np.zeros(self._size ** 2 * 3, dtype=int))
        for i in range(self._size):
            for j in range(self._size):
                index = self._vectorIndex(i, j)
                multiplicative = 0
                if board[i][j] == self._player:
                    multiplicative = 1
                elif board[i][j] == self._opponent:
                    multiplicative = 2
                result[index + self._size ** 2 * multiplicative] = 1
        return result

    def _containsMove(self, move: Tuple[int, int], emptyMoves: List[Move2D]) -> bool:
        for m in emptyMoves:
            if m[1] == move[0] and m[2] == move[1]:
                return True
        return False

    def _performMove(self, move: Move2D, board: Board2D) -> Board2D:
        board[move[1]][move[2]] = move[0]
        return board

    def _possibleMoves(self, board: Board2D, player: Player) -> List[Move2D]:
        collectionX = list(range(self._size))
        collectionY = list(range(self._size))
        random.shuffle(collectionX)
        random.shuffle(collectionY)
        emptyCells = [(player, i, j) for i in collectionX for j in collectionY if board[i][j] == 'E']
        fullCells = [(player, i, j) for i in range(self._size) for j in range(self._size) if board[i][j] != 'E']
        if len(fullCells) > 0:
            emptyCells.sort(key=lambda x: min([abs(x[1] - c[1]) + abs(x[2] - c[2]) for c in fullCells]))
        return emptyCells

    def _bestMove(self, board: Board2D, player: Player) -> Move2D:
        player, move = self._predictBestMove(board, player)
        sub = 0 if isinstance(move[0], str) else 1
        return player, move[1 - sub], move[2 - sub]
