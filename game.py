import random

import pygame


class Game:
    def __init__(self, is_agent_playing=True, box_size=50):
        self.is_agent_playing = is_agent_playing
        self.box_size = box_size

        self.num_rows = 20
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
                [(1, -1), (1, 0), (1, 1), (0, 1)],
            ],
            [
                [(0, 0), (1, 0), (2, 0), (2, -1)],
                [(1, 0), (1, -1), (1, 1), (0, -1)],
                [(0, 0), (1, 0), (2, 0), (0, 1)],
                [(1, 0), (1, -1), (1, 1), (2, 1)],
            ],
            [
                [(0, 0), (1, 0), (2, 0), (1, 1)],
                [(2, 0), (1, 0), (1, -1), (1, 1)],
                [(0, 0), (1, 0), (2, 0), (1, -1)],
                [(0, 0), (1, 0), (1, -1), (1, 1)],
            ],
            [
                [(0, 0), (1, 0), (0, 1), (1, 1)]
            ],
            [
                [(0, 0), (1, 0), (2, 0), (3, 0)],
                [(1, -1), (1, 0), (1, 1), (1, 2)],
                [(0, 0), (1, 0), (2, 0), (-1, 0)],
                [(1, -1), (1, 0), (1, 1), (1, -2)],
            ],
            [
                [(1, 0), (2, 0), (0, 1), (1, 1)],
                [(1, 0), (0, 0), (0, -1), (1, 1)],
            ],
            [
                [(0, 0), (1, 0), (1, 1), (2, 1)],
                [(0, 0), (1, 0), (0, 1), (1, -1)]
            ],
        ]

        self.action_space = [
            self.no_action,
            self.rotate_c,
            self.rotate_cc,
            self.move_right,
            self.move_left,
            self.soft_drop,
            self.hard_drop,
        ]

    def init_grid(self):
        self.grid = []
        for _ in range(self.num_columns):
            self.grid.append([None] * self.num_rows)

    def init_piece(self):
        self.piece_index = random.randint(0, len(self.pieces) - 1)
        self.piece_rotation_index = 0
        self.piece = self.pieces[self.piece_index][self.piece_rotation_index]
        self.piece_x = self.num_columns // 2
        self.piece_y = 0

    def reset(self):
        self.init_grid()
        self.piece = None

    def no_action(self):
        pass

    def rotate_c(self):
        self.piece_rotation_index += 1
        self.piece_rotation_index %= len(self.pieces[self.piece_index])
        self.piece = self.pieces[self.piece_index][self.piece_rotation_index]

    def rotate_cc(self):
        self.piece_rotation_index -= 1
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
        self.piece_y -= 1
        self.set_piece()

    def collision(self):
        for x, y in self.piece:
            absolute_x = self.piece_x + x
            absolute_y = self.piece_y + y
            if (
                absolute_x < 0
                or absolute_x >= self.num_rows
                or absolute_y >= self.num_columns
                or self.grid[absolute_x][absolute_y] == 1
            ):
                return True
        return False

    def set_piece(self):
        for x, y in self.piece:
            absolute_x = self.piece_x + x
            absolute_y = self.piece_y + y
            self.grid[absolute_x][absolute_y] = 1
        self.piece = None

    def print_game(self):
        print("\n[------TETRIS------]")
        for y in range(self.num_rows):
            row_output = ""
            for x in range(self.num_columns):
                relative_x = x - self.piece_x
                relative_y = y - self.piece_y
                if (relative_x, relative_y) in self.piece:
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

    def play_step(self, action):
        if not self.piece:
            self.init_piece()

        self.piece_y += 1
        if self.collision():
            self.piece_y -= 1
            self.set_piece()

        self.action_space[action]()


# if __name__ == "__main__":
#     g = Game()
#     g.reset()
#     g.play_step(0)
#     g.play_step(0)
#     g.play_step(0)
#     g.move_right()
#     g.print_game()
#     g.rotate_c()
#     g.print_game()
#     g.rotate_cc()
#     g.print_game()
