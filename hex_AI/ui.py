""""
==========================================================
            Intelligent Agents: Final project
                    A.A. 2022-2023
----------------------------------------------------------
                   Luigi Schiavone
=========================================================

FILE: this file contains the game ui class

"""
from math import cos, sin, pi, radians
import pygame
from pygame import gfxdraw
from pygame import time


class UI:
    """
    The GUI class for the game of Hex
    """

    def __init__(self, board_size: int):
        self.board_size = board_size
        assert 1 < self.board_size <= 26

        self.clock = time.Clock()
        self.hex_radius = 20
        self.x_offset, self.y_offset = 100, 100
        self.text_offset = 160
        self.screen = pygame.display.set_mode((810, 552))

        # Colors
        self.red = (222, 29, 47)
        self.blue = (0, 121, 251)
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)
        self.black = (40, 40, 40)
        self.gray = (70, 70, 70)

        # Players
        self.BLUE_PLAYER = 1
        self.RED_PLAYER = -1

        self.screen.fill(self.white)
        self.fonts = pygame.font.SysFont("avenir", 15)

        self.hex_lookup = {}
        self.rects, self.color, self.node = [], [self.white] * (self.board_size ** 2), None

    def draw_hexagon(self, surface: object, color: tuple, position: tuple, node: int):
        # Vertex count and radius
        n = 6
        x, y = position
        offset = 3

        # Outline
        self.hex_lookup[node] = [(x + (self.hex_radius + offset) * cos(radians(90) + 2 * pi * _ / n),
                                  y + (self.hex_radius + offset) * sin(radians(90) + 2 * pi * _ / n))
                                 for _ in range(n)]
        gfxdraw.aapolygon(surface,
                          self.hex_lookup[node],
                          color)

        # Shape
        gfxdraw.filled_polygon(surface,
                               [(x + self.hex_radius * cos(radians(90) + 2 * pi * _ / n),
                                 y + self.hex_radius * sin(radians(90) + 2 * pi * _ / n))
                                for _ in range(n)],
                               self.color[node])

        # Antialiased shape outline
        gfxdraw.aapolygon(surface,
                          [(x + self.hex_radius * cos(radians(90) + 2 * pi * _ / n),
                            y + self.hex_radius * sin(radians(90) + 2 * pi * _ / n))
                           for _ in range(n)],
                          self.gray)

        # Placeholder
        rect = pygame.draw.rect(surface,
                                self.color[node],
                                pygame.Rect(x - self.hex_radius + offset, y - (self.hex_radius / 2),
                                            (self.hex_radius * 2) - (2 * offset), self.hex_radius))
        self.rects.append(rect)

        # Bounding box (colour-coded)
        bbox_offset = [0, 3]

        # Top side
        if 0 < node < self.board_size:
            points = ([self.hex_lookup[node - 1][3][_] - bbox_offset[_] for _ in range(2)],
                      [self.hex_lookup[node - 1][4][_] - bbox_offset[_] for _ in range(2)],
                      [self.hex_lookup[node][3][_] - bbox_offset[_] for _ in range(2)])
            gfxdraw.filled_polygon(surface,
                                   points,
                                   self.red)
            gfxdraw.aapolygon(surface,
                              points,
                              self.red)

        # Bottom side
        if self.board_size ** 2 - self.board_size < node < self.board_size ** 2:
            points = ([self.hex_lookup[node - 1][0][_] + bbox_offset[_] for _ in range(2)],
                      [self.hex_lookup[node - 1][5][_] + bbox_offset[_] for _ in range(2)],
                      [self.hex_lookup[node][0][_] + bbox_offset[_] for _ in range(2)])
            gfxdraw.filled_polygon(surface,
                                   points,
                                   self.red)
            gfxdraw.aapolygon(surface,
                              points,
                              self.red)

        # Left side
        bbox_offset = [3, -3]

        if node % self.board_size == 0:
            if node >= self.board_size:
                points = ([self.hex_lookup[node - self.board_size][1][_] - bbox_offset[_] for _ in range(2)],
                          [self.hex_lookup[node - self.board_size][0][_] - bbox_offset[_] for _ in range(2)],
                          [self.hex_lookup[node][1][_] - bbox_offset[_] for _ in range(2)])
                gfxdraw.filled_polygon(surface,
                                       points,
                                       self.blue)
                gfxdraw.aapolygon(surface,
                                  points,
                                  self.blue)

        # Right side
        if (node + 1) % self.board_size == 0:
            if node > self.board_size:
                points = ([self.hex_lookup[node - self.board_size][4][_] + bbox_offset[_] for _ in
                           range(2)],
                          [self.hex_lookup[node - self.board_size][5][_] + bbox_offset[_] for _ in
                           range(2)],
                          [self.hex_lookup[node][4][_] + bbox_offset[_] for _ in range(2)])
                gfxdraw.filled_polygon(surface,
                                       points,
                                       self.blue)
                gfxdraw.aapolygon(surface,
                                  points,
                                  self.blue)

    def draw_text(self):

        for _ in range(self.board_size):
            # Columns
            text = self.fonts.render(str(_), True, self.gray, self.white)
            text_rect = text.get_rect()
            text_rect.center = (self.x_offset + (2 * self.hex_radius) * _, self.text_offset / 2 - 27)
            self.screen.blit(text, text_rect)

            # Rows
            text = self.fonts.render(str(_), True, self.gray, self.white)
            text_rect = text.get_rect()
            text_rect.center = (
                (self.text_offset / 4 + self.hex_radius * _, self.y_offset + (1.75 * self.hex_radius) * _))
            self.screen.blit(text, text_rect)

    def draw_board(self):
        self.screen.fill(self.white)

        counter = 0
        for row in range(self.board_size):
            for column in range(self.board_size):
                self.draw_hexagon(self.screen, self.white, self.get_coordinates(row, column), counter)
                counter += 1
        screen_size = self.screen.get_size()
        gfxdraw.filled_polygon(self.screen, [(0, screen_size[1]),(0, 100),(250, screen_size[1])], self.blue)
        gfxdraw.filled_polygon(self.screen, [(screen_size[0], 0),(530, 0),(screen_size[0], 490)], self.red)
        self.draw_text()

    def get_coordinates(self, row: int, column: int):
        x = self.x_offset + (2 * self.hex_radius) * column + self.hex_radius * row
        y = self.y_offset + (1.75 * self.hex_radius) * row

        return x, y

    def get_true_coordinates(self, node: int):
        return int(node / self.board_size), node % self.board_size

    def draw_stats_left(self, config, J, player_turn, winner, move_lasted='-'):
        text = pygame.font.SysFont("avenir", 30, bold=True).render('AI' , True, self.white)
        text_rect = text.get_rect()
        text_rect.x = 15
        text_rect.y = 245
        self.screen.blit(text, text_rect)
        text = pygame.font.SysFont("avenir", 18).render('Player' , True, self.white)
        text_rect = text.get_rect()
        text_rect.x = 15
        text_rect.y = 280
        self.screen.blit(text, text_rect)

        text = pygame.font.SysFont("avenir", 14).render('Algorithm:' , True, self.white)
        text_rect = text.get_rect()
        text_rect.x = 15
        text_rect.y = 320
        self.screen.blit(text, text_rect)
        text = pygame.font.SysFont("avenir", 12, True).render('a-b pruning', True, self.white)
        text_rect = text.get_rect()
        text_rect.x = 15
        text_rect.y = 340
        self.screen.blit(text, text_rect)

        text = pygame.font.SysFont("avenir", 14).render('Search Depth:' , True, self.white)
        text_rect = text.get_rect()
        text_rect.x = 15
        text_rect.y = 360
        self.screen.blit(text, text_rect)
        text = pygame.font.SysFont("avenir", 12, True).render(str(config['max_depth']), True, self.white)
        text_rect = text.get_rect()
        text_rect.x = 15
        text_rect.y = 380
        self.screen.blit(text, text_rect)

        text = pygame.font.SysFont("avenir", 14).render("Node Value Heuristic:", True, self.white)
        text_rect = text.get_rect()
        text_rect.x = 15
        text_rect.y = 400
        self.screen.blit(text, text_rect)
        text = pygame.font.SysFont("avenir", 12, True).render(config['AI1_node_value_heuristic'].__class__.__name__, True, self.white)
        text_rect = text.get_rect()
        text_rect.x = 15
        text_rect.y = 418
        self.screen.blit(text, text_rect)

        text = pygame.font.SysFont("avenir", 14).render("Node Ordering Heuristic:" , True, self.white)
        text_rect = text.get_rect()
        text_rect.x = 15
        text_rect.y = 440
        self.screen.blit(text, text_rect)
        text = pygame.font.SysFont("avenir", 12, True).render(config['AI1_node_ordering_heuristic'].__class__.__name__, True, self.white)
        text_rect = text.get_rect()
        text_rect.x = 15
        text_rect.y = 458
        self.screen.blit(text, text_rect)

        text = pygame.font.SysFont("avenir", 22, bold=True).render("J(B, R) = " + str(round(J, 4)), True, self.white)
        text_rect = text.get_rect()
        text_rect.center = (115, 505)
        self.screen.blit(text, text_rect)
        text = pygame.font.SysFont("avenir", 12).render("[B maximizes, R minimizes]", True, self.white)
        text_rect = text.get_rect()
        text_rect.center = (115, 528)
        self.screen.blit(text, text_rect)

        gfxdraw.filled_polygon(self.screen, [(300, 500), (700, 500), (700, 550),(300, 550)], self.white)

        text = pygame.font.SysFont("avenir", 12).render('Last move took ' + str(move_lasted) + 's', True, self.black, self.white)
        text_rect = text.get_rect()
        text_rect.center = (250, 20)
        self.screen.blit(text, text_rect)

        if not winner:
            text = pygame.font.SysFont("avenir", 25, bold=True).render("It's        turn!", True, self.black, self.white)
            text_rect = text.get_rect()
            text_rect.center = (510, 517)
            self.screen.blit(text, text_rect)
            if not config['AI_vs_AI']:
                text = pygame.font.SysFont("avenir", 25).render('[AI]' if player_turn == self.BLUE_PLAYER else '[YOU]', True, self.black, self.white)
            else:
                text = pygame.font.SysFont("avenir", 25).render('[AI1]' if player_turn == self.BLUE_PLAYER else '[AI2]', True, self.black, self.white)
            text_rect = text.get_rect()
            text_rect.x = 595
            text_rect.y = 500
            self.screen.blit(text, text_rect)
            x = 502
            y = 516
            gfxdraw.filled_polygon(self.screen,
                                   [(x + 15 * cos(radians(90) + 2 * pi * _ / 6),
                                     y + 15 * sin(radians(90) + 2 * pi * _ / 6))
                                    for _ in range(6)],
                                   self.red if player_turn == self.RED_PLAYER else self.blue)
        else:
            text = pygame.font.SysFont("avenir", 25, bold=True).render("The winner is", True, self.black,
                                                                       self.white)
            text_rect = text.get_rect()
            text_rect.center = (470, 517)
            self.screen.blit(text, text_rect)
            if not config['AI_vs_AI']:
                text = pygame.font.SysFont("avenir", 25).render('[AI]' if winner == self.BLUE_PLAYER else '[YOU]',
                                                                True, self.black, self.white)
            else:
                text = pygame.font.SysFont("avenir", 25).render('[AI1]' if winner == self.BLUE_PLAYER else '[AI2]',
                                                                True, self.black, self.white)
            text_rect = text.get_rect()
            text_rect.x = 595
            text_rect.y = 500
            self.screen.blit(text, text_rect)
            x = 570
            y = 516
            gfxdraw.filled_polygon(self.screen,
                                   [(x + 15 * cos(radians(90) + 2 * pi * _ / 6),
                                     y + 15 * sin(radians(90) + 2 * pi * _ / 6))
                                    for _ in range(6)],
                                   self.red if winner == self.RED_PLAYER else self.blue)

    def draw_stats_right(self, config, J, player_turn):
        x_offset = 600
        y_offset = - 230

        text = pygame.font.SysFont("avenir", 22, bold=True).render("J(B, R) = " + str(round(J, 4)), True, self.white)
        text_rect = text.get_rect()
        text_rect.center = (80 + x_offset, 260 + y_offset)
        self.screen.blit(text, text_rect)
        text = pygame.font.SysFont("avenir", 12).render("[B maximizes, R minimizes]", True, self.white)
        text_rect = text.get_rect()
        text_rect.center = (80 + x_offset, 283 + y_offset)
        self.screen.blit(text, text_rect)

        text = pygame.font.SysFont("avenir", 14).render('Node Ordering Heuristic:', True, self.white)
        text_rect = text.get_rect()
        text_rect.topright = (195 + x_offset, 320 + y_offset)
        self.screen.blit(text, text_rect)
        text = pygame.font.SysFont("avenir", 12, True).render(config['AI2_node_ordering_heuristic'].__class__.__name__, True, self.white)
        text_rect = text.get_rect()
        text_rect.topright = (195 + x_offset, 340 + y_offset)
        self.screen.blit(text, text_rect)

        text = pygame.font.SysFont("avenir", 14).render('Node Value Heuristic:', True, self.white)
        text_rect = text.get_rect()
        text_rect.topright = (195 + x_offset, 360 + y_offset)
        self.screen.blit(text, text_rect)
        text = pygame.font.SysFont("avenir", 12, True).render(config['AI2_node_value_heuristic'].__class__.__name__, True, self.white)
        text_rect = text.get_rect()
        text_rect.topright = (195 + x_offset, 380 + y_offset)
        self.screen.blit(text, text_rect)

        text = pygame.font.SysFont("avenir", 14).render("Search Depth:", True, self.white)
        text_rect = text.get_rect()
        text_rect.topright = (195 + x_offset, 400 + y_offset)
        self.screen.blit(text, text_rect)
        text = pygame.font.SysFont("avenir", 12, True).render(str(config['max_depth']), True, self.white)
        text_rect = text.get_rect()
        text_rect.topright = (195 + x_offset, 418 + y_offset)
        self.screen.blit(text, text_rect)

        text = pygame.font.SysFont("avenir", 14).render("Algorithm:" , True, self.white)
        text_rect = text.get_rect()
        text_rect.topright = (195 + x_offset, 440 + y_offset)
        self.screen.blit(text, text_rect)
        text = pygame.font.SysFont("avenir", 12, True).render('a-b pruning', True, self.white)
        text_rect = text.get_rect()
        text_rect.topright = (195 + x_offset, 458 + y_offset)
        self.screen.blit(text, text_rect)

        text = pygame.font.SysFont("avenir", 30, bold=True).render('AI', True, self.white)
        text_rect = text.get_rect()
        text_rect.topright = (190 + x_offset, 510 + y_offset)
        self.screen.blit(text, text_rect)
        text = pygame.font.SysFont("avenir", 18).render('Player' , True, self.white)
        text_rect = text.get_rect()
        text_rect.topright = (190 + x_offset, 542 + y_offset)
        self.screen.blit(text, text_rect)

    def draw_user_stats(self):
        x_offset = 600
        y_offset = - 230

        # title
        text = pygame.font.SysFont("avenir", 50, bold=True).render("HexAI", True, self.white)
        text_rect = text.get_rect()
        text_rect.center = (680, 40)
        self.screen.blit(text, text_rect)

        text = pygame.font.SysFont("avenir", 15, bold=True).render("by Luigi Schiavone", True, self.white)
        text_rect = text.get_rect()
        text_rect.center = (683, 70)
        self.screen.blit(text, text_rect)
        text = pygame.font.SysFont("avenir", 10, bold=True).render("AGIG course 22/23 UniSa", True, self.white)
        text_rect = text.get_rect()
        text_rect.center = (682, 87)
        self.screen.blit(text, text_rect)

        text = pygame.font.SysFont("avenir", 30, bold=True).render('You', True, self.white)
        text_rect = text.get_rect()
        text_rect.topright = (190 + x_offset, 510 + y_offset)
        self.screen.blit(text, text_rect)
        text = pygame.font.SysFont("avenir", 18).render('Player', True, self.white)
        text_rect = text.get_rect()
        text_rect.topright = (190 + x_offset, 542 + y_offset)
        self.screen.blit(text, text_rect)
