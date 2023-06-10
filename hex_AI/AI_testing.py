"""
==========================================================
            Intelligent Agents: Final project
                    A.A. 2022-2023
----------------------------------------------------------
                   Luigi Schiavone
=========================================================

FILE: this file contains all the testing and the benchmarks done on my AI players
"""
import time
import numpy as np
import scipy as sc
from tabulate import tabulate

import hex_AI
from hex import Hex
import heuristics

def test(config, trials):

    starting_player = 1

    AI1_wins = 0
    AI2_wins = 0

    AI1_wins_when_starting = 0
    AI2_wins_when_starting = 0

    AI1_avg_times = []
    AI2_avg_times = []
    game_lasted = []

    # run trials run of the experiment
    for n in range(trials):
        AI1_avg_times.append([])
        AI2_avg_times.append([])
        print('Trial', n, '/', trials, '- starting_player:', starting_player, '\n')
        # init the game
        hex = Hex(config['board_size'], starting_player=starting_player)
        i = 0
        # until game finishes
        while True:
            print('Turn', i, '- Player', hex.player_turn, end='. ')
            # running game turn and measuring play time
            start_time = time.time()
            hex_AI.computer_turn_testing(hex, config)
            lasted_time = round(time.time() - start_time, 3)
            if hex.player_turn == 1:
                AI2_avg_times[n].append(lasted_time)
            else:
                AI1_avg_times[n].append(lasted_time)
            print('Took', lasted_time, 's to place a move')
            winner = hex.check_game()
            # if there is a winner breaks
            if winner is not None:
                print('\n ================= Player', winner,
                      '\033[34m●\033[0m' if winner == 1 else '\033[31m●\033[0m', 'wins! =================\n')
                if winner == 1:
                    AI1_wins += 1
                    if winner == starting_player:
                        AI1_wins_when_starting += 1
                else:
                    AI2_wins += 1
                    if winner == starting_player:
                        AI2_wins_when_starting += 1
                break
            i += 1
        game_lasted.append(i+1)
        starting_player = -starting_player

    meansA1 = []
    stdsA1 = []
    for times in AI1_avg_times:
        meansA1.append(np.mean(np.asarray(times)))
        stdsA1.append(np.std(np.asarray(times)))

    meansA2 = []
    stdsA2 = []
    for times in AI2_avg_times:
        meansA2.append(np.mean(np.asarray(times)))
        stdsA2.append(np.std(np.asarray(times)))

    stats, p = sc.stats.mannwhitneyu(np.asarray(meansA1), np.asarray(meansA2), alternative='less')


    alpha = 0.05
    if p > alpha:
        mw_res = 'same performances!'
    else:
        mw_res = 'different performances!'

    return AI1_wins, AI2_wins, AI1_wins_when_starting, AI2_wins_when_starting,\
        np.mean(np.asarray(meansA1)), np.mean(np.asarray(stdsA1)), \
        np.mean(np.asarray(meansA2)), np.mean(np.asarray(stdsA2)), \
        np.mean(np.asarray(game_lasted)), \
        mw_res

def formatted_test(config, N):
    print('\n===========================================================================')
    print('Board size', config['board_size'])
    print(config['AI1_node_value_heuristic'].__class__.__name__, 'VS',
          config['AI2_node_value_heuristic'].__class__.__name__)
    print(config['AI1_node_ordering_heuristic'].__class__.__name__, 'VS',
          config['AI2_node_ordering_heuristic'].__class__.__name__)
    print('max depth', config['AI1_max_depth'], 'VS max depth', config['AI2_max_depth'])
    print('===========================================================================\n')
    AI1_wins, AI2_wins, AI1_wins_starting, AI2_wins_starting,\
        AI1_avg_move_time, AI1_std_move_time, \
        AI2_avg_move_time, AI2_std_move_time, \
        game_lasted, \
        mw_res = test(config, N)
    print('[Results averaged on', N, 'trials]')

    headers = ['', config['AI1_node_value_heuristic'].__class__.__name__, config['AI2_node_value_heuristic'].__class__.__name__]
    table = [['N of wins',  round(AI1_wins, 5), round(AI2_wins, 5)],
             ['N of wins as starting player', round(AI1_wins_starting, 5), round(AI2_wins_starting, 5)],
             ['E[MoveTime]', round(AI1_avg_move_time, 5), round(AI2_avg_move_time, 5)],
             ['Std[MoveTime]', round(AI1_std_move_time, 5), round(AI2_std_move_time, 5)],
             ['Avg move times with Mann-Whitney test', mw_res],
             ['Number of moves to win', round(game_lasted, 5)]]

    print(tabulate(table, headers=headers), '\n')
    print(tabulate(table, headers=headers, tablefmt='latex', maxcolwidths=[12, None, None]))

# the game configs
board_size = 11
config = {
    'board_size': board_size,
    'max_depth': 2,
    'AI1_node_value_heuristic': None,
    'AI1_node_ordering_heuristic': None,
    'AI2_node_value_heuristic': None,
    'AI2_node_ordering_heuristic': None,
}


# ============================================== TESTS =====================================================


# 1
# ConnectedValueHeuristic VS ShortestPathValueHeuristic
# with RandomOrderHeuristic
# max_depth = 2 VS max_depth = 2


N = 30
config['AI1_max_depth'] = 2
config['AI2_max_depth'] = 2
config['AI1_node_value_heuristic'] = heuristics.ConnectedValueHeuristic()
config['AI1_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
config['AI2_node_value_heuristic'] = heuristics.ShortestPathValueHeuristic()
config['AI2_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
formatted_test(config, N)


# 2
# ShortestPathValueHeuristic VS YReductionValueHeuristic
# with RandomOrderHeuristic
# max_depth = 2 VS max_depth = 2


N = 30
config['AI1_max_depth'] = 2
config['AI2_max_depth'] = 2
config['AI1_node_value_heuristic'] = heuristics.ShortestPathValueHeuristic()
config['AI1_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
config['AI2_node_value_heuristic'] = heuristics.YReductionValueHeuristic()
config['AI2_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
formatted_test(config, N)


# 3
# ShortestPathValueHeuristic VS TwoDistanceValueHeuristic
# with RandomOrderHeuristic
# max_depth = 2 VS max_depth = 2


N = 30
config['AI1_max_depth'] = 2
config['AI2_max_depth'] = 2
config['AI1_node_value_heuristic'] = heuristics.ShortestPathValueHeuristic()
config['AI1_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
config['AI2_node_value_heuristic'] = heuristics.TwoDistanceValueHeuristic()
config['AI2_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
formatted_test(config, N)


# 4
# TwoDistanceValueHeuristic VS MaxFlowValueHeuristic
# with RandomOrderHeuristic
# max_depth = 2 VS max_depth = 2


N = 20
config['board_size'] = 8
config['AI1_max_depth'] = 2
config['AI2_max_depth'] = 2
config['AI1_node_value_heuristic'] = heuristics.TwoDistanceValueHeuristic()
config['AI1_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
config['AI2_node_value_heuristic'] = heuristics.MaxFlowValueHeuristic()
config['AI2_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
formatted_test(config, N)


# 5
# TwoDistanceValueHeuristic VS ResistanceValueHeuristic
# with RandomOrderHeuristic
# max_depth = 2 VS max_depth = 2


N = 20
config['board_size'] = 8
config['AI1_max_depth'] = 2
config['AI2_max_depth'] = 2
config['AI1_node_value_heuristic'] = heuristics.TwoDistanceValueHeuristic()
config['AI1_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
config['AI2_node_value_heuristic'] = heuristics.ResistanceValueHeuristic()
config['AI2_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
formatted_test(config, N)


# 6
# TwoDistanceValueHeuristic VS TwoDistanceValueHeuristic
# with ChargeHeuristic, with RandomOrderHeuristic
# max_depth = 2 VS max_depth = 2


N = 30
config['board_size'] = 11
config['AI1_max_depth'] = 2
config['AI2_max_depth'] = 2
config['AI1_node_value_heuristic'] = heuristics.TwoDistanceValueHeuristic()
config['AI1_node_ordering_heuristic'] = heuristics.ChargeHeuristic(config['board_size'])
config['AI2_node_value_heuristic'] = heuristics.TwoDistanceValueHeuristic()
config['AI2_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
formatted_test(config, N)


# 7
# TwoDistanceValueHeuristic VS TwoDistanceValueHeuristic
# with ChargeHeuristic
# max_depth = 2 VS max_depth = 3

N = 20
config['board_size'] = 8
config['AI1_max_depth'] = 2
config['AI2_max_depth'] = 3
config['AI1_node_value_heuristic'] = heuristics.TwoDistanceValueHeuristic()
config['AI1_node_ordering_heuristic'] = heuristics.ChargeHeuristic(config['board_size'])
config['AI2_node_value_heuristic'] = heuristics.TwoDistanceValueHeuristic()
config['AI2_node_ordering_heuristic'] = heuristics.ChargeHeuristic(config['board_size'])
formatted_test(config, N)


