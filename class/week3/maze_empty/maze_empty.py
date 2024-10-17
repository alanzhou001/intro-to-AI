import sys

class Node():
    """The node need to keep track of the current state, the parent node, and the action"""

    #To do

    raise NotImplementedError


class StackFrontier():
    def __init__(self):
        """Initialize the frontier"""
        # To do
        raise NotImplementedError

    def add(self, node):
        """Add a node to the frontier"""
        # To do
        raise NotImplementedError

    def contains_state(self, state):
        """Check whether the state is already contain in the frontier"""
        # To do
        raise NotImplementedError

    def empty(self):
        """Check whether the frontier is empty or not"""
        # To do
        raise NotImplementedError

    def remove(self):
        """Remove/Select a node from the frontier
           Last-in first-out
        """
        # To do
        raise NotImplementedError


class QueueFrontier(StackFrontier):
    """Inherit from stack frontier"""
    def remove(self):
        """Remove/Select a node from the frontier
           First-in first-out
        """
        # To do
        raise NotImplementedError


class Maze():

    def __init__(self, filename):

        # Read file
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None


    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result


    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Start with a frontier that contains the initial state
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Start with an empty explore set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If the frontier is empty, then there is no solution
            if frontier.empty():
                raise Exception("no solution")

            # remove (select) a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If the node contains goal state, return the solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Else:
            # Add the node to the explore set
            self.explored.add(node.state)

            # Expand node, add resulting nodes to the frontier if they aren’t already in the frontier or the explored set
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumer2zate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            (100,149,237) # light blue
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    # dark blue
                    fill = (0, 0, 128)

                # Start
                elif (i, j) == self.start:
                    # red
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    # green
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    # yellow
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    # brown
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    # white
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if __name__=="__main__":
    # make sure the terminal argument is in the correct format
    if len(sys.argv) != 2:
        sys.exit("Usage: python maze.py maze.txt")

    # Initialize the maze
    m = Maze(sys.argv[1])
    print("Maze:")
    m.print()

    # Solve the result
    print("Solving...")
    m.solve()

    # Output the result in the terminal
    print("States Explored:", m.num_explored)
    print("Solution:")
    m.print()

    # Output the result to general audience
    m.output_image("maze.png", show_explored=False)