class Student:
    def __init__(self, name, major):
        self.name = name
        self.major = major
        self.score=dict()

    def update(self,courseName,courseScore):
        self.score[courseName]=courseScore

    def averageScore(self):
        if len(self.score)==0:
            return 'No Score'
        else:
            return sum(self.score.values())/len(self.score)


Lulu=Student('Lulu','IS')
Lulu.name
Lulu.major

Lulu.update('AI',90)
Lulu.update('Finance',80)


Lulu.averageScore()
Lulu.score
print(Lulu)

###operater overload
class Student:
    def __init__(self, name, major):
        self.name = name
        self.major = major
        self.score=dict()

    def update(self,courseName,courseScore):
        self.score[courseName]=courseScore

    def averageScore(self):
        if len(self.score)==0:
            return 'No Score'
        else:
            return sum(self.score.values())/len(self.score)

    def __str__(self):
        return f"{self.name}'s major is {self.major}"


    def __gt__(self, other):
        if self.averageScore()> other.averageScore():
            return True
        else:
            return False

Lulu=Student('Lulu','IS')
print(Lulu)

Lulu.update('AI',85)
Lulu.update('Finance',78)
Alex=Student('Alex','AI')
Alex.update('Fina',90)
Alex.update('Acct',95)
lulu > Alex


### Inheritance
class Professor(Student):
    def __init__(self,name,major,title):
        super().__init__(name,major)
        self.title=title

    def update(self):
        self.title='Professor'


lulu=Professor('Lulu','AI','Assistant Professor')
lulu.title

lulu.update()
lulu.title
