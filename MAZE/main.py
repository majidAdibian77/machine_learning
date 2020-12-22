class Node:
    def __init__(self, color, number_of_node):
        self.number_of_node = number_of_node
        self.color = color
        self.neighbor = {}

    def add_neighbor(self, neighbor, color):
        if color in self.neighbor.keys():
            self.neighbor[color].append(neighbor)
        else:
            self.neighbor[color] = [neighbor]


class DFS:
    def __init__(self, nodes, start_node1, start_node2):
        self.nodes = nodes
        self.start_node1 = start_node1
        self.start_node2 = start_node2
        self.visited = set()

    def dfs_algorithm(self, node1, node2, turn):
        if turn:
            if node2.color == '':  # if this child is goal
                return []
            if node1.color in node2.neighbor.keys():
                for child in node2.neighbor[node1.color]:
                    if not (node1.number_of_node, self.nodes[child].number_of_node, 1 - turn) in self.visited:
                        self.visited.add((node1.number_of_node, self.nodes[child].number_of_node, 1 - turn))
                        result = self.dfs_algorithm(node1, self.nodes[child], 1 - turn)
                        if result != 'failed':
                            if result:
                                result.append([2, child])
                                return result
                            else:
                                return [[2, child]]
                        self.visited.remove((node1.number_of_node, self.nodes[child].number_of_node, 1 - turn))
                    if not (node1.number_of_node, self.nodes[child].number_of_node, turn) in self.visited:
                        self.visited.add((node1.number_of_node, self.nodes[child].number_of_node, turn))
                        result = self.dfs_algorithm(node1, self.nodes[child], turn)
                        if result != 'failed':
                            if result:
                                result.append([2, child])
                                return result
                            else:
                                return [[2, child]]
                        self.visited.remove((node1.number_of_node, self.nodes[child].number_of_node, turn))

            return 'failed'
        else:
            if node1.color == '':  # if this child is goal
                return []
            if node2.color in node1.neighbor.keys():
                for child in node1.neighbor[node2.color]:
                    if not (self.nodes[child].number_of_node, node2.number_of_node, 1 - turn) in self.visited:
                        self.visited.add((self.nodes[child].number_of_node, node2.number_of_node, 1 - turn))
                        result = self.dfs_algorithm(self.nodes[child], node2, 1 - turn)
                        if result != 'failed':
                            if result:
                                result.append([1, child])
                                return result
                            else:
                                return [[1, child]]
                        self.visited.remove((self.nodes[child].number_of_node, node2.number_of_node, 1 - turn))
                    if not (self.nodes[child].number_of_node, node2.number_of_node, turn) in self.visited:
                        self.visited.add((self.nodes[child].number_of_node, node2.number_of_node, turn))
                        result = self.dfs_algorithm(self.nodes[child], node2, turn)
                        if result != 'failed':
                            if result:
                                result.append([1, child])
                                return result
                            else:
                                return [[1, child]]
                        self.visited.remove((self.nodes[child].number_of_node, node2.number_of_node, turn))
            return 'failed'

    def run(self):
        turn = 1  # if this variable is 0 it is queue1's turn and if is 1 it is queue2's turn
                  # and we should toggle it every time
        result = self.dfs_algorithm(self.start_node1, self.start_node2, turn)
        if result != 'failed':
            return result
        else:
            return self.dfs_algorithm(self.start_node1, self.start_node2, turn)


"""
    Getting inputs
"""

input1 = input().split(' ')
number_of_vertex = int(input1[0])
number_of_edge = int(input1[1])
input2 = input().split(' ')
nodes = []  # list of all nodes

# creating all nodes
i = 0
for i in range(len(input2)):
    node = Node(input2[i], i)
    nodes.append(node)
nodes.append(Node('', i+1))  # appending goal node to list of all nodes

# getting palace of Rocket and Lucky
input3 = input().split(' ')
place_of_R = int(input3[0]) - 1
place_of_L = int(input3[1]) - 1
# getting edges and adding to neighbour of nodes
for i in range(number_of_edge):
    input4 = input().split(' ')
    number_of_node = int(input4[0]) - 1
    neighbor = int(input4[1]) - 1
    edge_color = input4[2]
    nodes[number_of_node].add_neighbor(neighbor, edge_color)
dfs = DFS(nodes, nodes[place_of_R], nodes[place_of_L])
result = dfs.run()
if result == 'failed':
    print("failed")
else:
    for res in result:
        if res[0] == 1:
            name = 'R'
        else:
            name = 'L'
        print(name + ' ' + str(res[1]))
