import heapq


class UCS:
    def __init__(self, problem):
        start = problem.first_node
        self.problem = problem
        self.start = start
        min_heap = [(0, start)]
        heapq.heapify(min_heap)
        self.min_heap = min_heap
        self.g_nodes = {id(start): 0}
        self.number_of_created_node = 1
        self.number_of_expanded_node = 0

    def run_search(self):
        goal = None
        if self.problem.get_heuristic(self.start) == 0:
            goal = self.start
        while not goal:
            current_node = heapq.heappop(self.min_heap)[1]
            if self.problem.goal_test(current_node):
                goal = current_node
                break
            actions = self.problem.get_actions()
            self.number_of_expanded_node += 1
            for action in actions:
                child = self.problem.get_child(current_node, action)
                self.problem.set_parent(child, current_node, action)
                self.number_of_created_node += 1
                g_child = self.g_nodes[id(current_node)] + 1
                self.g_nodes[id(child)] = g_child
                # heuristic = self.problem.get_heuristic(child)
                # if heuristic == 0:
                #     goal = child
                #     break
                # f_child = g_child + heuristic

                heapq.heappush(self.min_heap, (g_child, child))
        path = [[goal, None]]
        parent = self.problem.parent[id(goal)]
        while parent[0]:
            path.append(parent)
            parent = self.problem.parent[id(parent[0])]
        path = path[::-1]

        number_of_nodes_in_memory = self.min_heap.__len__()

        return [path, len(path)-1, number_of_nodes_in_memory, self.number_of_created_node, self.number_of_expanded_node]


