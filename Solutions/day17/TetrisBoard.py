import numpy as np
from Solutions.day17.TetrisPiece import TetrisPiece, FallingTetrisPiece

h_line = TetrisPiece(np.ones((1,4), dtype=int))
cross = TetrisPiece(np.array([[0,1,0],[1,1,1],[0,1,0]]))
l_piece = TetrisPiece(np.array([[0,0,1],[0,0,1],[1,1,1]]))
v_line = TetrisPiece(np.ones((4,1), dtype=int))
square = TetrisPiece(np.ones((2,2), dtype=int))

all_pieces = [h_line, cross, l_piece, v_line, square]
spawn_height = 4


class TetrisBoard:
    def __init__(self, wind_array):
        super().__init__()
        self.column_heights = np.zeros(7, dtype=int)
        self.pieces = all_pieces
        self.piece_index = 0
        self.age = 0
        self.wind_array = wind_array
        self.wind_index = 0

    # Get next piece in sequence, and increment sequence index
    # Return a falling piece
    def get_next_piece(self):
        piece_to_return = self.pieces[self.piece_index]
        self.piece_index += 1
        if self.piece_index >= len(self.pieces):
            self.piece_index = 0
        return FallingTetrisPiece(piece_to_return, max(self.column_heights) + spawn_height, self.column_heights)

    # Apply wind to falling piece, then increment wind index
    def apply_wind(self, falling_piece: FallingTetrisPiece):
        falling_piece.blow_piece(self.wind_array[self.wind_index])
        self.wind_index += 1
        if self.wind_index >= len(self.wind_array):
            self.wind_index = 0

    # Check if a piece has landed, if not
    def move_piece_down(self, falling_piece: FallingTetrisPiece):
        if self.has_piece_landed(falling_piece):
            return True
        falling_piece.height -= 1
        return False

    def has_piece_landed(self, falling_piece):
        if max(self.column_heights) + 1 < falling_piece.height:
            return False
        return self.check_each_row_for_contact(falling_piece)

    def check_each_row_for_contact(self, falling_piece:FallingTetrisPiece):
        for i in range(falling_piece.left_hand_side, falling_piece.right_hand_side+1):
            if self.column_heights[i] + 1 >= falling_piece.height + falling_piece.get_bottom_height_at_board_column_i(i):
                return True
        return False

    def update_column_heights(self, fallen_piece):
        for i in range(fallen_piece.left_hand_side, fallen_piece.right_hand_side+1):
            self.column_heights[i] = fallen_piece.height - 1 + fallen_piece.get_top_height_at_board_column_i(i)

    def make_n_pieces(self, n):
        for i in range(0, n):
            self.add_piece()

    def add_piece(self):
        piece = self.get_next_piece()

        landed = False

        # Piece falls
        while not landed:
            # Blow piece
            self.apply_wind(piece)
            # Move piece down
            landed = self.move_piece_down(piece)

        # Now piece becomes the column height
        self.update_column_heights(piece)
