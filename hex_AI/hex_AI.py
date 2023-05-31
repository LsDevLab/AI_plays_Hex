""""
==========================================================
            Intelligent Agents: Final project
                    A.A. 2022-2023
----------------------------------------------------------
                   Luigi Schiavone
=========================================================

FILE: this file contains the game solving functions

"""
import math
import heuristics


def minimax(game, maximize, depth=0, max_depth=math.inf,
            node_value_heuristic=heuristics.ShortestPathValueHeuristic,
            node_ordering_heuristic=heuristics.RandomOrderHeuristic):
    """
    The Minimax algorithm for solving a game.

    :param game: the game object
    :param maximize: True if first player wants to maximize the minimax value
    :param depth: the current tree visit depth
    :param max_depth: the max depth to search until
    :param node_value_heuristic: the heuristic the algorithm will use to evaluate a position
    :param node_ordering_heuristic: an orderding heuristic on the positions
    :return: the current minimax value and the best move to execute
    """
    winner = game.check_game()
    # if position is terminal (the game is ended) return the position value and no move can be done
    # or max search depth reached
    if winner is not None or depth >= max_depth:
        # compute the heuristic function
        J = node_value_heuristic().compute(game)
        return J, None
    curr_minimax_value = -float('inf') if maximize else float('inf')
    # compute legal moves
    available_moves = game.available_moves()
    # sort moves according node_ordering_heuristic
    available_moves = node_ordering_heuristic().sort(game, available_moves)
    # for each possible move at current position
    for move in available_moves:
        # suppose to play move
        game.play_move(move)
        # compute the minimax value using the opponent
        minimax_value, _ = minimax(game, not maximize, depth=depth+1, max_depth=max_depth, node_value_heuristic=node_value_heuristic)
        game.undo_move()
        # update the best move according the max/min minimax value
        if (maximize and (minimax_value > curr_minimax_value or curr_minimax_value == float('-inf'))) or (not maximize and (minimax_value < curr_minimax_value or curr_minimax_value == float('inf'))):
            curr_minimax_value = minimax_value
            best_move = move
    # returning the minimax value and the best move for the player
    return curr_minimax_value, best_move


def alpha_beta_pruning(game, maximize, depth=0, max_depth=math.inf,
                       node_value_heuristic=heuristics.ShortestPathValueHeuristic,
                       node_ordering_heuristic=heuristics.RandomOrderHeuristic,
                       alpha=-float('inf'),
                       beta=float('inf')):
    """
    The a-b pruning algorithm for solving a game.

    :param game: the game object
    :param maximize: True if first player wants to maximize the minimax value
    :param depth: the current tree visit depth
    :param max_depth: the max depth to search until
    :param node_value_heuristic: the heuristic the algorithm will use to evaluate a position
    :param node_ordering_heuristic: an orderding heuristic on the positions
    :param alpha: the current alpha value
    :param beta: the current beta value
    :return: the current minimax value and the best move to execute
    """
    winner = game.check_game()
    # if position is terminal (the game is ended) or max search depth reached
    # return the position value and no move can be done
    if winner is not None:
        return winner * float('inf'), None
    elif depth >= max_depth:
        # compute the heuristic function
        J = node_value_heuristic.compute(game)
        return J, None
    curr_minimax_value = -float('inf') if maximize else float('inf')
    # compute legal moves
    available_moves = game.available_moves()
    # sort moves according node_ordering_heuristic
    available_moves = node_ordering_heuristic.sort(game, available_moves)
    # for each possible move at current position
    for move in available_moves:
        # suppose to play move
        game.play_move(move)
        # compute the minimax value using the opponent
        minimax_value, _ = alpha_beta_pruning(game, not maximize, depth=depth+1, max_depth=max_depth,
                                              node_value_heuristic=node_value_heuristic,
                                              node_ordering_heuristic=node_ordering_heuristic,
                                              alpha=alpha, beta=beta)
        game.undo_move()
        # update the best move according the max/min minimax value
        if (maximize and (minimax_value > curr_minimax_value or curr_minimax_value == float('-inf'))) or (not maximize and (minimax_value < curr_minimax_value or curr_minimax_value == float('inf'))):
            curr_minimax_value = minimax_value
            best_move = move
        # alpha beta cutoff
        if maximize:
            alpha = max(alpha, minimax_value)
        else:
            beta = min(beta, minimax_value)
        if beta <= alpha:
            break
    # returning the minimax value and the best move for the player
    return curr_minimax_value, best_move


def computer_turn(game, ui, config):
    """
    Plays a move from the computer.

    :param game: the game object
    :param ui: the game ui object
    :param config: the game config
    """
    # compute the best move
    player = game.player_turn
    # if this is the first move uses the central cell as opening move
    if len(game.available_moves()) == config['board_size'] ** 2:
        move = (config['board_size'] // 2, config['board_size'] // 2)
    else:
        node_value_heuristic = config['AI1_node_value_heuristic'] if (player == ui.BLUE_PLAYER) else config[
            'AI2_node_value_heuristic']
        node_ordering_heuristic = config['AI1_node_ordering_heuristic'] if (player == ui.BLUE_PLAYER) else config[
            'AI2_node_ordering_heuristic']
        maximize = (player == ui.BLUE_PLAYER)
        _, move = alpha_beta_pruning(game, maximize, max_depth=config['max_depth'],
                                            node_value_heuristic=node_value_heuristic,
                                            node_ordering_heuristic=node_ordering_heuristic)
    # plays the move
    game.play_move(move)
    # updates the ui
    node = move[0] * ui.board_size + move[1]
    ui.color[node] = ui.blue if player is ui.BLUE_PLAYER else ui.red
    print(move)
