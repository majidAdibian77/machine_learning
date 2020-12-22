class IDS:
    def __init__(self, problem, first_limit):
        self.problem = problem
        self.first_node = problem.first_node
        self.first_limit = first_limit
        self.solution = []
        self.number_of_expanded_node = 0
        self.number_of_created_node = 0

    def recursive_DLS(self, node, problem, limit):
        self.number_of_created_node += 1
        if problem.goal_test(node):
            self.solution.append([None, node])
            return self.solution
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            actions = problem.get_actions()
            self.number_of_expanded_node += 1
            for action in actions:
                child = problem.get_child(node, action)
                result = self.recursive_DLS(child, problem, limit-1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result != 'failure':
                    self.solution.append([action, node])
                    return self.solution
            if cutoff_occurred:
                return 'cutoff'
            else:
                return 'failure'

    def depth_limited_search(self, problem, depth):
        return self.recursive_DLS(problem.first_node, problem, depth)

    def iterative_deepening_search(self):
        result = 'cutoff'
        number_of_nodes_in_memory = 0
        for depth in range(self.first_limit, 10):
            result = self.depth_limited_search(self.problem, depth)
            number_of_nodes_in_memory = depth+1
            if result != 'cutoff' and result != 'failure':
                break
        return [result, number_of_nodes_in_memory-1, number_of_nodes_in_memory, self.number_of_created_node, self.number_of_expanded_node]
