import {Cell, Player, Winner} from "./Defs";
import * as _ from 'lodash';

export type Board2D = Cell[][];
export type Board3D = Cell[][][];

export const createBoard2D = (size: number = 3): Board2D =>
    _.times(size, () => _.times(size, (): Cell => ' '));

export const createBoard3D = (size: number = 3): Board3D =>
    _.times(size, () => _.times(size, () => _.times(size, (): Cell => ' ')));

export const board2DToString = (board: Board2D): string =>
    `-${_.times(board.length, () => '----').join('')}\n` +
    board.map(row =>
        `| ${row.join(' | ')} |\n` +
        `-${_.times(board.length, () => '----').join('')}\n`
    ).join('');

export const get2DBoardWinner = (board: Board2D, toWin: number): Winner => {
    // check rows
    for (let i = 0; i < board.length; i++) {
        for (let j = 0; j < board.length - toWin + 1; j++) {
            if (board[i][j] == ' ') continue;
            const cells: Cell[] = [];
            for (let k = j; k < toWin; k++) {
                cells.push(board[i][k]);
            }
            if (_.every(cells, cell => cell == cells[0])) {
                return cells[0] as Player;
            }
        }
    }

    // check cols
    for (let j = 0; j < board.length; j++) {
        for (let i = 0; i < board.length - toWin + 1; i++) {
            if (board[i][j] == ' ') continue;
            const cells: Cell[] = [];
            for (let k = i; k < toWin; k++) {
                cells.push(board[k][j]);
            }
            if (_.every(cells, cell => cell == cells[0])) {
                return cells[0] as Player;
            }
        }
    }

    // check diagonals
    for (let i = 0; i < board.length - toWin + 1; i++) {
        for (let j = 0; j < board.length - toWin + 1; j++) {
            if (board[i][j] == ' ') continue;
            let cells: Cell[] = [];
            for (let k = 0; k < toWin; k++) {
                cells.push(board[i + k][j + k]);
            }
            if (_.every(cells, cell => cell == cells[0])) {
                return cells[0] as Player;
            }
            cells = [];
            for (let k = 0; k < toWin; k++) {
                cells.push(board[i - k + toWin - 1][j + k]);
            }
            if (_.every(cells, cell => cell == cells[0])) {
                return cells[0] as Player;
            }
        }
    }

    return '_';
};
