import copy

from Part1.UCS import UCS
from Part1.BIDIRECTIONAL import BidirectionalSearch
from Part1.IDS import IDS


class RubicProblem:
    def __init__(self, rubic_color):
        self.first_node = rubic_color
        # [[5, 3, 4], [3, 1, 2], [2, 1, 2], [1, 1, 2] if is index i
        # means that side of i is neighbor to side of 5 and squares of 3 and 4 in it.
        self.relations = [[[5, 2, 3], [3, 1, 0], [2, 1, 0], [1, 1, 0]],  # side of 0
                          [[0, 0, 2], [2, 0, 2], [4, 0, 2], [5, 0, 2]],  # side of 1
                          [[0, 2, 3], [3, 0, 2], [4, 1, 0], [1, 3, 1]],  # side of 2
                          [[0, 3, 1], [5, 3, 1], [4, 3, 1], [2, 3, 1]],  # side of 3
                          [[2, 2, 3], [3, 2, 3], [5, 1, 0], [1, 2, 3]],  # side of 4
                          [[4, 2, 3], [3, 3, 1], [0, 1, 0], [1, 0, 2]],  # side of 5
                          ]
        self.actions = [[0, 1], [0, 0], [1, 1], [1, 0], [2, 1], [2, 0], [3, 1], [3, 0], [4, 1], [4, 0], [5, 1], [5, 0]]
        self.parent = {}
        self.set_parent(self.first_node, None, None)

    def print_rubic(self, main_rubic, neighbor_rubic, name):
        print("##########################" + str(name) + "############")
        print("######" + str(main_rubic[0][0:2]) + "######    " + "    ######" + str(neighbor_rubic[0][0:2]) + "######")
        print("######" + str(main_rubic[0][2:4]) + "######    " + "    ######" + str(neighbor_rubic[0][2:4]) + "######")
        print(str(main_rubic[1][0:2]) + str(main_rubic[2][0:2]) + str(main_rubic[3][0:2]) + "        " + str(
            neighbor_rubic[1][0:2]) + str(neighbor_rubic[2][0:2]) + str(neighbor_rubic[3][0:2]))
        print(str(main_rubic[1][2:4]) + str(main_rubic[2][2:4]) + str(main_rubic[3][2:4]) + "        " + str(
            neighbor_rubic[1][2:4]) + str(neighbor_rubic[2][2:4]) + str(neighbor_rubic[3][2:4]))
        print("######" + str(main_rubic[4][0:2]) + "######    " + "    ######" + str(neighbor_rubic[4][0:2]) + "######")
        print("######" + str(main_rubic[4][2:4]) + "######    " + "    ######" + str(neighbor_rubic[4][2:4]) + "######")
        print("######" + str(main_rubic[5][0:2]) + "######    " + "    ######" + str(neighbor_rubic[5][0:2]) + "######")
        print("######" + str(main_rubic[5][2:4]) + "######    " + "    ######" + str(neighbor_rubic[5][2:4]) + "######")
        print("")
        print("")

    def get_child(self, rubic, action):
        relations = self.relations
        side = action[0]
        left_right = action[1]
        neighbor_rubic = copy.deepcopy(rubic)
        if left_right == 1:
            c = rubic[side][2]
            neighbor_rubic[side][2] = rubic[side][3]
            neighbor_rubic[side][3] = rubic[side][1]
            neighbor_rubic[side][1] = rubic[side][0]
            neighbor_rubic[side][0] = c
            temp1 = relations[side][0]
            for rel in relations[side][1:4]:
                neighbor_rubic[rel[0]][rel[1]] = rubic[temp1[0]][temp1[1]]
                neighbor_rubic[rel[0]][rel[2]] = rubic[temp1[0]][temp1[2]]
                temp1 = rel
            neighbor_rubic[relations[side][0][0]][relations[side][0][1]] = rubic[temp1[0]][temp1[1]]
            neighbor_rubic[relations[side][0][0]][relations[side][0][2]] = rubic[temp1[0]][temp1[2]]
        else:
            c = rubic[side][0]
            neighbor_rubic[side][0] = rubic[side][1]
            neighbor_rubic[side][1] = rubic[side][3]
            neighbor_rubic[side][3] = rubic[side][2]
            neighbor_rubic[side][2] = c
            temp1 = relations[side][3]
            for rel in relations[side][3::-1]:
                neighbor_rubic[rel[0]][rel[1]] = rubic[temp1[0]][temp1[1]]
                neighbor_rubic[rel[0]][rel[2]] = rubic[temp1[0]][temp1[2]]
                temp1 = rel
            neighbor_rubic[relations[side][3][0]][relations[side][3][1]] = rubic[temp1[0]][temp1[1]]
            neighbor_rubic[relations[side][3][0]][relations[side][3][2]] = rubic[temp1[0]][temp1[2]]
        return neighbor_rubic

    def get_actions(self):
        return self.actions

    # This function returns one of goals
    def get_goal(self):
        rubic = [[1, 1, 1, 1],
                 [2, 2, 2, 2],
                 [3, 3, 3, 3],
                 [4, 4, 4, 4],
                 [5, 5, 5, 5],
                 [6, 6, 6, 6]]
        # this "set parent" is for bidirectional search
        self.set_parent(rubic, None, None)
        return rubic

    def goal_test(self, rubic):
        is_goal = True
        for side in rubic:
            side_color = 0
            for square in side:
                if side_color == 0:
                    side_color = square
                elif side_color != square:
                    is_goal = False
                    break
            if not is_goal:
                break
        return is_goal

    def set_parent(self, child, parent, action):
        self.parent[id(child)] = [parent, action]

    def get_heuristic(self, rubic_colors):
        number_of_sides = [0, 0, 0, 0]  # [1 different color, 2 different color, 3 different color, 4 different color]
        for side in rubic_colors:
            different_colors = [False, False, False, False, False, False]
            for square in side:
                different_colors[square - 1] = True
            number_of_different_colors = 0
            for color in different_colors:
                if color: number_of_different_colors += 1
            number_of_sides[number_of_different_colors-1] += 1
        heuristic = number_of_sides[3] * 4 + number_of_sides[2] * 2 + number_of_sides[1]
        return heuristic


rubic_colors = []
print("enter colors of rubic:")
side_input = input()
while len(side_input) != 0:
    side_input = side_input.split(' ')
    side_colors = []
    for i in side_input:
        side_colors.append(int(i))
    rubic_colors.append(side_colors)
    side_input = input()
print("witch algorithm: \n1) IDS\n2) Bidirectional\n3) UCS")
number_of_algorithm = int(input())

rubic_problem = RubicProblem(rubic_colors)
# c = rubic_colors
# s = time.time()
# for i in range(100000):
#     c = rubic_problem.get_child(c, [2, 0])
# e = time.time()
# print(e - s)

if number_of_algorithm == 1:
    # IDS algorithm
    ids = IDS(rubic_problem, 0)
    solution = ids.iterative_deepening_search()
    path = solution[0]
    if path == 'cutoff' or path == 'failure':
        print(path)
    else:
        for s in path[::-1]:
            rubic_problem.print_rubic(rubic_problem.first_node, s[1], s[0])
        print("depth of result: " + str(solution[1]))
        print("number of_nodes in memory: " + str(solution[2]))
        print("number of created node: " + str(solution[3]))
        print("number of expanded node: " + str(solution[4]))

elif number_of_algorithm == 2:
    # Bidirectional algorithm
    bidirectional = BidirectionalSearch(rubic_problem)
    solution = bidirectional.run_search()
    if solution != 'failure':
        for s in solution[0]:
            rubic_problem.print_rubic(rubic_problem.first_node, s[0], '######')
        print("actions: " + str(solution[1]))
    else:
        print(solution[0])
    print("depth of result: " + str(solution[2]))
    print("number of_nodes in memory: " + str(solution[3]))
    print("number of created node: " + str(solution[4]))
    print("number of expanded node: " + str(solution[5]))

else:
    # A star algorithm
    ucs = UCS(rubic_problem)
    solution = ucs.run_search()
    path = solution[0]
    for s in path:
        rubic_problem.print_rubic(rubic_problem.first_node, s[0], s[1])
    print("depth of result: " + str(solution[1]))
    print("number of_nodes in memory: " + str(solution[2]))
    print("number of created node: " + str(solution[3]))
    print("number of expanded node: " + str(solution[4]))

# r1 = rubic_problem.get_child(rubic_colors, [1,1])
# r2 = rubic_problem.get_child(r1, [3,1])
# r3 = rubic_problem.get_child(r2, [4,0])
# r4 = rubic_problem.get_child(r3, [2,1])
# r5 = rubic_problem.get_child(r4, [3,0])
# r6 = rubic_problem.get_child(r4, [5,0])
# r7 = rubic_problem.get_child(r4, [1,1])
# print(r7)