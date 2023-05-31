# Tic-Tac-Toe using Mini-Max Algorithm

class TicTacToe:

    def __init__(self):
        self._board = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def draw_board(self):
        print("Current State Of Board : \n\n")
        for i in range(0, 9):
            if (i > 0) and (i % 3) == 0:
                print("\n")
            if self._board[i] == 0:
                print("- ", end=" ")
            if self._board[i] == 1:
                print("O ", end=" ")
            if self._board[i] == -1:
                print("X ", end=" ")
        print("\n\n")

    def check(self):
        cb = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        moves_exhausted = self._board.count(0) == 0
        for i in range(0, 8):
            if (self._board[cb[i][0]] != 0 and
                    self._board[cb[i][0]] == self._board[cb[i][1]] and
                    self._board[cb[i][0]] == self._board[cb[i][2]]):
                return self._board[cb[i][2]]
        # return draw if play is finished else None
        return 0 if moves_exhausted else None

    def play_move(self, player, move):
        if self._board[move] != 0:
            raise Exception('Move not admitted!')
        self._board[move] = player

    def reset_move(self, move):
        self._board[move] = 0

    def available_moves(self):
        moves = []
        for move in range(9):
            if self._board[move] == 0:
                moves.append(move)
        return moves

def computer_turn(game, player):
    maximize = (player == 1)    # player 1 want to maximize, player -1 to minimize
    _, move = minimax(game, player, maximize)
    game.play_move(player, move)

def minimax(game, player, maximize):
    winner = game.check()
    # if position is terminal (the game is ended) return the position value and no move can be done
    if winner is not None:
        return winner, None
    curr_minimax_value = -float('inf') if maximize else float('inf')
    # for each possible move at current position
    for move in game.available_moves():
        # suppose to play move
        game.play_move(player, move)
        # compute the minimax value using the opponent
        minimax_value, _ = minimax(game, (player * -1), not maximize)
        game.reset_move(move)
        # update the best move according the max/min minimax value
        if (maximize and minimax_value > curr_minimax_value) or (not maximize and minimax_value < curr_minimax_value):
            curr_minimax_value = minimax_value
            best_move = move
    # returning the minimax value and the best move for the player
    return curr_minimax_value, best_move

# Main Function.
def main():
    tictactoe = TicTacToe()
    for i in range(0, 9):
        if i % 2 == 0:
            computer_turn(tictactoe, 1)
        else:
            computer_turn(tictactoe, -1)
        tictactoe.draw_board()
        winner = tictactoe.check()
        if winner is not None:
            if winner == 0:
                print("Draw!!!")
            elif winner == -1:
                print("X Wins!!! Y Loose !!!")
            elif winner == 1:
                print("X Loose!!! O Wins !!!!")
            break


# ---------------#
main()
# ---------------#
