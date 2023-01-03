import numpy as np

from Solutions.day17.TetrisBoard import TetrisBoard
from Solutions.day17.TetrisPiece import TetrisPiece

f = open("../../Inputs/day17/test_data.dat", "r")
input = f.read().splitlines()

h_line = TetrisPiece(np.array([1, 1, 1, 1]))
cross = TetrisPiece(np.array([[0,1,0],[1,1,1],[0,1,0]]))
l_piece = TetrisPiece(np.array([[0,0,1],[0,0,1],[1,1,1]]))
v_line = TetrisPiece(np.array([[1], [1], [1], [1]]))
square = TetrisPiece(np.array([[1,1],[1,1]]))

board = TetrisBoard([h_line, cross, l_piece, v_line, square])


belb = 1

