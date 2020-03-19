from typing import TypeVar, Union, Tuple

X = TypeVar('X')
O = TypeVar('O')
Draw = TypeVar('Draw')
E = TypeVar('E')

Player = Union[X, O]
Cell = Union[Player, E]
Winner = Union[Player, Draw]

Move2D = Tuple[Player, int, int]
Move3D = Tuple[Player, int, int, int]


def getOtherPlayer(player: Player) -> Player:
    return 'O' if player == 'X' else 'X'
