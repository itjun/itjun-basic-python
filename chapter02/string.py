# Hello Python
print("Hello Python")

# Hello Python
print('Hello Python')

# Hello "Python"
print('Hello "Python"')

"""
Hello
Python
"""
print('''
Hello
Python
''')

# 123 是变量 x 的值
x = 123
print(f"{x} 是变量 x 的值")

# True
print("xy" in "123xy456")

# False
print("x" not in "123xy456")

# abcxyz
print("abc" + "xyz")

# 拼接字符串
var1 = "abc"
var2 = "xyz"
print(var1 + var2)

# 字符串连续拼接3次
print(var1 * 3)
print(var1)
print(var2)

# 切片操作
print("切片操作演示")
string = "abcde"
print(string[0])
print(string[-1])
print(string[1:3])

# str.count(sub[, strart[,end]]) 返回字符串 sub 在 [start, end] 范围内出现的次数
# str.isalnum() 如果字符串中所有的字符都是字母或数字，且至少有一个字符，那么返回 True，否则返回 False，例如可用于判断用户的 e-mail
# str.isalpha() 如果字符串中所有的字符都是字母，且至少有一个字符，那么返回 True，否则返回 False

print((string * 3).count("a"))
print((string * 3).count("abc"))
print(string.isalnum())
print(string.isalpha())

print(",".join(string))
print("a,b,c,d,".split(","))
print("xyz".startswith("x"))
