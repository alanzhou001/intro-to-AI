import sys
from util import Node, StackFrontier, QueueFrontier


class WareHouse():

    def __init__(self, filename, start, goals):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start
        if len(start) != 1:
            raise Exception("warehouse must have exactly one start point")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls, goals, and cell_to_letter
        self.walls = []
        self.goal = []
        self.cell_to_letter = dict()
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j]==start:
                        self.start=(i,j)
                        row.append(False)
                        self.cell_to_letter[(i,j)]=contents[i][j]
                    elif contents[i][j] in goals:
                        self.goal.append((i,j))
                        row.append(False)
                        self.cell_to_letter[(i, j)] = contents[i][j]
                    elif contents[i][j] == "#":
                        row.append(True)
                    else:
                        row.append(False)
                        self.cell_to_letter[(i, j)] = contents[i][j]

                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None
        self.num_explored = 0

    def print(self):
        solution = self.solution[2] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print('\033[91m' + self.cell_to_letter[(i,j)] + '\033[0m', end="")
                elif (i, j) in self.goal:
                    print('\033[91m' + self.cell_to_letter[(i,j)] + '\033[0m', end="")
                elif solution is not None and (i, j) in solution:
                    print('\033[92m' + self.cell_to_letter[(i,j)] + '\033[0m', end="")
                else:
                    try:
                        print(self.cell_to_letter[(i,j)], end="")
                    except:
                        print(' ', end="")
            print()
        print()


    def neighbors(self, state):
        """Return the possible (action, (x_position, y_position)) pairs for state"""

        #TO DO
        raise NotImplementedError


    def solve(self):
        """Finds a solution to warehouse, if one exists."""

        #TO DO
        raise NotImplementedError



    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        wall=5
        text='A'

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (int((self.width-1)/2) * cell_size+ int((self.width+1)/2) *wall, int((self.height-1)/2) * cell_size+ int((self.height+1)/2) *wall),
            "white"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[2] if self.solution is not None else None
        current_y=0
        for i, row in enumerate(self.walls):
            current_x=0
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) in self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    # fill = (237, 240, 252)
                    fill = 'white'

                # Determin the width and height of the cell
                if i %2 == 1:
                    y = cell_size
                else:
                    y = wall

                if j % 2 ==1:
                    x= cell_size
                else:
                    x = wall


                # Draw cell
                draw.rectangle(
                    ([(current_x, current_y),
                      (current_x + x, current_y+ y)]),
                    fill=fill
                )

                if x== cell_size and y == cell_size:
                    draw.text((current_x+x/3,current_y+y/3),text,fill='black', font=ImageFont.truetype("Arial.ttf",20))
                    text=chr(ord(text)+1)

                current_x=current_x+x
                # print([(current_x, current_y),
                #       (current_x + x, current_y+ y)],fill)
            current_y = current_y + y

        img.save(filename)


def main():
    if len(sys.argv) != 4:
        sys.exit("Usage: python Warehouse.py Warehouse.txt start goals")

    m = WareHouse(sys.argv[1], sys.argv[2], sys.argv[3])
    print("WareHouse:")
    m.print()
    print("Solving...")
    m.solve()
    print("States Explored:", m.num_explored)
    print(len(m.solution[0])-1, "step solution:", m.solution)
    m.print()
    m.output_image("WareHouse.png", show_explored=True)


if __name__ == '__main__':
    main()