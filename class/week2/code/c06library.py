###抓取命令行输入的内容
from sys import argv

print(argv[0])
print(argv[1])
print(argv[2])

# ###调用自己其他文件写好的包(同一个目录)
# import c05function
# print(c05function.add(argv[1],argv[2]))
#
# ###无法识别
# print(add(argv[1],argv[2]))
#
# ###可以识别
# from c05function import add
# print(add(argv[1],argv[2]))