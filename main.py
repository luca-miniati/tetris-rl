import pygame
import random

class Figure:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.figures = [
            [[1, 5, 9, 13], [4, 5, 6, 7]],
            [[4, 5, 9, 10], [2, 6, 5, 9]],
            [[6, 7, 9, 10], [1, 5, 6, 10]],
            [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
            [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
            [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
            [[1, 2, 5, 6]],
        ]
        self.type = random.randint(0, len(self.figures) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Game:
    def __init__(self, height=20, width=10, box_size=20):
        pygame.init()
        self.display = pygame.display.set_mode((width*box_size, height*box_size))
        self.width, self.height = width, height
        self.box_size = box_size
        
        self.bg_color = (50, 50, 50)
        self.line_color = (0, 0, 0)
        self.clock = pygame.time.Clock()
        self.fps = 25
        
    def reset(self):
        self.state = "start"
        self.figure = None
        self.level = 2
        self.score = 0
        self.grid = []

        for _ in range(self.height):
            new_line = []
            for _ in range(self.width):
                new_line.append(0)
            self.grid.append(new_line)
        
        self.play()

    def play(self):
        game_over = False
        counter = 0

        down = False

        while not game_over:
            if self.figure is None:
                self.new_figure()
            counter += 1
            if counter > 100000:
                counter = 0

            if counter % (self.fps // self.level // 2) == 0 or down:
                if self.state == "start":
                    self.go_down()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.rotate()
                    if event.key == pygame.K_DOWN:
                        down = True
                    if event.key == pygame.K_LEFT:
                        self.go_side(-1)
                    if event.key == pygame.K_RIGHT:
                        self.go_side(1)
                    if event.key == pygame.K_SPACE:
                        self.go_space()
                    if event.key == pygame.K_ESCAPE:
                        self.__init__(self.width, self.height)

            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        down = False

            self.display.fill(self.bg_color)

            for i in range(self.height):
                for j in range(self.width):
                    pygame.draw.rect(self.display, self.line_color, [self.box_size * j, self.box_size * i, self.box_size, self.box_size], 1)
                    if self.grid[i][j] > 0:
                        pygame.draw.rect(self.display, (235, 235, 235),
                                        [self.box_size * j + 1, self.box_size * i + 1, self.box_size - 2, self.box_size - 1])

            if self.figure is not None:
                for i in range(4):
                    for j in range(4):
                        p = i * 4 + j
                        if p in self.figure.image():
                            pygame.draw.rect(self.display, (235, 235, 235),
                                            [self.box_size * (j + self.figure.x) + 1,
                                            self.box_size * (i + self.figure.y) + 1,
                                            self.box_size - 2, self.box_size - 2])
                            
            if self.state == 'gameover':
                self.reset()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.grid[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.grid[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.grid[i1][j] = self.grid[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.grid[i + self.figure.y][j + self.figure.x] = 1
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

if __name__ == '__main__':
    g = Game()
    g.reset()