### If else
x = int(input("What's x? "))
y = int(input("What's y? "))

if x < y:
    print("x is less than y")
elif x > y:
    print("x is greater than y")
elif x == y:
    print("x is equal to y")

# ###match
# x=3
# y=4
#
# match x+y:
#     case 7:
#         print('correct')
#     case _:
#         print('wrong')