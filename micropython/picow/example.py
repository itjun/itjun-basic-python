import os

# 读取板载上的配置文件

def read_properties(lines, key, defValue):
    for line in lines:
        arr = line.split("=")
        key1 = arr[0]
        value = arr[1]
        if key1==key:
            return value.strip()
    return defValue

f = open('config.txt', 'r')
if f == None:
    print("config.txt not found")
lines = f.readlines()

print(read_properties(lines, 'd', '222'))

