from game import Game
import time


def test_game_break_row():
    g = Game()
    grid = g.transpose_grid(g.grid)
    grid[-1] = [1, 1, 1, 1, 0, 1, 1, 1, 1, 1]
    g.grid = g.transpose_grid(grid)

    g.piece = g.pieces[0][0]
    g.piece_x = 2
    g.piece_y = 13

    g.print_game()

    points, game_over, score = g.play_step(0)
    print(points, game_over, score)

    g.print_game()


def test_game_over():
    g = Game()
    grid = g.transpose_grid(g.grid)
    grid[2] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    g.grid = g.transpose_grid(grid)

    g.piece = g.pieces[0][0]
    g.piece_x = 2
    g.piece_y = 0

    g.print_game()

    points, game_over, score = g.play_step(0)
    print(points, game_over, score)

    g.print_game()


def test_game_earn_points():
    g = Game()
    grid = g.transpose_grid(g.grid)
    grid[-1] = [1, 1, 1, 1, 0, 1, 1, 1, 1, 1]
    g.grid = g.transpose_grid(grid)

    g.piece = g.pieces[0][0]
    g.piece_x = 2
    g.piece_y = 6

    g.print_game()

    while True:
        points, game_over, score = g.play_step(0)
        time.sleep(0.1)


test_game_earn_points()

# todo: test_hard_drop
