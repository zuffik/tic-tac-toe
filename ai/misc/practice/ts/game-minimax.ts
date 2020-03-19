import {board2DToString, createBoard2D} from "./Board";
import {MinMax2D} from "./Minimax";

const board = createBoard2D(4);


const minMax2D = new MinMax2D(board, 'X', 4);

while (minMax2D.isDraw()) {
    const move = minMax2D.bestMove();
    console.log(`Best move for player '${move[0]}' is to [${move.slice(1).join(', ')}].`);
    minMax2D.performMove(move);
    console.log(board2DToString(minMax2D.board));
}
