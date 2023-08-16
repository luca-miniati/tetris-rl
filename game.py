import random
import pygame


class Game:
    def __init__(self, is_agent_playing, box_size=50):
        self.is_agent_playing = is_agent_playing
        self.box_size = box_size

        self.num_rows = 10
        self.num_columns = 20

        if not self.is_agent_playing:
            self.display = pygame.display.set_mode(
                (self.num_rows * self.box_size,
                 self.num_columns * self.box_size)
            )

        self.piece = None
        self.pieces = [
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 0), (1, 0), (2, 0), (2, 1)],
            [(0, 0), (1, 0), (2, 0), (2, -1)],
            [(0, 0), (1, 0), (2, 0), (1, 1)],
            [(0, 0), (1, 0), (0, 1), (1, 1)],
            [(1, 0), (2, 0), (0, 1), (1, 1)],
            [(0, 0), (1, 0), (1, 1), (2, 1)],
        ]

        self.pivots = [
            (1, 0),
            (1, 0),
            (1, 0),
            (1, 0),
            (0, 0),
            (1, 1),
            (1, 1),
        ]

        self.action_space = [
            self.rotate_c,
            self.rotate_cc,
            self.move_right,
            self.move_left,
            self.soft_drop,
            self.hard_drop
        ]

    def init_grid(self):
        self.grid = []
        for _ in range(self.num_columns):
            self.grid.append([None] * self.num_rows)

    def init_piece(self):
        self.piece = self.pieces[random.randint(0, len(self.pieces) - 1)]

    def reset(self):
        self.init_grid()
        self.piece = None

    def rotate_c(self):


    def play_step(self, action):
        if not self.piece:
            self.init_piece()

        self.piece = [(x, y + 1) for x, y in self.piece]

        if action:
            self.action_space[action]()
