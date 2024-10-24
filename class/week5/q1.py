class Node():
    """记录营销策略"""
    def __init__(self, strategy, parent, left, right):
        """记录子节点"""
        self.strategy = strategy
        self.parent = parent
        self.left = left
        self.right = right

class StackFrontier():
    """构建StackFrontier"""
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_strategy(self, strategy):
        return any(node.strategy == strategy for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


advertising={
    'Email Campaign':['Discount Offer','Content Marketing'],
    'Discount Offer':['Follow-up Email','Phone Call'],
    'Content Marketing':['Social Media Ad']
}


class Graph():
    """搜索"""
    def __init__(self, start):
        """储存必要信息"""
        self.start=start
        self.solution=[]

    def addNode(self,strategy, parent):
        """添加节点"""
        if strategy in advertising.keys():
            if len(advertising[strategy])==1:
                left=advertising[strategy][0]
                right=None
            else:
                left = advertising[strategy][0]
                right =advertising[strategy][1]
        else:
            left=None
            right=None

        return Node(strategy=strategy, parent=parent, left=left, right=right)


    def solve(self):
        """搜索所有的解"""
        # Start with a frontier that contains the initial strategy
        # 新建节点
        start = self.addNode(strategy=self.start, parent=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Start with an empty explore set
        self.explored = set()

        # Keep looping until all solutions are found
        while True:

            # If the frontier is empty, then there is no solution
            if frontier.empty():
                return

            # remove (select) a node from the frontier
            node = frontier.remove()

            # If the node contains goal strategy, return the solution
            if node.left == None: # 没有子节点
                solution = []
                while node.parent is not None:
                    solution.append(node.strategy)
                    node = node.parent
                solution.append(self.start)
                solution.reverse()
                self.solution.append(solution)

            else:
                # Add the node to the explore set
                self.explored.add(node.strategy)

                # Expand node, add resulting nodes to the frontier if they aren’t already in the frontier or the explored set
                for strategy in [node.left,node.right]: # neighbors()就是左右子节点
                    if not frontier.contains_strategy(strategy) and strategy not in self.explored and strategy is not None:
                        child = self.addNode(strategy=strategy, parent=node)
                        frontier.add(child)

g=Graph('Email Campaign')
g.solve()
g.solution