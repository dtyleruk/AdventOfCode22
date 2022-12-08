from Solutions.day7.Node import Node, File
import re

f = open("../../Inputs/day7/part1.dat", "r")
instructions = f.read().splitlines()

base_node = Node(None, "base")


def change_current_node(current_node, instruction):
    node_name = instruction[5:]
    if node_name == "/":
        current_node = base_node

    elif node_name == "..":
        current_node = current_node.parent

    else:
        for node in current_node.children:
            if node.name == node_name:
                current_node = node
                break
    return current_node
    # Else find node with node_name in current_node


working_node = base_node
is_adding_to_node = False

# Build tree
for instruction in instructions:

    if instruction[0:4] == "$ cd":
        working_node = change_current_node(working_node, instruction)

    elif instruction == "$ ls":
        is_adding_to_node = True

    elif instruction[0:3] == "dir":
        dir_name = instruction[4:]
        new_node = Node(working_node, dir_name)
        working_node.add_node(new_node)

    else:
        file_info = re.split(" ", instruction)
        file = File(int(file_info[0]), file_info[1])
        working_node.add_file(file)


# Now work out size of each node in tree
all_nodes = base_node.get_all_nodes()

max_node_size = 100000
total_node_size = 0
for node in all_nodes:
    if node.get_size() <= max_node_size:
        total_node_size += node.get_size()

print("Total node size of nodes with size <= ", max_node_size, "= ", total_node_size)

total_disk_space = 70000000
required_unused_space = 30000000

total_used_space = base_node.get_size()
current_free_space = total_disk_space - total_used_space
required_deletion_size = required_unused_space - current_free_space

# Need to find the smallest node that is bigger than required_deletion_size
curr_node_to_delete = base_node
for node in all_nodes:
    if node.get_size() > required_deletion_size and node.get_size() < curr_node_to_delete.get_size():
        curr_node_to_delete = node

print("Total size of directory to delete is:", curr_node_to_delete.get_size())