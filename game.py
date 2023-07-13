import random

import pygame

FIGURE_COLORS = [
    None,
    pygame.Color("#44ffff"),
    pygame.Color("#ff4444"),
    pygame.Color("#44ff44"),
    pygame.Color("#4444ff"),
    pygame.Color("#8244ff"),
    pygame.Color("#ffff44"),
    pygame.Color("#ff44ff"),
]


class Figure:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.figures = [
            None,
            [[1, 5, 9, 13], [4, 5, 6, 7]],
            [[4, 5, 9, 10], [2, 6, 5, 9]],
            [[6, 7, 9, 10], [1, 5, 6, 10]],
            [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
            [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
            [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
            [[1, 2, 5, 6]],
        ]
        self.type = random.randint(1, len(self.figures) - 1)
        self.color = FIGURE_COLORS[self.type]
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Game:
    def __init__(
            self,
            agent_playing,
            update_ui,
            control_fps,
            height=20,
            width=10,
            box_size=20
    ):
        pygame.init()
        self.display = pygame.display.set_mode(
            (width*box_size, height*box_size)
        )
        self.width, self.height = width, height
        self.box_size = box_size

        self.bg_color = (50, 50, 50)
        self.line_color = (0, 0, 0)
        self.counter = 0
        self.clock = pygame.time.Clock()
        self.fps = 25
        self.agent_playing = agent_playing
        self.update_ui = update_ui
        self.control_fps = control_fps
        self.actions = [
            self.rotate,
            self.down,
            self.left,
            self.right,
            self.drop
        ]

    def reset(self):
        self.state = "start"
        self.figure = None
        self.level = 2
        self.score = 0
        self.last_score = 0
        self.grid = []

        for _ in range(self.height):
            new_line = []
            for _ in range(self.width):
                new_line.append(None)
            self.grid.append(new_line)

    def play(self):
        while True:
            self.play_step(action=None)

    def play_step(self, action):
        if self.figure is None:
            self.new_figure()

        self.counter += 1
        if self.counter > 100000:
            self.counter = 0

        if self.counter % (self.fps // self.level // 2) == 0:
            if self.state == "start":
                self.down()

        if self.agent_playing:
            self.take_action(action)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.rotate()
                    if event.key == pygame.K_DOWN:
                        self.down()
                    if event.key == pygame.K_LEFT:
                        self.left(-1)
                    if event.key == pygame.K_RIGHT:
                        self.right(1)
                    if event.key == pygame.K_SPACE:
                        self.drop()
                    if event.key == pygame.K_ESCAPE:
                        self.__init__(self.width, self.height)

        if self.update_ui:
            self.display.fill(self.bg_color)

            for i in range(self.height):
                for j in range(self.width):
                    pygame.draw.rect(
                        self.display,
                        self.line_color,
                        [
                            self.box_size * j,
                            self.box_size * i,
                            self.box_size,
                            self.box_size
                        ],
                        1
                    )
                    if self.grid[i][j]:
                        pygame.draw.rect(
                            self.display,
                            FIGURE_COLORS[self.grid[i][j]],
                            [
                                self.box_size * j + 1,
                                self.box_size * i + 1,
                                self.box_size - 2,
                                self.box_size - 1
                            ]
                        )

            if self.figure is not None:
                for i in range(4):
                    for j in range(4):
                        p = i * 4 + j
                        if p in self.figure.image():
                            pygame.draw.rect(
                                self.display,
                                self.figure.color,
                                [
                                    self.box_size * (j + self.figure.x) + 1,
                                    self.box_size * (i + self.figure.y) + 1,
                                    self.box_size - 2,
                                    self.box_size - 2
                                ]
                            )

            pygame.display.flip()

        if self.control_fps:
            self.clock.tick(self.fps)

        reward = self.score - self.last_score
        if self.state == "gameover":
            reward = -50
        self.last_score = self.score
        return reward, self.state, self.score

    def get_observation(self):
        return [
            self.grid,
            self.figure,
        ]

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
                            self.grid[i+self.figure.y][j+self.figure.x]:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            nones = 0
            for j in range(self.width):
                if not self.grid[i][j]:
                    nones += 1
            if nones == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.grid[i1][j] = self.grid[i1 - 1][j]
        self.score += lines ** 2

    def take_action(self, action):
        for a, act in zip(action, self.actions):
            if a:
                act()

    def drop(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.grid[i + self.figure.y][j + self.figure.x] = \
                        FIGURE_COLORS.index(self.figure.color)
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def left(self):
        old_x = self.figure.x
        self.figure.x -= 1
        if self.intersects():
            self.figure.x = old_x

    def right(self):
        old_x = self.figure.x
        self.figure.x += 1
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


if __name__ == '__main__':
    g = Game(agent_playing=False)
