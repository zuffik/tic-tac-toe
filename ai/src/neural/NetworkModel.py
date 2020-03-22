import random
from abc import ABC, abstractmethod
from typing import List, Tuple, Union

import numpy as np
from keras import Model
from keras.utils import to_categorical

from boards.Board import Board, BoardOperations, Move, GameResult
from common.Defs import getOtherPlayer, Player, Winner


class NetworkModel(ABC):
    @abstractmethod
    def __init__(self, board: Board, operations: BoardOperations, toWin: int = 3, player: Player = 'X'):
        super().__init__()
        self.board = board
        self._size = len(board)
        self._toWin = toWin if toWin < len(board) else len(board)
        self._player = player
        self._opponent = getOtherPlayer(player)
        self._operations = operations
        self._playerModel = self._createModel()
        self._opponentModel = self._createModel()

    @abstractmethod
    def _createModel(self) -> Model:
        pass

    @abstractmethod
    def _bestMove(self, board: Board, player: Player) -> Move:
        pass

    @abstractmethod
    def _performMove(self, move: Move, board: Board) -> Board:
        pass

    @abstractmethod
    def _possibleMoves(self, board: Board, player: Player) -> List[Move]:
        pass

    @abstractmethod
    def _boardHash(self, board: Board) -> List[int]:
        pass

    @abstractmethod
    def _vectorMoveIndex(self, move: Move) -> int:
        pass

    @abstractmethod
    def _indexToMove(self, index: int) -> Union[Tuple[int, int, int], Tuple[int, int]]:
        pass

    @abstractmethod
    def _containsMove(self, move: Tuple[int, int, int], emptyMoves: List[Move]) -> bool:
        pass

    def bestMove(self, player: Player):
        return self._bestMove(self.board, player)

    def performMove(self, move: Move) -> Board:
        return self._performMove(move, self.board)

    def _simulateGame(self, useModel: bool = False, preferredPlayer: Player = None) -> GameResult:
        if preferredPlayer is None:
            preferredPlayer = self._player
        history: List[Move] = []
        board: Board = self._operations.createBoard(self._size)
        playerToMove: Player = self._player

        winner: Winner = self._operations.getBoardWinner(board, self._toWin)
        while winner == 'Draw' and self._operations.hasBoardAnyMoves(board):
            # Chose a move (random or use a player model if provided)
            if not useModel or self._operations.isBoardEmpty(board):  # or playerToMove != preferredPlayer:
                moves = self._possibleMoves(board, playerToMove)
                moveIndex = int(min(np.random.exponential(), len(moves) - 1)) if not useModel else \
                    random.randint(0, len(moves) - 1)
                move = moves[moveIndex]
            else:
                move = self._bestMove(board, playerToMove)
            self._performMove(move, board)
            winner = self._operations.getBoardWinner(board, self._toWin)

            # Add the move to the history
            history.append(move)

            # Switch the active player
            playerToMove = getOtherPlayer(playerToMove)

        return history, winner

    def gameStats(self, games: List[GameResult], player: Player = None):
        if player is None:
            player = self._player
        stats = {"win": 0, "loss": 0, "draw": 0}
        for (game, result) in games:
            if result == player:
                stats["win"] += 1
            elif result == 'Draw':
                stats["draw"] += 1
            else:
                stats["loss"] += 1

        winPct = stats["win"] / len(games) * 100
        lossPct = stats["loss"] / len(games) * 100
        drawPct = stats["draw"] / len(games) * 100

        print("Results for player %s:" % player)
        print("Wins: %d (%.1f%%)" % (stats["win"], winPct))
        print("Loss: %d (%.1f%%)" % (stats["loss"], lossPct))
        print("Draw: %d (%.1f%%)" % (stats["draw"], drawPct))

    def simulateGames(self, n: int = 10000, useModel: bool = False, preferredPlayer: Player = None, verbose: int = 0) -> \
            List[GameResult]:
        result = []
        for i in range(n):
            if verbose > 0:
                print(i)
            result.append(self._simulateGame(useModel, preferredPlayer))
        return result

    def clearBoard(self):
        self.board = self._operations.createBoard(self._size)

    def _trainTest(self, array: np.ndarray) -> Tuple[List[int], List[int]]:
        trainCount = int(len(array) * 0.8)
        return array[:trainCount], array[trainCount:]

    def _reshape(self, games: List[GameResult]) -> \
            Tuple[Tuple[List[int], List[int], List[int], List[int]], Tuple[List[int], List[int], List[int], List[int]]]:
        playerX = []
        playerY = []
        opponentX = []
        opponentY = []
        for (game, winner) in games:
            if winner == 'Draw':
                # really?
                continue
            X = playerX if winner == self._player else opponentX
            Y = playerY if winner == self._player else opponentY
            board = self._operations.createBoard(self._size)
            for move in game:
                X.append(self._boardHash(board))
                Y.append(self._vectorMoveIndex(move))
                self._performMove(move, board)
        playerX = np.array(playerX)
        opponentX = np.array(opponentX)

        playerY = to_categorical(playerY)
        opponentY = to_categorical(opponentY)
        playerXTrain, playerXTest = self._trainTest(playerX)
        playerYTrain, playerYTest = self._trainTest(playerY)
        opponentXTrain, opponentXTest = self._trainTest(opponentX)
        opponentYTrain, opponentYTest = self._trainTest(opponentY)
        return (playerXTrain, playerXTest, playerYTrain, playerYTest), \
               (opponentXTrain, opponentXTest, opponentYTrain, opponentYTest)

    def trainModel(self, games: List[GameResult] = None) -> Tuple[int, int]:
        (xPlayerTrain, xPlayerTest, yPlayerTrain, yPlayerTest), \
        (xOpponentTrain, xOpponentTest, yOpponentTrain, yOpponentTest) = \
            self._reshape(self.simulateGames() if games is None else games)

        self._playerModel.fit(xPlayerTrain, yPlayerTrain, validation_data=(xPlayerTest, yPlayerTest), epochs=100,
                              batch_size=100, verbose=0)
        return len(xPlayerTrain) + len(xPlayerTest), len(xOpponentTrain) + len(xOpponentTest)

    def _predictBestMove(self, board: Board, player: Player) -> Tuple[Player, Move]:
        emptyMoves = self._possibleMoves(board, player)
        model = self._playerModel if player == self._player else self._opponentModel
        boardHash = np.array([self._boardHash(board)])
        predictions = model.predict(boardHash)
        i = 0
        move = None
        while i < len(predictions):
            result = int(np.argmax(predictions[i]))
            m = self._indexToMove(result)
            if self._containsMove(m, emptyMoves):
                move = m
                break
            i += 1
        if move is None:
            move = emptyMoves[random.randint(0, len(emptyMoves) - 1)]
        return player, move

    def playerModel(self):
        return self._playerModel
