### List
students = ["Harry", "Ron"]

print(students[0])
print(students[1])

students[0]='Harry Potter'
students

for student in students:
    print(student)

len(students)

###tuple
students = ("Harry", "Ron",'Draco')

print(students[0])
print(students[1])

students[0]='Harry Potter'

###函数返回多个值
def max_min(t):
    return max(t), min(t)

max, min=max_min([1,2,3])

###set

students=['Harry','Harry','Ron']
set(students)


### dictionary
students = {
    "Harry Potter": "Gryffindor",
    "Ron Weasley": "Gryffindor",
    "Draco Malfoy": "Slytherin",
}

students.keys()
students.values()

print(students["Harry Potter"])
print(students["Ron Weasley"])
print(students["Draco Malfoy"])

students.items()


for student in students:
    print(student)

students = [
    {"name": "Harry Potter", "house": "Gryffindor", "Hair Color": "Black"},
    {"name": "Ron Weasley", "house": "Gryffindor", "Hair Color": "Brown"},
    {"name": "Draco Malfoy", "house": "Slytherin", "Hair Color": "Blond"},
]

for student in students:
    print(student["name"], student["house"], student["Hair Color"], sep=", ")


###字典中的key
{0:0,2:0}
{(1,1):1,(1,2):1}
{[1,1]:1,[1,2]:1} #not valid
{{1,1}:1,{1,2}:1} #not valid


