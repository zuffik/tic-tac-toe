import random
from typing import List, Tuple

import baseconvert
import numpy as np
import tensorflow.keras as keras

from boards.Board3D import Board3D, Board3DOperations
from common.Defs import Player, Winner, Move3D
from neural.NetworkModel import NetworkModel

GameResult = Tuple[List[Move3D], Winner]


class NetworkModelAdaptive3D(NetworkModel):
    def __init__(self, board: Board3D, operations: Board3DOperations, toWin: int = 3, player: Player = 'X'):
        super().__init__(board, operations, toWin, player)

    def _createModel(self) -> keras.Model:
        inputs = len(self.board) ** 3 * 3
        hidden1 = len(self.board) ** 3
        # hidden2 = len(self.board) ** 3
        output = len(self.board) ** 3
        model = keras.Sequential()
        model.add(keras.layers.Dense(inputs, activation='relu', input_shape=(inputs,)))
        model.add(keras.layers.Dense(hidden1, activation='relu'))
        # model.add(keras.layers.Dense(hidden2, activation='relu'))
        model.add(keras.layers.Dense(output, activation='softmax', name="out_softmax"))
        model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])
        return model

    def _vectorMoveIndex(self, move: Move3D) -> int:
        return self._vectorIndex(move[1], move[2], move[3])

    def _vectorIndex(self, i: int, j: int, k: int) -> int:
        return int(''.join(map(str, baseconvert.base(number=str(i) + str(j) + str(k), input_base=self._size, output_base=10))))

    def _indexToMove(self, index: int) -> Tuple[int, int, int]:
        result = ''.join(map(str, baseconvert.base(number=index, input_base=10, output_base=self._size))).zfill(3)
        return int(result[0]), int(result[1]), int(result[2])

    def _boardHash(self, board: Board3D) -> List[int]:
        result: List[int] = list(np.zeros(self._size ** 3 * 3, dtype=int))
        for i in range(self._size):
            for j in range(self._size):
                for k in range(self._size):
                    index = self._vectorIndex(i, j, k)
                    multiplicative = 0
                    if board[i][j][k] == self._player:
                        multiplicative = 1
                    elif board[i][j][k] == self._opponent:
                        multiplicative = 2
                    result[index + self._size ** 3 * multiplicative] = 1
        return result

    def _containsMove(self, move: Tuple[int, int, int], emptyMoves: List[Move3D]) -> bool:
        for m in emptyMoves:
            if m[1] == move[0] and m[2] == move[1] and m[3] == move[2]:
                return True
        return False

    def _performMove(self, move: Move3D, board: Board3D) -> Board3D:
        board[move[1]][move[2]][move[3]] = move[0]
        return board

    def _possibleMoves(self, board: Board3D, player: Player) -> List[Move3D]:
        collectionX = list(range(self._size))
        collectionY = list(range(self._size))
        collectionZ = list(range(self._size))
        random.shuffle(collectionX)
        random.shuffle(collectionY)
        random.shuffle(collectionZ)
        emptyCells = [(player, i, j, k) for i in collectionX for j in collectionY for k in collectionZ if
                      board[i][j][k] == 'E']
        fullCells = [(player, i, j, k) for i in range(self._size) for j in range(self._size) for k in range(self._size)
                     if board[i][j][k] != 'E']
        if len(fullCells) > 0:
            emptyCells.sort(
                key=lambda x: min([abs(x[1] - c[1]) + abs(x[2] - c[2]) + abs(x[3] - c[3]) for c in fullCells]))
        return emptyCells

    def _bestMove(self, board: Board3D, player: Player) -> Move3D:
        player, move = self._predictBestMove(board, player)
        sub = 0 if isinstance(move[0], str) else 1
        return player, move[1 - sub], move[2 - sub], move[3 - sub]
