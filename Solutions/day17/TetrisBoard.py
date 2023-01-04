import copy

import numpy as np
from Solutions.day17.TetrisPiece import TetrisPiece, FallingTetrisPiece

h_line = TetrisPiece(np.ones((1,4), dtype=int))
cross = TetrisPiece(np.array([[0,1,0],[1,1,1],[0,1,0]]))
l_piece = TetrisPiece(np.array([[1,1,1],[0,0,1],[0,0,1]]))
v_line = TetrisPiece(np.ones((4,1), dtype=int))
square = TetrisPiece(np.ones((2,2), dtype=int))

all_pieces = [h_line, cross, l_piece, v_line, square]
init_spawn_height = 4


class TetrisBoard:
    def __init__(self, wind_array):
        super().__init__()

        self.board = np.zeros((1000000, 9), dtype=int)
        self.board[0,:] = 1
        self.board[:,0] = 1
        self.board[:,8] = 1

        self.pieces = all_pieces
        self.piece_index = 0
        self.age = 0
        self.wind_array = wind_array
        self.wind_index = 0
        self.spawn_height = init_spawn_height
        self.height_per_piece = []
        self.wind_applied = 0
        self.wind_per_piece = []

        self.cut_tower = int(0) # How much of the tower has been removed

    def print_board(self, rows=10):
        for row in range(rows, -1, -1):
            print(self.board[row,:])
        print("\n\n")

    # Get next piece in sequence, and increment sequence index
    # Return a falling piece
    def get_next_piece(self):
        piece_to_return = self.pieces[self.piece_index]
        self.piece_index += 1
        if self.piece_index >= len(self.pieces):
            self.piece_index = 0
        return FallingTetrisPiece(piece_to_return, self.spawn_height)

    # Apply wind to falling piece, then increment wind index
    def apply_wind(self, falling_piece: FallingTetrisPiece):

        self.wind_applied += 1
        direction = self.wind_array[self.wind_index]
        self.wind_index += 1
        if self.wind_index >= len(self.wind_array):
            self.wind_index = 0

        if direction < 0 and falling_piece.left_hand_side == 1:
            return
        elif direction > 0 and falling_piece.right_hand_side == falling_piece.board_width-2:
            return
        elif self.check_sideways_collision(falling_piece, direction):
            return

        falling_piece.blow_piece(direction)



    # Check if a piece has landed, if not
    def move_piece_down(self, falling_piece: FallingTetrisPiece):
        if self.has_piece_landed(falling_piece):
            return True
        falling_piece.height -= 1
        return False

    def has_piece_landed(self, falling_piece):
        # Dumb check for now, premature optimization is the root of all evil.
        return self.check_each_row_for_contact(falling_piece)

    def check_sideways_collision(self, falling_piece: FallingTetrisPiece, direction):
        for row in range(falling_piece.piece.array.shape[0]):
            for col in range(falling_piece.piece.array.shape[1]):
                if falling_piece.piece.array[row, col] == 1:
                    if self.board[row + falling_piece.height, col + falling_piece.left_hand_side + direction] == 1:
                        return True
        return False

    def check_each_row_for_contact(self, falling_piece:FallingTetrisPiece):
        for i in range(falling_piece.left_hand_side, falling_piece.right_hand_side+1):
            if self.board[falling_piece.height + falling_piece.get_bottom_height_at_board_column_i(i) - 1, i] == 1:
                return True
        return False

    def update_board(self, fallen_piece):
        # Set all squares of piece to 1
        for row in range(fallen_piece.piece.array.shape[0]):
            for col in range(fallen_piece.piece.array.shape[1]):
                if fallen_piece.piece.array[row, col] == 1:
                    self.board[row + fallen_piece.height, col + fallen_piece.left_hand_side] = 1
                    if row + fallen_piece.height + 4 > self.spawn_height:
                        self.spawn_height = row + fallen_piece.height + 4
        # self.print_board()

    def make_n_pieces(self, n):
        for i in range(0, n):
            if i%100000 == 0:
                print("Doing step ", i)
            self.add_piece()
            self.height_per_piece.append(self.spawn_height - 3)
            self.wind_per_piece.append(self.wind_applied)

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
        self.update_board(piece)

    def highest_point_on_tower(self):
        max_height = 0
        for col in range(1, self.board.shape[1]-1):
            max_height = max(max_height, np.where(self.board[:, col] == 1)[0][-1])
        return int(max_height) + self.cut_tower
