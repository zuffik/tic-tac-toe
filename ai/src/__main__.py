import os
import time
from argparse import ArgumentParser, Namespace

import tensorflow as tf
from tensorflow import keras
from keras import backend as K
from tensorflow.python.tools import freeze_graph

from boards.Board import board2DOperations, board3DOperations, BoardOperations, Board
from common.Defs import Player, getOtherPlayer
from minmax.MinMax import MinMax
from neural.NetworkModelAdaptive2D import NetworkModelAdaptive2D
from neural.NetworkModelAdaptive3D import NetworkModelAdaptive3D
from neural.NetworkModelLarge import NetworkModelLarge

scripts = ['ann', 'minmax', 'analyze', 'game', 'playground', 'store-ann']

analyzeParameters = [

    {'size': 3, 'algorithm': None, 'player': 'X', 'ann_model': 'adaptive', 'to_win': 3, 'simulations': 4000,
     'validations': 30, 'dimension': 2, 'max_depth': -1},
    {'size': 4, 'algorithm': None, 'player': 'X', 'ann_model': 'adaptive', 'to_win': 3, 'simulations': 4000,
     'validations': 25, 'dimension': 2, 'max_depth': 4},
    {'size': 5, 'algorithm': None, 'player': 'X', 'ann_model': 'adaptive', 'to_win': 3, 'simulations': 4000,
     'validations': 25, 'dimension': 2, 'max_depth': 2},
    {'size': 6, 'algorithm': None, 'player': 'X', 'ann_model': 'adaptive', 'to_win': 3, 'simulations': 4000,
     'validations': 25, 'dimension': 2, 'max_depth': 2},
    {'size': 7, 'algorithm': None, 'player': 'X', 'ann_model': 'adaptive', 'to_win': 3, 'simulations': 4000,
     'validations': 15, 'dimension': 2, 'max_depth': 2},
    {'size': 8, 'algorithm': None, 'player': 'X', 'ann_model': 'adaptive', 'to_win': 3, 'simulations': 4000,
     'validations': 15, 'dimension': 2, 'max_depth': 2},
    {'size': 9, 'algorithm': None, 'player': 'X', 'ann_model': 'adaptive', 'to_win': 3, 'simulations': 4000,
     'validations': 15, 'dimension': 2, 'max_depth': 2},
    {'size': 10, 'algorithm': None, 'player': 'X', 'ann_model': 'adaptive', 'to_win': 3, 'simulations': 4000,
     'validations': 15, 'dimension': 2, 'max_depth': 2},
    {'size': 11, 'algorithm': None, 'player': 'X', 'ann_model': 'adaptive', 'to_win': 3, 'simulations': 4000,
     'validations': 15, 'dimension': 2, 'max_depth': 2},
    {'size': 12, 'algorithm': None, 'player': 'X', 'ann_model': 'adaptive', 'to_win': 3, 'simulations': 4000,
     'validations': 15, 'dimension': 2, 'max_depth': 2},
    {'size': 13, 'algorithm': None, 'player': 'X', 'ann_model': 'adaptive', 'to_win': 3, 'simulations': 4000,
     'validations': 15, 'dimension': 2, 'max_depth': 2},
    {'size': 14, 'algorithm': None, 'player': 'X', 'ann_model': 'adaptive', 'to_win': 3, 'simulations': 4000,
     'validations': 15, 'dimension': 2, 'max_depth': 2},
    {'size': 15, 'algorithm': None, 'player': 'X', 'ann_model': 'adaptive', 'to_win': 3, 'simulations': 4000,
     'validations': 15, 'dimension': 2, 'max_depth': 2},
]
analyzeParameters.reverse()

parser = ArgumentParser()
parser.add_argument('algorithm', help='Algorithm to run', type=str, choices=scripts)
parser.add_argument('--size', help='Size of the board', default=3, type=int)
parser.add_argument('--to-win', help='Number of cells in row to become winner', default=3, type=int)
parser.add_argument('--player', help='Starting player', default='X', type=str, choices=['X', 'O'])
parser.add_argument('--simulations', help='Number of random games for training (for ANN)', default=100000, type=int)
parser.add_argument('--validations', help='Number of random games for testing (for ANN)', default=20, type=int)
parser.add_argument('--dimension', help='Dimension of board', default=2, type=int, choices=[2, 3])
parser.add_argument('--max-depth', help='Max depth of minmax algorithm', default=-1, type=int)
parser.add_argument('--ann-model', help='ANN model', default='large', type=str, choices=['large', 'adaptive'])


def createAndTrainModel(argv, board: Board, operations: BoardOperations):
    model = NetworkModelLarge(board, operations, argv.to_win, argv.player) if argv.ann_model == 'large' else \
        (NetworkModelAdaptive2D(board, operations, argv.to_win, argv.player) if argv.dimension == 2 else
         NetworkModelAdaptive3D(board, operations, argv.to_win, argv.player))
    st = time.time()
    games = model.simulateGames(n=argv.simulations)
    model.gameStats(games)
    model.trainModel(games)
    print('Trained in ' + str(time.time() - st))
    st = time.time()
    model.gameStats(model.simulateGames(n=argv.validations, useModel=True, verbose=1))
    print('Validated in ' + str(time.time() - st))
    return model


def freeze_session(session, keep_var_names=None, output_names=None, clear_devices=True):
    """
    Freezes the state of a session into a pruned computation graph.

    Creates a new computation graph where variable nodes are replaced by
    constants taking their current value in the session. The new graph will be
    pruned so subgraphs that are not necessary to compute the requested
    outputs are removed.
    @param session The TensorFlow session to be frozen.
    @param keep_var_names A list of variable names that should not be frozen,
                          or None to freeze all the variables in the graph.
    @param output_names Names of the relevant graph outputs.
    @param clear_devices Remove the device directives from the graph for better portability.
    @return The frozen graph definition.
    """
    from tensorflow.python.framework.graph_util import convert_variables_to_constants
    graph = session.graph
    with graph.as_default():
        freeze_var_names = list(set(v.op.name for v in tf.compat.v1.global_variables()).difference(keep_var_names or []))
        output_names = output_names or []
        output_names += [v.op.name for v in tf.compat.v1.global_variables()]
        # Graph -> GraphDef ProtoBuf
        input_graph_def = graph.as_graph_def()
        if clear_devices:
            for node in input_graph_def.node:
                node.device = ""
        frozen_graph = convert_variables_to_constants(session, input_graph_def,
                                                      output_names, freeze_var_names)
        return frozen_graph


def main(argv):
    board = board2DOperations.createBoard(argv.size) if argv.dimension == 2 else board3DOperations.createBoard(
        argv.size)
    operations = board2DOperations if argv.dimension == 2 else board3DOperations
    if argv.algorithm == scripts[0]:
        createAndTrainModel(argv, board, operations)
    elif argv.algorithm == scripts[5]:
        with tf.compat.v1.Session() as sess:
            model = createAndTrainModel(argv, board, operations).playerModel()
            outDir = os.getcwd() + '/models/size-' + str(argv.size) + '-to-win-' + str(argv.to_win)
            os.makedirs(outDir, exist_ok=True)
            print(model.output.op.name)
            print(model.outputs)
            print(model.inputs)
            model.save_weights(outDir + '/weights')
            frozen_graph = freeze_session(sess, output_names=[model.output.op.name])
            tf.io.write_graph(frozen_graph, "model", outDir + "/model.bytes", as_text=False)

            # freeze_graph.freeze_graph(input_graph=outDir + '/model.pb',
            #                           input_binary=True,
            #                           input_checkpoint=tf.train.latest_checkpoint(outDir),
            #                           output_node_names=[model.output.op.name],
            #                           output_graph=outDir + '/model.bytes',
            #                           clear_devices=True, initializer_nodes="", input_saver="",
            #                           restore_op_name="save/restore_all", filename_tensor_name="save/Const:0")

    elif argv.algorithm == scripts[1]:
        minmax = MinMax(board, operations, argv.to_win, argv.player, argv.max_depth)
        st = time.time()
        i = 0
        while minmax.isDraw() and operations.hasBoardAnyMoves(board):
            # print(operations.boardToString(board))
            st = time.time()
            move = minmax.bestMove()
            minmax.performMove(move)
            i += 1
            print('Step ' + str(i) + ' in ' + str(time.time() - st))
        # print(operations.boardToString(board))
        print('Winner ' + operations.getBoardWinner(board, argv.to_win))
        print('Game played in ' + str(time.time() - st))
    elif argv.algorithm == scripts[3]:
        baseModel = NetworkModelAdaptive2D(board, operations, argv.to_win, argv.player)
        baseModel.trainModel(baseModel.simulateGames(n=argv.simulations))

        annModel = NetworkModelLarge(board, operations, argv.to_win, argv.player)
        minmax = MinMax(board, operations, argv.to_win, getOtherPlayer(argv.player), argv.max_depth)
        second = minmax

        # second.trainModel(second.simulateGames(n=argv.simulations))

        player: Player = argv.player

        pl = 0
        op = 0
        draw = 0
        for game in range(argv.validations):
            print('Validation ' + str(game + 1))
            while operations.getBoardWinner(board, argv.to_win) == 'Draw' and operations.hasBoardAnyMoves(board):
                model = baseModel if player == argv.player else second
                move = model.bestMove(player)
                baseModel.performMove(move)
                second.performMove(move)
                board = baseModel.board
                # print('Player ' + player + ' moved to ' + str(move))
                # print(operations.boardToString(board))
                player = getOtherPlayer(player)
            # print('Winner is ' + operations.getBoardWinner(board, argv.to_win))
            winner = operations.getBoardWinner(board, argv.to_win)
            if winner == argv.player:
                pl += 1
            elif winner == getOtherPlayer(argv.player):
                op += 1
            else:
                draw += 1
            baseModel.clearBoard()
            second.clearBoard()
            board = baseModel.board
        print("Results for player %s:" % argv.player)
        print("Wins: %d (%.1f%%)" % (pl, pl / argv.validations * 100))
        print("Loss: %d (%.1f%%)" % (op, op / argv.validations * 100))
        print("Draw: %d (%.1f%%)" % (draw, draw / argv.validations * 100))
    else:
        raise RuntimeError(argv[1] + ' is not valid script')


if __name__ == '__main__':
    args = parser.parse_args()
    if args.algorithm == 'playground':
        pass
    elif args.algorithm == 'analyze':
        for a in analyzeParameters:
            for i in range(3):
                a['algorithm'] = 'minmax'
                print('Nth simulation ' + str(i))
                st = time.time()
                copy = Namespace(**a)
                print('Running with arguments:', copy)
                print('MinMax')
                main(copy)
                print('MinMax run in ' + str(time.time() - st))
            for i in range(3):
                a['algorithm'] = 'ann'
                print('Nth simulation ' + str(i))
                copy = Namespace(**a)
                print('Running with arguments:', copy)
                print('ANN')
                st = time.time()
                main(copy)
                print('ANN run in ' + str(time.time() - st))
    else:
        print('Running with arguments:', args)
        main(args)
