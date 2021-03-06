import board
import pygame
import random
import tensorflow as tf
import numpy as np

"""
Options

0: board size
1: legal moves for each piece
2: squaresize
"""


class Game:
    def __init__(self, options):
        self.board = board.Board(*options)
        self.size = options[0]
        self.legalmoves = options[1]
        self.squaresize = options[2]
        self.player = 0
        self.held = 0
        self.possible_moves = []

    def start(self, surface, p1="player", p2="computer"):
        self.board.reset()
        self.player = 0
        self.held = 0
        images = load_shapes(self.squaresize)
        playing = 1
        self.possible_moves = self.board.get_possible_moves(self.player)
        green_square = pygame.Surface((self.squaresize, self.squaresize))
        green_square.fill((0, 255, 0))
        green_square.set_alpha(128)
        while playing:
            self.board.draw(surface, images)
            if self.held:
                x, y = pygame.mouse.get_pos()
                x = x // self.squaresize
                y = y // self.squaresize
                surface.blit(images[int(self.held[0][1] + (self.held[0][0] - 1) * 7)],
                             (x * self.squaresize, y * self.squaresize))
                for move in self.possible_moves:
                    if move[0][0] == self.held[1][0] and move[0][1] == self.held[1][1]:
                        surface.blit(green_square, (move[1][0]*self.squaresize, move[1][1]*self.squaresize))
            events = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return -1, 0
                else:
                    events.append(event)
            if self.player:
                self.handle_turn(events, p1)
            else:
                self.handle_turn(events, p2)
            if self.board.ended():
                return int(not self.player), 1
            pygame.display.flip()

    def handle_turn(self, events, player):
        if player == "player":
            self.user_handle(events)
        else:
            self.ai_handle()

    def user_handle(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    x = x // self.squaresize
                    y = y // self.squaresize
                    piece = self.board.get_piece_at(x, y)
                    if piece[0] == self.player + 1:
                        self.held = piece, (x, y)
            if event.type == pygame.MOUSEBUTTONUP and self.held and event.button == 1:
                x, y = pygame.mouse.get_pos()
                x = x // self.squaresize
                y = y // self.squaresize
                if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
                    if self.board.place(self.held[1], (x, y), self.player):
                        self.turn_change()
                self.held = 0

    def ai_handle(self):
        """Not currently useful"""
        not_placed = True
        while not_placed:
            x1, y1 = random.randrange(self.size[0]), random.randrange(self.size[1])
            x2, y2 = random.randrange(self.size[0]), random.randrange(self.size[1])
            if self.board.place((x1, y1), (x2, y2), self.player):
                not_placed = True
                self.turn_change()

    def turn_change(self):
        self.player = not self.player
        self.possible_moves = self.board.get_possible_moves(self.player)


shapes_designs = [
    [0, [[[0, 0], [1, 1]], [[1, 0], [0, 1]]]],
    [0, [[[0.5, 0], [1, 0.75], [0, 0.75], [0.5, 0]]]],
    [1, [0.5, 0.5, 0.5]],
    [0, [[[0.5, 0], [0.5, 1]], [[0, 0.5], [1, 0.5]]]],
    [0, [[[0.5, 0], [1, 0.5], [0.5, 1], [0, 0.5], [0.5, 0]]]],
    [0, [[[0.5, 0], [0.5, 1]], [[0, 0.5], [1, 0.5]], [[0, 0], [1, 1]], [[1, 0], [0, 1]]]],
    [0, [[[0.25, 0], [0.25, 1]], [[0.75, 0], [0.75, 1]], [[0, 0.25], [1, 0.25]], [[0, 0.75], [1, 0.75]]]]
]


def load_shapes(squaresize):
    shapes = [pygame.Surface((squaresize, squaresize), pygame.SRCALPHA, 32).convert_alpha() for _ in range(14)]
    for i, shape in enumerate(shapes_designs):
        if shapes_designs[i][0]:
            circle = shapes_designs[i][1]
            pygame.draw.circle(shapes[i], (0, 0, 0), (int(circle[0] * squaresize), int(circle[1] * squaresize)),
                               int(circle[2] * squaresize))
        else:
            for lines in shapes_designs[i][1]:
                pygame.draw.lines(shapes[i], (0, 0, 0), 0,
                                  [[int(d * squaresize) for d in point] for point in lines], int(squaresize / 16))
    for i, shape in enumerate(shapes_designs):
        if shapes_designs[i][0]:
            circle = shapes_designs[i][1]
            pygame.draw.circle(shapes[i + 7], (255, 0, 0), (int(circle[0] * squaresize), int(circle[1] * squaresize)),
                               int(circle[2] * squaresize))
        else:
            for lines in shapes_designs[i][1]:
                pygame.draw.lines(shapes[i + 7], (255, 0, 0), 0,
                                  [[int(d * squaresize) for d in point] for point in lines], int(squaresize / 16))
    return shapes
