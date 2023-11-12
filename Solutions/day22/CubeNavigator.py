from Solutions.day22.GridNavigator import convert_grid_to_array, convert_instructions_to_list
import numpy as np

class CubeNavigator:
    def __init__(self, input, face_size):
        self.grid = convert_grid_to_array(input[:-2])
        self.instructions = convert_instructions_to_list(input[-1])
        self.faces_by_coordinate = split_grid_into_faces(self.grid, face_size)
        self.faces_on_cube = define_cube_faces(self.faces_by_coordinate)
        self.face_orientations = define_cube_edges()

    def move_off_edge(self, from_which_face, edge_1, edge_2, position_on_edge):
        edge_to_move_to = self.find_edge(edge_1, edge_2)



        edge_to_move_to.remove(from_which_face)

        return 1

    def find_edge(self, edge_1, edge_2):
        edge_on_these_faces = []
        for face in self.face_orientations.keys():
            if is_edge_on_this_face(self.face_orientations[face], edge_1, edge_2) != 0:
                edge_on_these_faces.append(face)
        return edge_on_these_faces

    def do_orientations_match(self, edge_1, edge_2):
        edges = self.find_edge(edge_1, edge_2)
        orientation_1 = is_edge_clockwise(self.face_orientations[edges[0]], edge_1, edge_2)
        orientation_2 = is_edge_clockwise(self.face_orientations[edges[1]], edge_1, edge_2)

        return orientation_1 == orientation_2

def is_edge_clockwise(face_edges, edge_1, edge_2):
    edge1_ind = face_edges.index(edge_1)
    edge2_ind = face_edges.index(edge_2)

    ind_diff = edge2_ind - edge1_ind

    if ind_diff == 1 or ind_diff == -3:
        return True
    return False



def is_edge_on_this_face(face_edges, edge_1, edge_2):
    if edge_1 in face_edges and edge_2 in face_edges:
        return 1
    else:
        return 0

def split_grid_into_faces(grid, face_size):

    faces = {}

    for xPos in range(0, int(grid.shape[0] / face_size)):
        for yPos in range(0, int(grid.shape[1] / face_size)):
            xStart = xPos*face_size
            xEnd = (xPos+1)*face_size
            yStart = yPos * face_size
            yEnd = (yPos + 1) * face_size

            if grid[xStart:xEnd,yStart:yEnd].max() > 0:
                faces[xPos,yPos] = grid[xStart:xEnd,yStart:yEnd]

    return faces


def define_cube_faces(faces):
    edge_positions = {}

    edge_positions["Top"] = faces[1, 0]
    edge_positions["Bottom"] = faces[1, 2]
    edge_positions["Left"] = faces[1, 1]
    edge_positions["Right"] = faces[2, 3]
    edge_positions["Front"] = faces[2, 2]
    edge_positions["Back"] = faces[0, 2]

    return edge_positions

def define_cube_edges():
    # Now need a map from grid position to correct orientation on grid
    # Define corners as 1,2,3,4 clockwise from bottom, starting at top left
    # 5,6,7,8 clockwise from top, starting at top left
    # Each face's corners are defined in the order top left, top right, bottom right, bottom left

    face_orientations = {}
    face_orientations["Bottom"] = [1, 2, 3, 4]
    face_orientations["Top"] = [6, 5, 8, 7]
    face_orientations["Left"] = [5, 1, 4, 8]
    face_orientations["Right"] = [2, 3, 6, 7]
    face_orientations["Front"] = [8, 7, 3, 4]
    face_orientations["Back"] = [1, 2, 6, 5]

    return face_orientations