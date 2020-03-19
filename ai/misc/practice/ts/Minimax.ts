/**
 * Based on
 * @link https://www.geeksforgeeks.org/minmax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/
 */
import {Board2D, get2DBoardWinner} from "./Board";
import {Cell, getOtherPlayer, Move2D, Player, Winner} from "./Defs";
import * as _ from 'lodash';

export class MinMax2D {
    private readonly size: number;
    private readonly toWin: number;
    private readonly opponent: Player;
    private onMove: Player;

    constructor(
        public readonly board: Board2D,
        private readonly player: Player = 'X',
        toWin?: number
    ) {
        this.size = board.length;
        this.toWin = toWin || this.size;
        this.opponent = getOtherPlayer(this.player);
        this.onMove = this.player;
    }

    public canMoveSomewhere(): boolean {
        return this.areAnyMovesLeft(this.board);
    }

    public getWinner(): Winner {
        const value = this.evaluateBoard(this.board);
        if (value < 0) {
            return this.opponent;
        } else if (value > 0) {
            return this.player;
        } else {
            return '_';
        }
    }

    public isDraw(): boolean {
        return this.getWinner() == '_';
    }

    private areAnyMovesLeft(board: Board2D): boolean {
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                if (board[i][j] == ' ') {
                    return true;
                }
            }
        }
        return false;
    }

    private evaluateBoard(board: Board2D): number {
        const winner = get2DBoardWinner(board, this.toWin);
        if (winner == '_') return 0;
        return winner == this.player ? 1 : -1;
    }

    private minMax(gameBoard: Board2D, maximizing: boolean, depth: number = 0): number {
        const board = _.cloneDeep(gameBoard);
        const score = this.evaluateBoard(board);
        if (score > 0 || score < 0 || (score == 0 && !this.areAnyMovesLeft(board))) {
            return score;
        }

        let bestValue = maximizing ? Number.MIN_SAFE_INTEGER : Number.MAX_SAFE_INTEGER;
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                if (board[i][j] == ' ') {
                    board[i][j] = maximizing ? this.player : this.opponent;
                    const newValue = this.minMax(board, !maximizing, depth + 1);
                    bestValue = maximizing
                        ? Math.max(bestValue, newValue)
                        : Math.min(bestValue, newValue);
                    board[i][j] = ' ';
                }
            }
        }
        return bestValue;
    }

    private findBestMove(gameBoard: Board2D, forPlayer?: Player): Move2D {
        forPlayer = forPlayer || this.onMove;
        const isPlayerOnMove = forPlayer == this.player;
        let bestValue = forPlayer == this.player ? Number.MIN_SAFE_INTEGER : Number.MAX_SAFE_INTEGER;
        const bestMove: Move2D = [
            forPlayer,
            -1,
            -1
        ];
        const board = _.cloneDeep(gameBoard);
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                if (board[i][j] == ' ') {
                    board[i][j] = forPlayer;
                    const newVal = this.minMax(board, isPlayerOnMove, 0);
                    if (
                        (isPlayerOnMove && newVal > bestValue) ||
                        (!isPlayerOnMove && newVal < bestValue)
                    ) {
                        bestValue = newVal;
                        bestMove[1] = i;
                        bestMove[2] = j;
                    }
                }
            }
        }
        return bestMove;
    }

    public bestMove(forPlayer?: Player): Move2D {
        return this.findBestMove(this.board, forPlayer);
    }

    public performMove(move: Move2D) {
        this.onMove = getOtherPlayer(move[0]);
        this.board[move[1]][move[2]] = move[0];
    }
}
