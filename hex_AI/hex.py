""""
==========================================================
            Intelligent Agents: Final project
                    A.A. 2022-2023
----------------------------------------------------------
                   Luigi Schiavone
=========================================================

FILE: this file contains the game logic

"""
from heapq import heappop, heappush


class Hex:
    """
    A class which realizes the Hex game logic
    """

    def __init__(self, n, starting_player=1):
        """
        Initializes a new game.

        :param n: the dimension of the board
        :param starting_player: 1 or -1
        """
        # the dimension of the grid
        self.n = n
        # the grid
        self.grid = [[0] * n for _ in range(n)]
        # a history of the game.
        self.history = []
        # the player turn
        self.player_turn = starting_player

    def check_game(self):
        """
        :return: 1 if 1 wins, -1 if -1 wins, None if the game is not finished yet.
        """
        if self._has_connection(1):
            return 1
        elif self._has_connection(-1):
            return -1
        else:
            return None

    def _is_move_in_grid(self, r, c):
        """
        :param r: a row value
        :param c: a column value
        :return: True if the move is in the grid else False
        """
        return 0 <= r < self.n and 0 <= c < self.n

    def play_move(self, move):
        """
        Plays the specified move (r, c) for current turn player, if valid

        :param move: a tuple of integers (r, c)
        :return: False if game already ended or move is not valid, else True
        """
        # game is ended (someone won)
        if self.check_game() is not None:
            return False
        # if move is valid
        r, c = move
        if self._is_move_in_grid(r, c) and self.grid[r][c] == 0:
            self.grid[r][c] = self.player_turn
            self.history.append((r, c))
            self.player_turn *= -1
            return True
        else:
            return False

    def undo_move(self):
        """
        Undo the last move.
        """
        self.player_turn *= -1
        r, c = self.history.pop()
        self.grid[r][c] = 0

    def _has_connection(self, player):
        """
        :param player: 1 or -1
        :return: True if there is a connection between edges of player
        """
        # performs a BFS from one side to another
        # build a queue with the border cells according players
        # (distance_from_target, r, c)
        if player == 1:
            queue = [(self.n, i, self.n) for i in range(self.n-1)]
        else:
            queue = [(self.n, self.n, i) for i in range(self.n-1)]
        # ancestors cells
        ancestors = dict()
        # while there are cells in the queue
        while queue:
            # get a cell
            distance_from_target, r, c = heappop(queue)
            # if distance from the target is 0 there is a connection
            if distance_from_target == 0:
                return True
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
                        adj_cell = self.grid[adj_r][adj_c]
                except IndexError:
                    # if the cell is not legal ignore it
                    continue
                # if the adj_cell belong to the player and is not an ancestor add it to the queue
                if adj_cell == player and (adj_r, adj_c) not in ancestors:
                    ancestors[(adj_r, adj_c)] = (r, c)
                    heappush(queue, (adj_c if player == 1 else adj_r, adj_r, adj_c))
        # if execution reach this point there is no connection for player
        return False

    def available_moves(self):
        """
        :return: a list of all remaining valid moves.
        """
        moves = []
        for r in range(0, self.n):
            for c in range(0, self.n):
                if self.grid[r][c] == 0:
                    moves.append((r, c))
        return moves

    def draw_board_tty(self):
        """
        Draws the board on the terminal.
        """
        # spacing should be odd for things to be consistent
        spacing = 3
        string = '\n' + ' ' * (2 + (spacing + 1) // 2)
        for i in range(self.n):
            string += ('{:' + str(spacing + 1) + '}').format(str(i) + ':')
        string += '\n' + ' ' * (3 + (spacing + 1) // 2) + ('\033[31m■\033[0m' + ' ' * spacing) * self.n
        for i, row in enumerate(self.grid):
            string += ('\n' + '{:>' + str(2 + i * (spacing + 1) // 2) + '} ' + '\033[34m■\033[0m').format(str(i) + ':')
            for j, num in enumerate(row):
                if self.history and self.history[-1] == (i,j):
                    string += ' ' * (spacing - 1) + '('
                elif self.history and self.history[-1] == (i,j-1):
                    string += ')' + ' ' * (spacing - 1)
                else:
                    string += ' ' * spacing

                if num == 0:
                    string += '·'
                elif num < 0:
                    string += '\033[31m●\033[0m'
                else:
                    string += '\033[34m●\033[0m'

            if self.history and self.history[-1] == (i, self.n-1):
                string += ')' + ' ' * (spacing-1)
            else:
                string += ' ' * spacing
            string += '\033[34m■\033[0m'
        string += '\n' + ' ' * (4 + self.n * (spacing + 1) // 2) + (' ' * spacing + '\033[31m■\033[0m') * self.n
        print(string)


# TEST


if __name__ == "__main__":
    hex = Hex(5, starting_player=1)
    hex.play_move((2, 3))
    hex.draw_board_tty()
    hex.play_move((1, 2))
    hex.draw_board_tty()
    hex.play_move((1, 4))
    hex.draw_board_tty()
    hex.play_move((1, 2))
    hex.draw_board_tty()
    hex.undo_move()
    hex.draw_board_tty()
    hex.play_move((2, 4))
    hex.draw_board_tty()
    hex.play_move((2, 2))
    hex.play_move((3, 4))
    hex.play_move((0, 2))
    hex.play_move((1, 3))
    hex.play_move((3, 2))
    hex.play_move((2, 1))
    hex.play_move((4, 2))
    hex.draw_board_tty()
    print(hex.check_game())