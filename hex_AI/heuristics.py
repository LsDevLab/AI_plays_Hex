"""
==========================================================
            Intelligent Agents: Final project
                    A.A. 2022-2023
----------------------------------------------------------
                   Luigi Schiavone
=========================================================

FILE: this file contains all the heuristic classes I used in the game search

"""
import itertools
import math
import random
import time
from copy import deepcopy
from heapq import heappush, heappop
import networkx as nx
from hex import Hex
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# =============================================== Node Value Heuristics ===============================================


# ValueHeuristic interface
class ValueHeuristic():

    def compute(self, game):
        pass

class ConnectedValueHeuristic(ValueHeuristic):
    # J = k_p2 - k_p1

    def compute(self, game):
        # J measures who is the player closer to winning
        k_p1 = self._connected(game, 1)
        k_p2 = self._connected(game, -1)
        return k_p1 - k_p2

    def _connected(self, game, player):
        counted = set()
        connected = 0
        for r in range(game.n):
            for c in range(game.n):
                if game.grid[r][c] == player:
                    for dr, dc in [(-1, 0), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1)]:
                        adj_r = r + dr
                        adj_c = c + dc
                        if game._is_move_in_grid(adj_r, adj_c) and \
                                game.grid[adj_r][adj_c] == player and (adj_r, adj_c) not in counted:
                            counted.add((adj_r, adj_c))
                            connected += 1
        return connected

# The machine intelligence Hex project - 6.2.1
class ShortestPathValueHeuristic(ValueHeuristic):
    # J = k_p2 - k_p1
    # k_pi is the number of non-occupied cells on the SP for player i

    def compute(self, game):
        # J measures who is the player closer to winning
        k_p1 = self._sp_distance(game, 1)
        k_p2 = self._sp_distance(game, -1)
        return k_p2 - k_p1

    def _sp_distance(self, game, player):
        # performs a BFS from one side to another
        # build a queue with the border cells according players
        # (distance_so_far, distance_from_target, r, c)
        if player == 1:
            queue = [(0, game.n, i, game.n) for i in range(game.n-1)]
        else:
            queue = [(0, game.n, game.n, i) for i in range(game.n - 1)]
        # ancestors cells
        ancestors = set()
        # while there are cells in the queue
        while queue:
            # get a cell
            distance_so_far, distance_from_target, r, c = heappop(queue)
            # if distance from the target is 0 there is a connection
            if distance_from_target == 0:
                return distance_so_far
            # for each adjacent cell
            for dr, dc in [(-1, 0), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1)]:
                adj_r = r + dr
                adj_c = c + dc
                # check if the adjacent cell is in bound
                # try catch is faster than calling _is_move_in_grid
                try:
                    if adj_r < 0 or adj_c < 0:
                        continue
                    else:
                        adj_cell = game.grid[adj_r][adj_c]
                except IndexError:
                    # if the cell is not legal ignore it
                    continue
                # if the adj_cell belong to the player and is not an ancestor add it to the queue
                if adj_cell == player and (adj_r, adj_c) not in ancestors:
                    ancestors.add((adj_r, adj_c))
                    heappush(queue, (distance_so_far, adj_c if player == 1 else adj_r, adj_r, adj_c))
                # unoccupied cells are used to increase the distance #TODO: TOUNDERSTANTBETTER
                elif adj_cell == 0 and (adj_r, adj_c) not in ancestors:
                    ancestors.add((adj_r, adj_c))
                    heappush(queue, (distance_so_far + 1, adj_c if player == 1 else adj_r, adj_r, adj_c))

        # can't reach the other side, distance is infinite
        return float('inf')

# pag 37 jackmsc.pdf
class TwoDistanceValueHeuristic(ValueHeuristic):

    def compute(self, game):
        winner = game.check_game()
        # J measures who is the player closer to winning
        k_p1 = self._two_distance(game, 1)
        k_p2 = self._two_distance(game, -1)
        J = k_p2 - k_p1
        if math.isinf(J):
            J = int(math.copysign(100, J)) + ShortestPathValueHeuristic().compute(game)
        if math.isnan(J):
            J = ShortestPathValueHeuristic().compute(game)
        return J

    def _two_distance(self, game, player):
        # performs a BFS from one side to another
        # build a queue with the border cells according players
        # (distance_so_far, distance_from_target, r, c, (r, c))
        if player == 1:
            queue = [(0, game.n, i, game.n, (i, game.n)) for i in range(-1, game.n)]
        else:
            queue = [(0, game.n, game.n, i, (game.n, i)) for i in range(-1, game.n)]
        # for each cell the best adjacent cell
        best_neighbors = [[None] * game.n for _ in range(game.n)]
        # the best cell that's adjacent to the opposite wall
        best_opposite = None
        # ancestors cells
        ancestors = set()
        # while there are cells in the queue
        while queue:
            # get a cell
            distance_so_far, distance_from_target, r, c, neighbor = heappop(queue)
            # if distance from the target is 0 there is a connection
            if distance_from_target == 0:
                if best_opposite is None:
                    best_opposite = neighbor
                elif best_opposite != neighbor:
                    return distance_so_far
            # for each adjacent cell
            for dr, dc in [(-1, 0), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1)]:
                adj_r = r + dr
                adj_c = c + dc
                # check if the adjacent cell is in bound
                # try catch is faster than calling _is_move_in_grid
                try:
                    if adj_r < 0 or adj_c < 0:
                        continue
                    else:
                        adj_cell = game.grid[adj_r][adj_c]
                except IndexError:
                    # if the cell is not legal ignore it
                    continue
                # if the adj_cell not occupied and is not an ancestor
                if adj_cell == 0 and (adj_r, adj_c) not in ancestors:
                    # update best neighbor of adjacent cell
                    if best_neighbors[adj_r][adj_c] is None:
                        best_neighbors[adj_r][adj_c] = neighbor
                    elif best_neighbors[adj_r][adj_c] != neighbor:
                        ancestors.add((adj_r, adj_c))
                        heappush(queue, (distance_so_far + 1, adj_c if player == 1 else adj_r, adj_r, adj_c, (adj_r, adj_c)))
                # if the adj_cell belong to the player and is not an ancestor
                if adj_cell == player and (adj_r, adj_c) not in ancestors:
                    # update best neighbor of adjacent cell
                    if best_neighbors[adj_r][adj_c] is None:
                        best_neighbors[adj_r][adj_c] = neighbor
                        # extend the neighborhood to all the connected block of cells
                        heappush(queue, (distance_so_far, adj_c if player == 1 else adj_r, adj_r, adj_c, neighbor))
                    elif best_neighbors[adj_r][adj_c] != neighbor:
                        ancestors.add((adj_r, adj_c))
                        best_neighbors[adj_r][adj_c] = neighbor
                        heappush(queue, (distance_so_far, adj_c if player == 1 else adj_r, adj_r, adj_c, neighbor))

        # can't reach the other side, distance is infinite
        return math.inf

# Pag 8 y_hex.pdf
class MaxFlowValueHeuristic(ValueHeuristic):

    def compute(self, game):
        # J measures who is the player closer to winning
        k_p1 = self._max_flow(game, 1)
        k_p2 = self._max_flow(game, -1)
        return k_p1 - k_p2

    def get_coord_label(self, r1, c1, r2, c2, n):
        return str(r1) + '_' + str(c1), str(r2) + '_' + str(c2)

    def _max_flow(self, game, player):
        cell_positions = dict()
        G = nx.DiGraph()
        # for each cell
        for r in range(game.n):
            for c in range(game.n - 1, -1, -1):
                if game.grid[r][c] != -player:
                    #print(str(r)+'_'+str(c))
                    cell_positions[str(r)+'_'+str(c)] = [c, -r]
                    # for each neighbour
                    for dr, dc in [(0, -1), (1, -1), (1, 0)]:
                        adj_r = r + dr
                        adj_c = c + dc
                        # if in bounds
                        try:
                            if adj_r < 0 or adj_c < 0 or adj_r >= game.n or adj_c >= game.n:
                                continue
                            else:
                                adj_cell = game.grid[adj_r][adj_c]
                        except IndexError:
                            # if the cell is not legal ignore it
                            continue
                        R = None
                        if game.grid[r][c] == player and game.grid[adj_r][adj_c] == player:
                            R = math.inf#1.0#0
                        elif (game.grid[r][c] == player and game.grid[adj_r][adj_c] == 0) or \
                                (game.grid[r][c] == 0 and game.grid[adj_r][adj_c] == player):
                            R = 1# game.n - c if player == 1 else r + 1#1#0.5
                        elif game.grid[r][c] == 0 and game.grid[adj_r][adj_c] == 0:
                            R = 1#game.n - c if player == 1 else r + 1#1#0.5
                        if R is not None:
                            rr, cc = self.get_coord_label(r, c, adj_r, adj_c, game.n)
                            #circuit.add('R' + rr + cc + ' ' + rr + ' ' + cc + ' ' + str(R))
                            G.add_edge(rr, cc, capacity=R)
        # adding edge cells and voltage
        if player == 1:
            for i in range(game.n):
                if game.grid[i][0] == player:
                    R = math.inf#1#0
                elif game.grid[i][0] == 0:
                    R = math.inf#0.5
                else:
                    continue
                rr, cc = self.get_coord_label(i, 0, 20, 20, game.n)
                #circuit.add('R' + rr + cc + ' ' + '0' + ' ' + str(R))
                G.add_edge(rr, '0', capacity=R)
                if game.grid[i][game.n-1] == player:
                    R = math.inf#1#0
                elif game.grid[i][game.n-1] == 0:
                    R = math.inf#0.5
                else:
                    continue
                rr, cc = self.get_coord_label(21, 21, i, game.n-1, game.n)
                #circuit.add('R' + rr + cc + ' ' + rr + ' ' + cc + ' ' + str(R))
                G.add_edge(rr, cc, capacity=R)
                cell_positions[rr] = [5, 0]
                cell_positions['0'] = [-2, 0]
            #rr, cc = self.get_coord_label(20, 20, 21, 21, game.n)
            #circuit.add('Vb ' + '0' + ' ' + cc + ' ' + str(1))
            try:
                flow_value, flow_dict = nx.maximum_flow(G, '21_21', '0')
            except nx.NetworkXUnbounded:
                flow_value = math.inf
        else:
            for j in range(game.n):
                if game.grid[0][j] == player:
                    R = math.inf  #1#0
                elif game.grid[0][j] == 0:
                    R = math.inf# 0.5
                else:
                    continue
                rr, cc = self.get_coord_label(22, 22, 0, j, game.n)
                cell_positions[rr] = [0, 2]
                cell_positions['0'] = [0, -5]
                #circuit.add('R' + rr + cc + ' ' + rr + ' ' + cc + ' ' + str(R))
                G.add_edge(rr, cc, capacity=R)
                if game.grid[game.n-1][j] == player:
                    R = math.inf#1#0
                elif game.grid[game.n-1][j] == 0:
                    R = math.inf#0.5
                else:
                    continue
                rr, cc = self.get_coord_label(game.n-1, j, 23, 23, game.n)
                #circuit.add('R' + rr + cc + ' ' + '0' + ' ' + str(R))
                G.add_edge(rr, '0', capacity=R)
            try:
                flow_value, flow_dict = nx.maximum_flow(G, '22_22', '0')
            except nx.NetworkXUnbounded:
                flow_value = math.inf
            #circuit.add('Vb ' + '0' + ' ' + cc+ ' ' + str(1))

        """nx.draw(G, pos=cell_positions, with_labels=True,
                    node_size=500, font_color='white', font_size=8)
        labels = {(u, v): round(G.edges[(u, v)]['capacity'], 2) for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, cell_positions, edge_labels=labels)
        plt.show()"""

        return flow_value

# The machine intelligence Hex project - 6.2.3
class ResistanceValueHeuristic(ValueHeuristic):

    def compute(self, game):
        # J measures who is the player closer to winning
        # time_start = time.time()
        k_p1 = self._resistance(game, 1)
        k_p2 = self._resistance(game, -1)
        # print('Computing resistance J took', time.time() - time_start)
        return k_p2 - k_p1

    def get_coord_label(self, r1, c1, r2, c2, n):
        return str(r1) + '_' + str(c1), str(r2) + '_' + str(c2)

    def _resistance(self, game, player):
        circuit = Circuit('Circuit for ' + str(player))
        # for each cell
        time_start = time.time()
        for r in range(game.n):
            for c in range(game.n - 1, -1, -1):
                if game.grid[r][c] != -player:
                    # for each neighbour
                    for dr, dc in [(0, -1), (1, -1), (1, 0)]:
                        adj_r = r + dr
                        adj_c = c + dc
                        # if in bounds
                        try:
                            if adj_r < 0 or adj_c < 0 or adj_r >= game.n or adj_c >= game.n:
                                continue
                            else:
                                adj_cell = game.grid[adj_r][adj_c]
                        except IndexError:
                            # if the cell is not legal ignore it
                            continue
                        R = None
                        if game.grid[r][c] == player and game.grid[adj_r][adj_c] == player:
                            R = 0
                        elif (game.grid[r][c] == player and game.grid[adj_r][adj_c] == 0) or \
                                (game.grid[r][c] == 0 and game.grid[adj_r][adj_c] == player):
                            R = 1
                        elif game.grid[r][c] == 0 and game.grid[adj_r][adj_c] == 0:
                            R = 1
                        if R is not None:
                            rr, cc = self.get_coord_label(r, c, adj_r, adj_c, game.n)
                            res = circuit.R(rr+'-'+cc, rr, cc, R@u_Ω)
                            #if c == game.n - 1:
                            #    res.plus.add_current_probe(circuit)
        #print('Building resistance graph took', time.time() - time_start)
        # adding edge cells and voltage
        time_start = time.time()
        if player == 1:
            for i in range(game.n):
                R = 0
                rr, cc = self.get_coord_label(i, 0, 20, 20, game.n)
                circuit.R(rr + '-' + cc, rr, cc, R@u_Ω)
                R = 0
                rr, cc = self.get_coord_label(21, 21, i, game.n-1, game.n)
                circuit.R(str(circuit.gnd) + '-' + cc, circuit.gnd, cc, R@u_Ω)

            rr, cc = self.get_coord_label(20, 20, 21, 21, game.n)
            circuit.V('b', circuit.gnd, rr, 1@u_V)

            simulator = circuit.simulator(temperature=25, nominal_temperature=25)
            analysis = simulator.operating_point()
            i = float(analysis.branches['vb'])
            Req = abs(1 / i) if i != 0 else math.inf
        else:
            for j in range(game.n):
                R = 0
                rr, cc = self.get_coord_label(22, 22, 0, j, game.n)
                circuit.R(rr + '-' + cc, rr, cc, R@u_Ω)
                R = 0
                rr, cc = self.get_coord_label(game.n-1, j, 23, 23, game.n)
                circuit.R(str(circuit.gnd) + '-' + rr, circuit.gnd, rr, R@u_Ω)

            rr, cc = self.get_coord_label(22, 22, 23, 23, game.n)
            circuit.V('r', circuit.gnd, rr, 1@u_V)

            simulator = circuit.simulator(temperature=25, nominal_temperature=25)
            analysis = simulator.operating_point()
            i = float(analysis.branches['vr'])
            Req = abs(1 / i) if i != 0 else math.inf
        #print('Computing Req took', time.time() - time_start)

        return Req

# Pag 10 y_hex.pdf
class YReductionValueHeuristic(ValueHeuristic):

    def compute(self, game):
        return self._yred(game)

    def _yred(self, game):
        ysize = game.n + game.n - 1
        yboard = list()
        for x in range(ysize):
            column = list()
            for y in range(ysize - x):
                if x < game.n and y < game.n:
                    state = game.grid[x][y]
                    column.append(
                        -1 if state == -1 else 1 if state == 1 else 0)
                elif x >= game.n:
                    column.append(-1)
                elif y >= game.n:
                    column.append(1)
            yboard.append(column)

        for iteration in range(ysize, 0, -1):
            for y in range(iteration - 1):
                for x in range(iteration - 1 - y):
                    p1 = yboard[x][y]
                    p2 = yboard[x + 1][y]
                    p3 = yboard[x][y + 1]
                    yboard[x][y] = (p1 + p2 + p3 - p1 * p2 * p3) / 2

        return yboard[0][0]


# ============================================= Node Ordering Heuristics =============================================


# OrderHeuristic interface
class OrderHeuristic():

    def sort(self, game, available_nodes):
        pass

class RandomOrderHeuristic(OrderHeuristic):

    def sort(self, game, available_moves):
        random.shuffle(available_moves)
        return available_moves

# found on Github of rjewsbury
# Treats stones as positive/negative charges, and tries to find saddle points in the field
# supposed to represent choosing contested moves
class ChargeHeuristic(OrderHeuristic):
    _max_charge = 9

    def __init__(self, size):
        self._base_charge = self.base_charge(size)
        self.size = size
        self.states = []

    def sort(self, game, available_nodes):
        child_val = self.get_child_values(game)
        return sorted(available_nodes, key=lambda m: child_val[m[0]][m[1]] * -game.player_turn)

    # finds an approximation of "curvature" if the board was an electric field
    def get_child_values(self, game):
        same_moves = 0
        for move, state in zip(game.history, self.states):
            if move == state[0][-1]:
                same_moves += 1
        if same_moves == 0:
            charge = deepcopy(self._base_charge)
        else:
            charge = deepcopy(self.states[same_moves-1][1])
        # remove the incorrect values
        self.states = self.states[:same_moves]

        for i in range(same_moves, len(game.history)):
            y, x = game.history[i]
            ChargeHeuristic.add_charge(game.grid[y][x], charge, x, y)

            self.states.append((game.history[:i+1], charge))
            # copy the board so the one stored isnt modified
            if i+1 < len(game.history):
                charge = deepcopy(charge)

        # for row in charge:
        #     print(list((('%.4f'%x) if x >= 0 else ('%.3f'%x) for x in row)))
        curve = [[0] * game.n for i in range(game.n)]
        for y, x in itertools.product(range(1, game.n + 1), repeat=2):
            k_e_w = ChargeHeuristic.curve(charge[y][x - 1], charge[y][x], charge[y][x + 1])
            k_ne_sw = ChargeHeuristic.curve(charge[y + 1][x - 1], charge[y][x], charge[y - 1][x + 1])
            k_nw_se = ChargeHeuristic.curve(charge[y + 1][x], charge[y][x], charge[y - 1][x])
            curve[y - 1][x - 1] = min(k_e_w, k_ne_sw, k_nw_se) * max(k_e_w, k_ne_sw, k_nw_se)*-game.player_turn
            # print('%.3f'%curve[y-1][x-1], end=',' if x < board.size else '\n')
        return curve

    @staticmethod
    def base_charge(size):
        base = [[0] * (size + 2) for y in range(size + 2)]
        # treat the end zones as lines of charge
        for i in range(size):
            ChargeHeuristic.add_charge(1, base, -1, i)
            ChargeHeuristic.add_charge(1, base, size, i)
            ChargeHeuristic.add_charge(-1, base, i, -1)
            ChargeHeuristic.add_charge(-1, base, i, size)
        return base

    @staticmethod
    def distance(x1, y1, x2, y2):
        manhattan = abs(x2 - x1) + abs(y2 - y1)
        diagonal = abs(x2 - x1) + abs(y2 - y1 + (x2 - x1))
        return min(manhattan, diagonal)

    @staticmethod
    def add_charge(sign, charge, x, y):
        x += 1
        y += 1
        for y2, x2 in itertools.product(range(len(charge)), repeat=2):
            if abs(charge[y2][x2]) == ChargeHeuristic._max_charge:
                continue
            if (y2, x2) == (y, x):
                charge[y2][x2] = sign * ChargeHeuristic._max_charge
            else:
                charge[y2][x2] += sign * (1 / ChargeHeuristic.distance(x, y, x2, y2) ** 2)
            charge[y2][x2] = max(min(charge[y2][x2], ChargeHeuristic._max_charge), -ChargeHeuristic._max_charge)

    @staticmethod
    def inverse_radius(h1, h2, h3):
        # simplified equation for finding the radius of a circle defined by 3 points
        # I've changed it a lot because I don't actually care about the number, just the relationship between numbers
        a = (1 + ((h1 - h2) / 4 / ChargeHeuristic._max_charge) ** 2)
        b = (1 + ((h3 - h2) / 4 / ChargeHeuristic._max_charge) ** 2)
        c = (4 + ((h1 - h3) / 4 / ChargeHeuristic._max_charge) ** 2)
        area = (h3 - 2 * h2 + h1)
        return area / (a * b * c)

    @staticmethod
    def curve(h1, h2, h3):
        # return ChargeHeuristic.inverse_radius(h1,h2,h3)
        if min(h1, h2, h3) == h2 or max(h1, h2, h3) == h2:
            # upwards or downwards curve
            return (h1 - h2) + (h3 - h2)
        else:
            # other curved shapes are not evaluatable
            return 0


# TEST


if __name__ == "__main__":
    hex = Hex(11, starting_player=1)
    hex.play_move((0, 3))
    hex.play_move((3, 1))
    hex.play_move((2, 1))
    hex.play_move((4, 2))
    hex.play_move((2, 2))
    hex.play_move((0, 2))
    hex.play_move((2, 2))
    hex.play_move((1, 0))
    hex.play_move((3, 0))
    hex.play_move((1, 1))
    #hex.play_move((1, 2))
    hex.draw_board_tty()
    times = time.time()
    print('Resist for player -1 (empty)', ResistanceValueHeuristic()._resistance(hex, -1))
    print(time.time() - times)
    #hex.play_move((2, 2))
    #hex.play_move((1, 0))
    times = time.time()
    print('Resist for player 1 (empty)', ResistanceValueHeuristic()._resistance(hex, 1))
    print(time.time() - times)
    times = time.time()
    print('Resistor heuristic', ResistanceValueHeuristic().compute(hex))
    print(time.time() - times)
    times = time.time()
    print('SP for player -1 (empty)', ShortestPathValueHeuristic()._sp_distance(hex, -1))
    print(time.time() - times)
    times = time.time()
    print('TwoDistance for player -1 (empty)', TwoDistanceValueHeuristic()._two_distance(hex, -1))
    print(time.time() - times)
    times = time.time()
    print('Connected for player 1', ConnectedValueHeuristic()._connected(hex, 1))
    print(time.time() - times)
    times = time.time()
    print('Maxflow for player -1', MaxFlowValueHeuristic()._max_flow(hex, -1))
    print(time.time() - times)
    print('Maxflow for player 1', MaxFlowValueHeuristic()._max_flow(hex, 1))
    print('MaxflowValue J', MaxFlowValueHeuristic().compute(hex))

