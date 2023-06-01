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
import hex_AI
from hex import Hex
import heuristics

def test(config, trials):

    starting_player = 1

    AI1_wins = 0
    AI2_wins = 0

    AI1_avg_time_total = 0
    AI2_avg_time_total = 0

    # run trials run of the experiment
    for n in range(trials):
        print('Trial', n, '/', trials, '- starting_player:', starting_player)
        # init the game
        hex = Hex(config['board_size'], starting_player=starting_player)
        i = 0
        AI1_avg_time = 0
        AI2_avg_time = 0
        # until game finishes
        while True:
            print('\nTurn', i, '- Player', hex.player_turn)
            # running game turn and measuring play time
            start_time = time.time()
            hex_AI.computer_turn_testing(hex, config)
            lasted_time = round(time.time() - start_time, 3)
            if hex.player_turn == 1:
                AI2_avg_time += lasted_time
            else:
                AI1_avg_time += lasted_time
            print('Took', lasted_time, 's')
            winner = hex.check_game()
            # if there is a winner breaks
            if winner is not None:
                print('\n ================= Player', winner,
                      '\033[34m●\033[0m' if winner == 1 else '\033[31m●\033[0m', 'wins! =================\n')
                if winner == 1:
                    AI1_wins += 1
                else:
                    AI2_wins += 1
                break
            i += 1
        AI1_avg_time /= i
        AI2_avg_time /= i
        AI1_avg_time_total += AI1_avg_time
        AI2_avg_time_total += AI2_avg_time
        starting_player = -starting_player

    AI1_avg_time_total /= trials
    AI2_avg_time_total /= trials

    return AI1_wins, AI2_wins, AI1_avg_time_total, AI2_avg_time_total

def formatted_test(config, N):
    print('\n===========================================================================')
    print('Board size', config['board_size'])
    print(config['AI1_node_value_heuristic'].__class__.__name__, 'VS',
          config['AI2_node_value_heuristic'].__class__.__name__)
    print('max depth', config['AI1_max_depth'], '- max depth', config['AI2_max_depth'])
    print('===========================================================================\n')
    AI1_wins, AI2_wins, AI1_avg_time_total, AI2_avg_time_total = test(config, N)
    print('[On', N, 'trials]')
    print(config['AI1_node_value_heuristic'].__class__.__name__, 'wins:', AI1_wins,
          config['AI2_node_value_heuristic'].__class__.__name__, 'wins:', AI2_wins)
    print(config['AI1_node_value_heuristic'].__class__.__name__, 'average move time:', AI1_avg_time_total,
          config['AI2_node_value_heuristic'].__class__.__name__, 'average move time:', AI2_avg_time_total)


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

"""
# 1
# ConnectedValueHeuristic VS ShortestPathValueHeuristic
# with RandomOrderHeuristic
# max_depth = 2 VS max_depth = 2
# 20 trials, 10 times starts the first, and 10 the second


N = 20
config['AI1_max_depth'] = 2
config['AI2_max_depth'] = 2
config['AI1_node_value_heuristic'] = heuristics.ConnectedValueHeuristic()
config['AI1_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
config['AI2_node_value_heuristic'] = heuristics.ShortestPathValueHeuristic()
config['AI2_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
formatted_test(config, N)

# RESULT:
# ConnectedValueHeuristic wins: 0
# ShortestPathValueHeuristic wins: 20
# ConnectedValueHeuristic average move time: 0.15323649923509514
# ShortestPathValueHeuristic average move time: 0.18827420919331053
# COMMENT:

# 2
# ShortestPathValueHeuristic VS YReductionValueHeuristic
# with RandomOrderHeuristic
# max_depth = 2 VS max_depth = 2
# 20 trials, 10 times starts the first, and 10 the second

N = 20
config['AI1_max_depth'] = 2
config['AI2_max_depth'] = 2
config['AI1_node_value_heuristic'] = heuristics.ShortestPathValueHeuristic()
config['AI1_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
config['AI2_node_value_heuristic'] = heuristics.YReductionValueHeuristic()
config['AI2_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
formatted_test(config, N)

# RESULT:
# ShortestPathValueHeuristic wins: 15
# YReductionValueHeuristic wins: 5
# ShortestPathValueHeuristic average move time: 0.2583786973439321
# YReductionValueHeuristic average move time: 0.46483719183595884
# COMMENT:


# 3
# ShortestPathValueHeuristic VS TwoDistanceValueHeuristic
# with RandomOrderHeuristic
# max_depth = 2 VS max_depth = 2
# 20 trials, 10 times starts the first, and 10 the second

N = 20
config['AI1_max_depth'] = 2
config['AI2_max_depth'] = 2
config['AI1_node_value_heuristic'] = heuristics.ShortestPathValueHeuristic()
config['AI1_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
config['AI2_node_value_heuristic'] = heuristics.TwoDistanceValueHeuristic()
config['AI2_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
formatted_test(config, N)

# RESULT:
# ShortestPathValueHeuristic wins: 0
# TwoDistanceValueHeuristic wins: 20
# ShortestPathValueHeuristic average move time: 0.4712842316209004
# TwoDistanceValueHeuristic average move time: 0.4964141600123648
# COMMENT:


# 4
# TwoDistanceValueHeuristic VS MaxFlowValueHeuristic
# with RandomOrderHeuristic
# max_depth = 2 VS max_depth = 2
# 20 trials, 10 times starts the first, and 10 the second

N = 6
config['board_size'] = 8
config['AI1_max_depth'] = 2
config['AI2_max_depth'] = 2
config['AI1_node_value_heuristic'] = heuristics.TwoDistanceValueHeuristic()
config['AI1_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
config['AI2_node_value_heuristic'] = heuristics.MaxFlowValueHeuristic()
config['AI2_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
formatted_test(config, N)

# RESULT:
# TwoDistanceValueHeuristic wins: 6 
# MaxFlowValueHeuristic wins: 0
# TwoDistanceValueHeuristic average move time: 0.119840522875817 
# MaxFlowValueHeuristic average move time: 1.6200286764705882
# COMMENT:


# 5
# TwoDistanceValueHeuristic VS ResistanceValueHeuristic
# with RandomOrderHeuristic
# max_depth = 2 VS max_depth = 2
# 20 trials, 10 times starts the first, and 10 the second

N = 6
config['board_size'] = 8
config['AI1_max_depth'] = 2
config['AI2_max_depth'] = 2
config['AI1_node_value_heuristic'] = heuristics.TwoDistanceValueHeuristic()
config['AI1_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
config['AI2_node_value_heuristic'] = heuristics.ResistanceValueHeuristic()
config['AI2_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
formatted_test(config, N)

# RESULT: 
# TwoDistanceValueHeuristic wins: 6 
# ResistanceValueHeuristic wins: 0
# TwoDistanceValueHeuristic average move time: 0.12909754901960785 
# ResistanceValueHeuristic average move time: 17.223876348039212
# COMMENT:


# 6
# TwoDistanceValueHeuristic VS TwoDistanceValueHeuristic
# with ChargeHeuristic, with RandomOrderHeuristic
# max_depth = 2 VS max_depth = 2
# 20 trials, 10 times starts the first, and 10 the second

N = 20
config['board_size'] = 11
config['AI1_max_depth'] = 2
config['AI2_max_depth'] = 2
config['AI1_node_value_heuristic'] = heuristics.TwoDistanceValueHeuristic()
config['AI1_node_ordering_heuristic'] = heuristics.ChargeHeuristic(config['board_size'])
config['AI2_node_value_heuristic'] = heuristics.TwoDistanceValueHeuristic()
config['AI2_node_ordering_heuristic'] = heuristics.RandomOrderHeuristic()
formatted_test(config, N)

# RESULT:
# TwoDistanceValueHeuristic with Charge Ordering wins: 13
# TwoDistanceValueHeuristic wins: 7
# TwoDistanceValueHeuristic with Charge Ordering wins average move time: 0.3478755031722586
# TwoDistanceValueHeuristic average move time: 0.551365240678479
"""

# 7
# TwoDistanceValueHeuristic VS TwoDistanceValueHeuristic
# max_depth = 2 VS max_depth = 3
# 10 trials, 5 times starts the first, and 5 the second

N = 10
config['board_size'] = 8
config['AI1_max_depth'] = 2
config['AI2_max_depth'] = 3
config['AI1_node_value_heuristic'] = heuristics.TwoDistanceValueHeuristic()
config['AI1_node_ordering_heuristic'] = heuristics.ChargeHeuristic(config['board_size'])
config['AI2_node_value_heuristic'] = heuristics.TwoDistanceValueHeuristic()
config['AI2_node_ordering_heuristic'] = heuristics.ChargeHeuristic(config['board_size'])
formatted_test(config, N)

# RESULT:


