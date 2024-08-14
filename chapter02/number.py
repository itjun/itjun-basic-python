import sys

print(6 / 3)
print(3 // 6)
print(2 ** 3)
print(pow(2, 3))
print(int(12.345))

value = str(123.456)
print(value)
print(type(value))

try:
    var1 = int(input("input first number:"))
    var2 = int(input("input second number:"))
except ValueError:
    print("错误：请输入整数作为计算参数")
    sys.exit(1)
print(var1 + var2)

print("1234" > "456")

print(len("456") > len("1234"))

#  变量 pi 用于计算圆的面积
pi = 3.14


def compute(num1, op, num2):
    return eval(f"{num1}{op}{num2}")


print(compute(3, "+", 5))
