""""
==========================================================
            Intelligent Agents: Final project
                    A.A. 2022-2023
----------------------------------------------------------
                   Luigi Schiavone
=========================================================

FILE: this file contains the game application logic

"""
import sys
import time
from hex import Hex
import pygame
import heuristics
import hex_AI
from ui import UI


def check_button_pressed(event):
    """
    Check the keyboard pressed event and close the application if the user wants to exit

    :param event: the gui event to check
    :return: True if the player pressed spacebar
    """
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        return True


def user_turn(game, ui, config):
    """
    Plays a move from the user.

    :param game: the game object
    :param ui: the game ui object
    :return:
    """
    player = game.player_turn
    while True:
        move = None
        while move is None:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                check_button_pressed(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for _, rect in enumerate(ui.rects):
                        # getting the mouse collided coordinate
                        if rect.collidepoint(mouse_pos):
                            # getting the move
                            move = ui.get_true_coordinates(_)
                            break
        moved = game.play_move(move)
        if moved:
            # updates the ui
            node = move[0] * ui.board_size + move[1]
            ui.color[node] = ui.blue if player is ui.BLUE_PLAYER else ui.red
            print(move)
            break


# the game configs
board_size = 11
config = {
    'board_size': board_size,
    'AI_vs_AI': True,
    'max_depth': 2,
    'AI1_node_value_heuristic': heuristics.ResistanceValueHeuristic(),
    'AI1_node_ordering_heuristic': heuristics.RandomOrderHeuristic(),
    'AI2_node_value_heuristic': heuristics.YReductionValueHeuristic(),
    'AI2_node_ordering_heuristic': heuristics.RandomOrderHeuristic(),
    'starting_player': -1
}


def main():
    """
    The main app function.

    It will execute games, according the defined config, forever.
    After a game you have to press SPACE to restart another game.
    """

    while True:
        # init pygame
        pygame.init()
        pygame.display.set_caption("HexAI - by Luigi Schiavone")
        # inti the ui
        ui = UI(config['board_size'])
        player_turn = {ui.BLUE_PLAYER: hex_AI.computer_turn, ui.RED_PLAYER: hex_AI.computer_turn} if config['AI_vs_AI'] \
            else {ui.BLUE_PLAYER: hex_AI.computer_turn, ui.RED_PLAYER: user_turn}
        # init the game
        hex = Hex(config['board_size'], starting_player=config['starting_player'])
        print('Player', config['starting_player'],
              '\033[34m●\033[0m' if config['starting_player'] == ui.BLUE_PLAYER else '\033[31m●\033[0m', 'starts!')
        # draws the terminal and gui
        hex.draw_board_tty()
        ui.draw_board()
        ui.draw_stats_left(config, J=config['AI1_node_value_heuristic'].compute(hex), player_turn=hex.player_turn,
                           winner=None)
        if config['AI_vs_AI']:
            ui.draw_stats_right(config, J=config['AI2_node_value_heuristic'].compute(hex), player_turn=hex.player_turn)
        else:
            ui.draw_user_stats()
        pygame.display.update()
        ui.clock.tick(30)
        i = 0
        # until game finishes
        while True:
            print('\nTurn', i, '- Player', hex.player_turn,
                  '\033[34m●\033[0m' if hex.player_turn == ui.BLUE_PLAYER else '\033[31m●\033[0m', 'moves: ', end='')
            # running game turn and measuring play time
            start_time = time.time()
            player_turn[hex.player_turn](hex, ui, config)
            lasted_time = round(time.time() - start_time, 3)
            print('Took', lasted_time, 's')
            winner = hex.check_game()
            # updates the ui
            hex.draw_board_tty()
            ui.draw_board()
            ui.draw_stats_left(config, J=config['AI1_node_value_heuristic'].compute(hex), player_turn=hex.player_turn,
                               winner=winner, move_lasted=lasted_time)
            if config['AI_vs_AI']:
                ui.draw_stats_right(config, J=config['AI2_node_value_heuristic'].compute(hex),
                                    player_turn=hex.player_turn)
            else:
                ui.draw_user_stats()
            pygame.display.update()
            ui.clock.tick(30)
            # if there is a winner breaks
            if winner is not None:
                print('\n ================= Player', winner,
                      '\033[34m●\033[0m' if winner == ui.BLUE_PLAYER else '\033[31m●\033[0m', 'wins! =================')
                break
            i += 1
        # check for a game restart
        while True:
            restart = False
            for event in pygame.event.get():
                if check_button_pressed(event):
                    restart = True
            if restart:
                break


# Launching the app
main()
