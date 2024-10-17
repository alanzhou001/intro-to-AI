### original
with open("new_txt.txt", "w") as file:
    file.write("some text\n")
    file.write("some text 2\n")

with open("new_txt.txt", "r") as file:
    lines = file.readlines()

lines

### pandas
import pandas as pd
df=pd.DataFrame([{'Name':'Lulu','Major':'AI'},
                 {'Name':'Alex','Major':'AI'}])
df.to_csv('some.csv')

df1=pd.read_csv('some.csv')
df1