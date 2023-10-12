import random

import numpy as np
import pygame
import torch
# from copy import deepcopy


class Game:
    def __init__(self, is_agent_playing=True, box_size=50):
        self.is_agent_playing = is_agent_playing
        self.box_size = box_size

        self.num_rows = 16
        self.num_columns = 10

        if not self.is_agent_playing:
            pygame.init()
            self.display = pygame.display.set_mode(
                (self.num_rows * self.box_size,
                 self.num_columns * self.box_size)
            )

        self.piece = None
        self.pieces = [
            [
                [(0, 0), (1, 0), (2, 0), (2, 1)],
                [(1, -1), (1, 0), (1, 1), (2, -1)],
                [(0, 0), (1, 0), (2, 0), (0, -1)],
                [(1, -1), (1, 0), (1, 1), (0, 1)]
            ],
            [
                [(0, 0), (1, 0), (2, 0), (2, -1)],
                [(1, 0), (1, -1), (1, 1), (0, -1)],
                [(0, 0), (1, 0), (2, 0), (0, 1)],
                [(1, 0), (1, -1), (1, 1), (2, 1)]
            ],
            [
                [(0, 0), (1, 0), (2, 0), (1, 1)],
                [(2, 0), (1, 0), (1, -1), (1, 1)],
                [(0, 0), (1, 0), (2, 0), (1, -1)],
                [(0, 0), (1, 0), (1, -1), (1, 1)]
            ],
            [
                [(0, 0), (1, 0), (0, 1), (1, 1)]
            ],
            [
                [(0, 0), (1, 0), (2, 0), (3, 0)],
                [(1, -1), (1, 0), (1, 1), (1, 2)],
                [(0, 0), (1, 0), (2, 0), (-1, 0)],
                [(1, -1), (1, 0), (1, 1), (1, -2)]
            ],
            [
                [(1, 0), (2, 0), (0, 1), (1, 1)],
                [(1, 0), (0, 0), (0, -1), (1, 1)]
            ],
            [
                [(0, 0), (1, 0), (1, 1), (2, 1)],
                [(0, 0), (1, 0), (0, 1), (1, -1)]
            ] 
        ]

        self.score = 0
        self.points = -8

        self.action_space = [
            self.no_action,
            self.rotate_c,
            self.rotate_cc,
            self.move_right,
            self.move_left,
            self.soft_drop,
            self.hard_drop,
        ]

        self.reset()

    def init_grid(self):
        self.grid = []
        for _ in range(self.num_columns):
            self.grid.append([0] * self.num_rows)

    def init_piece(self):
        self.piece_index = random.randint(0, len(self.pieces) - 1)
        self.piece_rotation_index = 0
        self.piece = self.pieces[self.piece_index][self.piece_rotation_index]
        min_x, max_x = self.piece_width(self.piece)
        self.piece_x = random.randint(
            1 if min_x < 0 else 0,
            self.num_columns - 1 - max_x
        )
        self.piece_y = 0
        self.points = -8

    def piece_width(self, piece):
        min_x = 5
        max_x = -5
        for x, _ in piece:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
        return min_x, max_x

    def reset(self):
        self.init_grid()
        self.init_piece()
        self.score = 0
        self.points = -8

    def no_action(self):
        pass

    def rotate_c(self):
        self.piece_rotation_index += 1
        self.piece_rotation_index %= len(self.pieces[self.piece_index])
        self.piece = self.pieces[self.piece_index][self.piece_rotation_index]
        if self.collision():
            self.piece_rotation_index -= 1
            self.piece_rotation_index %= len(self.pieces[self.piece_index])
            self.piece = self.pieces[self.piece_index][self.piece_rotation_index]

    def rotate_cc(self):
        self.piece_rotation_index -= 1
        self.piece_rotation_index %= len(self.pieces[self.piece_index])
        self.piece = self.pieces[self.piece_index][self.piece_rotation_index]
        if self.collision():
            self.piece_rotation_index += 1
            self.piece_rotation_index %= len(self.pieces[self.piece_index])
            self.piece = self.pieces[self.piece_index][self.piece_rotation_index]

    def move_right(self):
        self.piece_x += 1
        if self.collision():
            self.piece_x -= 1

    def move_left(self):
        self.piece_x -= 1
        if self.collision():
            self.piece_x += 1

    def soft_drop(self):
        self.piece_y += 1
        if self.collision():
            self.piece_y -= 1

    def hard_drop(self):
        while not self.collision():
            self.piece_y += 1
            self.points += 1
        self.piece_y -= 1

    def collision(self):
        if self.piece:
            for x, y in self.piece:
                absolute_x = self.piece_x + x
                absolute_y = self.piece_y + y
                if (
                    absolute_x < 0
                    or absolute_x >= self.num_columns
                    or absolute_y >= self.num_rows
                    or self.grid[absolute_x][absolute_y] == 1
                ):
                    return True
        return False

    def piece_collision(self):
        for x, y in self.piece:
            absolute_x = self.piece_x + x
            absolute_y = self.piece_y + y
            if absolute_x > 0 and absolute_y > 0:
                if self.grid[absolute_x][absolute_y] == 1:
                    return True
        return False

    def set_piece(self):
        for x, y in self.piece:
            absolute_x = self.piece_x + x
            absolute_y = self.piece_y + y
            self.grid[absolute_x][absolute_y] = 1
        self.init_piece()

    def print_game(self):
        print("\n[------TETRIS------]")
        for y in range(self.num_rows):
            row_output = ""
            for x in range(self.num_columns):
                relative_x = x - self.piece_x
                relative_y = y - self.piece_y
                if self.piece and ((relative_x, relative_y) in self.piece):
                    row_output += "o "
                else:
                    row_output += "x " if self.grid[x][y] else ". "
            print(row_output)

    def print_pieces(self):
        for piece in self.pieces:
            print('-' * 10)
            for rotation in piece:
                print('-' * 5)
                for x in range(-5, 5):
                    row_output = ""
                    for y in range(-5, 5):
                        if (x, y) in rotation:
                            row_output += "o "
                        else:
                            row_output += ". "
                    print(row_output)
            print('-' * 10)

    def grid_to_image(self):
        image = torch.from_numpy(np.array(self.grid)).float()
        for x, y in self.piece:
            absolute_x, absolute_y = self.piece_x+x, self.piece_y+y
            image[absolute_x, absolute_y] = 0.5
        image = image[None][None]
        return image

    def transpose_grid(self, grid):
        grid_t = list(zip(*grid))
        return [list(row) for row in grid_t]

    def break_rows(self):
        grid_t = self.transpose_grid(self.grid)
        broken = False
        for row in grid_t:
            if all(row):
                broken = True
                self.score += 1
                self.points += 100
                grid_t.remove(row)
                grid_t.insert(0, [0] * self.num_columns)

        if broken:
            self.grid = self.transpose_grid(grid_t)

    def play_step(self, action):
        game_over = False

        if self.piece_y == 0 and self.piece_collision():
            return self.points, True, self.score

        self.action_space[action]()

        self.points += 1
        self.piece_y += 1

        if self.collision():
            self.piece_y -= 1
            self.set_piece()
            self.break_rows()

        self.print_game()

        return self.points, game_over, self.score


if __name__ == "__main__":
    g = Game()
