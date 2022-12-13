import numpy as np

# Read input section
f = open("../../Inputs/day8/part1.dat", "r")
input = f.read().splitlines()


tree_list = []
for row in input:
    row_input = []
    for char in row:
        row_input.append(int(char))
    tree_list.append(row_input)

tree_array = np.array(tree_list)


# Iterate through a vector of trees in direction of viewing, marking true for those you can see from that direction
def which_trees_visible(tree_vec):
    visible_trees = []
    max_height = -1
    for tree in tree_vec:
        if tree > max_height:
            max_height = tree
            visible_trees.append(1)
        else:
            visible_trees.append(0)
    return visible_trees


def calc_visible_trees(tree_array):

    visible_tree_array = np.zeros(tree_array.shape)

    for row in range(0, tree_array.shape[0]):
        # From top
        this_res = which_trees_visible(tree_array[row, :])
        visible_tree_array[row, :] = np.maximum(visible_tree_array[row, :], this_res)

        # From bottom
        this_res = which_trees_visible(reversed(tree_array[row, :]))
        this_res.reverse()
        visible_tree_array[row, :] = np.maximum(visible_tree_array[row, :], this_res)

    for col in range(0, tree_array.shape[1]):
        # From left
        this_res = which_trees_visible(tree_array[:, col])
        visible_tree_array[:, col] = np.maximum(visible_tree_array[:, col], this_res)

        # From right
        this_res = which_trees_visible(reversed(tree_array[:, col]))
        this_res.reverse()
        visible_tree_array[:, col] = np.maximum(visible_tree_array[:, col], this_res)

    return visible_tree_array


# Determine viewing distance from the tree in element 0
def view_distance(tree_vec):
    view_distance = 0
    for tree in tree_vec[1:]:
        view_distance += 1
        if tree >= tree_vec[0]:
            return view_distance
    return view_distance


# Part 2, calc scenic score for each tree
def calc_scenic_score(position, tree_array):
    # Look up
    up_score = view_distance(tree_array[0:position[0]+1, position[1]][::-1])
    # Look down
    down_score = view_distance(tree_array[position[0]:, position[1]])
    # Look left
    left_score = view_distance(tree_array[position[0], 0:position[1]+1][::-1])
    # Look right
    right_score = view_distance(tree_array[position[0], position[1]:])

    return up_score * down_score * left_score * right_score


visible_tree_array = calc_visible_trees(tree_array)

print("Total visible trees from exterior is:", visible_tree_array.sum())

max_scenic_score = 0

for row in range(0, tree_array.shape[0]):
    for col in range(0, tree_array.shape[1]):
        this_score = calc_scenic_score((row, col), tree_array)
        if max_scenic_score < this_score:
            max_scenic_score = this_score

print("Max scenic score: ", max_scenic_score)