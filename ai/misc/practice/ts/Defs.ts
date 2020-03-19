export type Player = 'X' | 'O';
export type Winner = Player | '_';
export type Cell = Player | ' ';

export type Move2D = [Player, number, number];
export type Move3D = [Player, number, number, number];

export const getOtherPlayer = (player: Player): Player => player == 'X' ? 'O' : 'X';
