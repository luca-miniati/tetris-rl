import random

PIECE_SHAPES = {
    'i': [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ],
    'j': [
        [0, 1, 0],
        [0, 1, 0],
        [1, 1, 0]
    ],
    'l': [
        [1, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ],
    'o': [
        [1, 1],
        [1, 1]
    ],
    's': [
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0]
    ],
    't': [
        [0, 1, 0],
        [1, 1, 0],
        [0, 1, 0]
    ],
    'z': [
        [0, 1, 0],
        [1, 1, 0],
        [1, 0, 0]
    ]
}

class Piece:
    def __init__(self, type, box_size):
        # i, j, l, o, s, t, z
        self.type = type
        self.box_size = box_size
        self.grid = PIECE_SHAPES[self.type]
        self.x = random.randint(0, 10-len(self.grid[0]))
        self.y = -1

    def is_at_bottom(self, grid):
        for i_y, row in enumerate(zip(*self.grid)):
            for i_x, sq in enumerate(row):
                if sq:
                    if self.y+i_y == 19:
                        return True
                    elif grid[self.x+i_x][self.y+i_y+1]:
                        return True
        return False
    
    def get_left_edge(self):
        for i, (col) in enumerate(self.grid):
            if 1 in col:
                return self.x + i
            
    def get_right_edge(self):
        for col in reversed(self.grid):
            if 1 in col:
                return self.x + self.get_width()
            
    def get_width(self):
        return sum([1 if 1 in col else 0 for col in self.grid])
    
    def can_move_left(self, grid):
        for i_y, (row) in enumerate(zip(*self.grid)):
            for i_x, (sq) in enumerate(row):
                if sq:
                    if grid[self.x+i_x-1][self.y+i_y]:
                        return False
                    break
        return True

    def can_move_right(self, grid):
        for i_y, (row) in enumerate(zip(*self.grid)):
            for i_x, (sq) in enumerate(reversed(row)):
                if sq:
                    if grid[self.x+self.get_width()][self.y+i_y]:
                        return False
                    break
        return True