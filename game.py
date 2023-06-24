import pygame
from piece import *

class Game:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.display = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.blocks = []
        self.bg_color = (46, 46, 46)
        self.border_color = (125, 125, 125)
        self.line_color = (0, 0, 0)
        self.line_width = 2
        self.piece_colors = {
            'i': (128, 255, 244),
            'j': (77, 91, 255),
            'l': (245, 165, 86),
            'o': (232, 235, 87),
            's': (85, 242, 124),
            't': (199, 110, 255),
            'z': (250, 87, 90)
        }
        self.piece_types = list(self.piece_colors.keys())
        self.box_size = self.width // 10
        self.grid = [[0] * 20 for _ in range(10)]
        
        self.falling_pieces = []
        self.set_pieces = []
        self.piece_fall_delay = 10
        self.piece_fall_counter = 0

        self.right = False
        self.left = False

    def draw(self):
        self.display.fill(self.bg_color)

        for piece in self.falling_pieces + self.set_pieces:
            for x in range(len(piece.grid)):
                for y in range(len(piece.grid)):
                    if piece.grid[x][y]:
                        pygame.draw.rect(self.display, self.piece_colors[piece.type], pygame.Rect((piece.x+x)*self.box_size, (piece.y+y)*self.box_size, self.box_size, self.box_size))

        for x in range(1, 10):
            pygame.draw.line(self.display, self.line_color, (x*self.box_size, 0), (x*self.box_size, self.height), self.line_width)
        for y in range(1, 20):
            pygame.draw.line(self.display, self.line_color, (0, y*self.box_size), (self.width, y*self.box_size), self.line_width)

        pygame.display.flip()

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT or e.key == pygame.K_a:
                    self.left = True
                if e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                    self.right = True
                if e.key == pygame.K_SPACE:
                    while not self.falling_pieces[0].is_at_bottom(self.grid):
                        self.falling_pieces[0].y += 1
                    self.set_piece(self.falling_pieces[0])
                    self.set_pieces.append(self.falling_pieces.pop(0))
                if e.key == pygame.K_UP or e.key == pygame.K_w:
                    self.falling_pieces[0].grid = list(reversed(list(zip(*self.falling_pieces[0].grid))))
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT or e.key == pygame.K_a:
                    self.left = False
                if e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                    self.right = False

    def set_piece(self, piece):
        for x in range(len(piece.grid)):
            for y in range(len(piece.grid)):
                if piece.grid[x][y]:
                    self.grid[piece.x + x][piece.y + y] = 1

    def update(self):
        grid_t = list(zip(*self.grid))
        for i, row in enumerate(grid_t):
            if 0 not in row:
                grid_t.pop(i)

        if self.right:
            if self.falling_pieces[0].get_right_edge() < 10:
                    if self.falling_pieces[0].can_move_right(self.grid):
                        self.falling_pieces[0].x += 1
        if self.left:
            if self.falling_pieces[0].get_left_edge() > 0:
                        if self.falling_pieces[0].can_move_left(self.grid):
                            self.falling_pieces[0].x -= 1

        if not len(self.falling_pieces):
            self.falling_pieces.append(Piece(random.choice(self.piece_types), self.box_size))

        self.piece_fall_counter += 1
        if self.piece_fall_counter >= self.piece_fall_delay:
            for piece in self.falling_pieces:
                if piece.is_at_bottom(self.grid):
                    self.falling_pieces.remove(piece)
                    self.set_pieces.append(piece)
                    self.set_piece(piece)
                else:
                    piece.y += 1
            self.piece_fall_counter = 0

    def play(self):
        game_over = False

        while not game_over:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(30)

if __name__ == '__main__':
    g = Game(40*10, 40*20)
    g.play()