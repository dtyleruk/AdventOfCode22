import numpy as np


class TetrisBoard:
    def __init__(self, shapes):
        super().__init__()
        self.board = np.zeros([3, 7], dtype=int)
        self.pieces = shapes
        self.piece_index = 0
        self.age = 0

    def add_piece(self):
        