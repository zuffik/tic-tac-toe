from typing import List, Tuple

import numpy as np
import tensorflow.keras as keras

from boards.Board import BoardOperations, Board, Move, GameResult
from common.Defs import Player, Winner, Cell
from neural.NetworkModel import NetworkModel


class NetworkModelLarge(NetworkModel):
    def __init__(self, board: Board, operations: BoardOperations, toWin: int = 3, player: Player = 'X'):
        super().__init__(board, operations, toWin, player)
        self._model = self._createModel()

    def _createModel(self) -> keras.Model:
        inputs = len(self.board) ** 2
        output = 3
        model = keras.Sequential()
        # model.add(keras.layers.Dense(inputs, activation='relu', input_shape=(inputs,)))
        # model.add(keras.layers.Dense(self._size ** 2, activation='relu'))
        # model.add(keras.layers.Dense(self._size ** 2, activation='relu'))
        model.add(keras.layers.Dense(200, activation='relu', input_shape=(inputs,)))
        model.add(keras.layers.Dropout(0.2))
        model.add(keras.layers.Dense(125, activation='relu'))
        model.add(keras.layers.Dense(75, activation='relu'))
        model.add(keras.layers.Dropout(0.1))
        model.add(keras.layers.Dense(25, activation='relu'))
        model.add(keras.layers.Dense(output, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])
        return model

    def _performMovesInEmptyBoard(self, moves: List[Move]) -> Board:
        board = self._operations.createBoard(self._size)
        for move in moves:
            self._performMove(move, board)
        return board

    def _evaluateState(self, winner: Winner) -> int:
        if winner == self._player:
            return 1
        elif winner == self._opponent:
            return 2
        else:
            return 0

    def _evaluateCell(self, cell: Cell) -> int:
        if cell == self._player:
            return 1
        elif cell == self._opponent:
            return -1
        else:
            return 0

    def _getState(self, winner: int) -> Winner:
        if winner == 1:
            return self._player
        elif winner == 2:
            return self._opponent
        else:
            return 'Draw'

    def _getCell(self, cell: int) -> Cell:
        if cell == 1:
            return self._player
        elif cell == -1:
            return self._opponent
        else:
            return 'E'

    def _evaluateBoard(self, board: Board) -> List[List[int]]:
        return [[self._evaluateCell(cell) for cell in row] for row in board]

    def _reshape(self, games: List[GameResult]) -> Tuple[List[int], List[int], List[int], List[int]]:
        X = []
        y = []
        for (game, winner) in games:
            winner = self._operations.getBoardWinner(self._performMovesInEmptyBoard(game), self._toWin)
            for move in range(len(game)):
                X.append(self._evaluateBoard(self._performMovesInEmptyBoard(game[:(move + 1)])))
                y.append(self._evaluateState(winner))

        X = np.array(X).reshape((-1, self._size ** 2))
        y = keras.utils.to_categorical(y)

        # Return an appropriate train/test split
        trainNum = int(len(X) * 0.8)
        return X[:trainNum], X[trainNum:], y[:trainNum], y[trainNum:]

    def _bestMove(self, board: Board, player: Player) -> Move:
        scores = []
        moves = self._possibleMoves(board, player)

        # Make predictions for each possible move
        for i in range(len(moves)):
            future = np.array(self._evaluateBoard(board))
            future[moves[i][1]][moves[i][2]] = self._evaluateCell(player)
            prediction = self._model.predict(future.reshape((-1, self._size ** 2)))[0]
            if player == self._player:
                winPrediction = prediction[1]
                lossPrediction = prediction[2]
            else:
                winPrediction = prediction[2]
                lossPrediction = prediction[1]
            drawPrediction = prediction[0]
            if winPrediction - lossPrediction > 0:
                scores.append(winPrediction - lossPrediction)
            else:
                scores.append(drawPrediction - lossPrediction)

        # Choose the best move with a random factor
        bestMoves = np.flip(np.argsort(scores))
        # Choose a move completely at random
        return player, moves[bestMoves[0]][1], moves[bestMoves[0]][2]

    def trainModel(self, games: List[GameResult] = None):
        xTrain, xTest, yTrain, yTest = self._reshape(self.simulateGames() if games is None else games)
        self._model.fit(xTrain, yTrain, validation_data=(xTest, yTest), epochs=100, batch_size=100)
