from typing import Union, List, Tuple

from boards.Board2D import Board2DOperations, Board2D
from boards.Board3D import Board3DOperations, Board3D
from common.Defs import Move2D, Move3D, Winner

board2DOperations = Board2DOperations()
board3DOperations = Board3DOperations()

Board = Union[Board2D, Board3D]
Move = Union[Move2D, Move3D]
BoardOperations = Union[Board2DOperations, Board3DOperations]
GameResult = Tuple[List[Move], Winner]
