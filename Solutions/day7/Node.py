class Node:
    def __init__(self, parent, name):
        self.parent = parent  # Is also a node
        self.name = name
        self.children = []  # Future nodes
        self.files = []  # Nodes with a size (maybe will be combined with children at some point

    def add_node(self, node):
        self.children.append(node)

    def add_file(self, file):
        self.files.append(file)

    def get_size(self):
        size = 0
        for node in self.children:
            size += node.get_size()
        for file in self.files:
            size += file.size
        return size

    # Returns list of all nodes and sub-nodes contained in this node
    def get_all_nodes(self):
        all_nodes = []
        for node in self.children:
            all_nodes.append(node)
            sub_nodes = node.get_all_nodes()
            for sub_node in sub_nodes:
                all_nodes.append(sub_node)
        return all_nodes


class File:
    def __init__(self, size, name):
        self.size = size
        self.name = name
