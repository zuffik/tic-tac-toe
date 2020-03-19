from typing import Generic, TypeVar

from common.Defs import Winner

T = TypeVar('T')


class IBoard(Generic[T]):
    def createBoard(self, size: int = 3) -> T:
        pass

    def boardToString(self, board: T) -> str:
        pass

    def getBoardWinner(self, board: T, toWin: int) -> Winner:
        pass

    def isBoardEmpty(self, board: T) -> bool:
        pass

    def hasBoardAnyMoves(self, board: T) -> bool:
        pass

    def mapBoard(self, board: T, func):
        pass

    def forEachBoard(self, board: T, func):
        pass
