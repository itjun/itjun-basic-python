# 交换两个输入的数据
var1 = input("请输入第一个字符串")
print(var1)
var2 = input("请输入第二个字符串")
print(var2)

var3 = var1
var1 = var2
var2 = var3
print("输入数据交换完成后")

print(var1)
print(var2)
