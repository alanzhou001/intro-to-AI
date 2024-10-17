import math, random

class Hero():
    def __init__(self,x,y,blood=3000):
        """Initialize the Hero"""

        self.x = x
        self.y = y
        self.blood = blood

    def __str__(self):
        """Print out Hero's current location and blood"""

        return f"Current location: {self.x},{self.y}; Blood: {self.blood}"


    def move(self,x,y):
        """Move Hero by x, y"""

        self.x += x
        self.y += y


    def attack(self,other):
        """Return True if A attack B successfully, otherwise False"""

        distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        if distance <= 4 and distance >= 3:
            return True
        else:
            return False

def main():
    # Randomly create two Character A and B
    A=Hero(random.randrange(-5,6),random.randrange(-5,6))
    B=Hero(random.randrange(-5,6),random.randrange(-5,6))
    print('A: ', A)
    print('B: ', B)

    # Ask the user to input how to move character A
    x=float(input("Move character A horizontally by: "))
    y=float(input("Move character A vertically by: "))

    # Character A move by x, y
    A.move(x,y)

    # A atack B
    if A.attack(B):
        print("Attack -400")
        B.blood=B.blood-400
    else:
        print("Missed")

    print('A: ',A)
    print('B: ',B)


if __name__ == '__main__':
    main()

