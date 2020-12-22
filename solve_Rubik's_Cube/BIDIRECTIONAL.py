from queue import Queue


class BidirectionalSearch:

    def __init__(self, problem):
        self.problem = problem
        first_node = problem.first_node
        goal = problem.get_goal()
        visited = {''.join(str(i) for i in first_node)}
        self.visited1 = visited
        visited = {''.join(str(i) for i in goal)}
        self.visited2 = visited
        self.first_node = first_node
        self.goal = goal
        self.queue1 = Queue()
        self.queue1.put(first_node)
        self.queue2 = Queue()
        self.queue2.put(goal)
        self.nodes = [first_node, goal]

    def run_search(self):
        success = False
        node1 = None
        node2 = None
        while not self.queue1.empty() and not self.queue2.empty():
            if not self.queue1.empty():
                node = self.queue1.get()
                if node == self.goal:
                    node1 = node
                    node2 = self.goal
                    success = True
                    break
                else:
                    for n in list(self.queue2.queue):
                        if node == n:
                            node1 = node
                            node2 = n
                            success = True
                            break
                if success:
                    break
                actions = self.problem.get_actions()
                for action in actions:
                    child = self.problem.get_child(node, action)
                    self.problem.set_parent(child, node, action)
                    self.nodes.append(child)
                    child_str = ''.join(str(i) for i in child)
                    if child_str not in self.visited1:
                        self.visited1.add(child_str)
                        self.queue1.put(child)

            if not self.queue2.empty():
                node = self.queue2.get()
                if node == self.first_node:
                    node1 = self.first_node
                    node2 = node
                    success = True
                    break
                else:
                    # sentinel = object()
                    # for n in iter(self.queue2.get, sentinel):
                    for n in list(self.queue1.queue):
                        if node == n:
                            node2 = node
                            node1 = n
                            success = True
                            break
                if success:
                    break
                actions = self.problem.get_actions()
                for action in actions:
                    child = self.problem.get_child(node, action)
                    self.problem.set_parent(child, node, action)
                    self.nodes.append(child)
                    child_str = ''.join(str(i) for i in child)
                    if child_str not in self.visited2:
                        self.visited2.add(child_str)
                        self.queue2.put(child)

        number_of_created_node = self.visited1.__len__() + self.visited1.__len__()
        number_of_expanded_node = number_of_created_node - (self.queue1.queue.__len__() + self.queue2.queue.__len__())
        if success:
            res_actions = []
            res1 = []
            res2 = []
            res1.append([node1, None])
            parent = self.problem.parent[id(node1)]
            # parent has tow argument : first argument is node of parent and
            # the second is action of parent for this child
            while parent[0]:
                res1.append(parent)
                # res_actions.append(parent[1])
                parent = self.problem.parent[id(parent[0])]

            res2.append([node2, None])
            parent = self.problem.parent[id(node2)]

            # parent has tow argument : first argument is node of parent and
            # the second is action of parent for this child
            while parent[0]:
                res2.append(parent)
                # act = parent[1]
                # act[1] = 1 - act[1]
                # res_actions.append(act)
                parent = self.problem.parent[id(parent[0])]
            result = res1[::-1] + res2[1:]
            for node in res1[:0:-1]:
                res_actions.append(node[1])
            for node in res2[1:]:
                act = node[1]
                act[1] = 1 - act[1]
                res_actions.append(act)
            return [result, res_actions, len(result) - 1, number_of_created_node, number_of_created_node,
                    number_of_expanded_node]
        else:
            return ['failure', 0, number_of_created_node, number_of_created_node, number_of_expanded_node]
