### 01：如果出现错误，则。。。
try:
    1/0
except:
    print("Wrong")

# ### 02：打出具体错误
# try:
#     1/0
# except Exception as e:
#     print(e)
#
# ### 03： 指定特定的错误
# try:
#     1/0
# except ZeroDivisionError:
#     print('Wrong')
#
# ### 04：需要正确的Error class
# try:
#     1/0
# except ValueError:
#     print("ValueError")
#
# ### 05：如果出现错误，则退出程序
# try:
#     1/0
# except:
#     print("Exit Before")
#     exit()
#     print("Exit After")
#
# ### 06: 不会识别syntax error
# try:
#     print("Hello, world)
# except:
#     print('Wrong')