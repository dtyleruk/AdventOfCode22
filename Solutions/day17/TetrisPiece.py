import numpy as np


class TetrisPiece:

    def __init__(self, piece_array):
        super().__init__()
        self.array = piece_array
        self.width = self.array.shape[1]
        self.bottom_heights = create_bottom_height_map(self.array)
        self.top_heights = create_top_height_map(self.array)


# Makes vector of length width determining how high the bottom part of each piece is relative to the lowest part
def create_bottom_height_map(shape_array):
    bottom_heights = []
    for i in range(0, shape_array.shape[1]):
        #Find the final 1 in this column

        indices = np.argwhere(shape_array[:, i] == 1)
        last_index = indices[-1][0] + 1
        bottom_heights.append(shape_array.shape[0] - last_index)
    return bottom_heights


# Makes vector of length width determining how high the top part of each piece is relative to the lowest part
def create_top_height_map(shape_array):
    top_heights = []
    for i in range(0, shape_array.shape[1]):
        #Find the first 1 in this column
        indices = np.argwhere(shape_array[:, i] == 1)
        last_index = indices[0][0]
        top_heights.append(shape_array.shape[0] - last_index)
    return top_heights


# Spawn height is how high the lowest point is.
class FallingTetrisPiece:
    def __init__(self, piece:TetrisPiece, spawn_height, board_col_heights, board_width=7):
        super().__init__()
        self.piece = piece
        self.height = spawn_height
        self.left_hand_side = 2
        self.right_hand_side = self.left_hand_side + self.piece.width - 1
        self.board_width = board_width
        self.board_column_heights = board_col_heights

    def get_bottom_height_at_board_column_i(self, i):
        return self.piece.bottom_heights[i - self.left_hand_side]

    def get_top_height_at_board_column_i(self, i):
        return self.piece.top_heights[i - self.left_hand_side]

    def blow_piece(self, direction):
        if direction < 0 and self.left_hand_side == 0:
            return
        elif direction > 0 and self.right_hand_side == self.board_width-1:
            return

        # Now need to check there is no collision with existing board pieces

        self.left_hand_side += direction
        self.right_hand_side += direction
