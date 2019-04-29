a = [1, 2, 3]
b = [4, 5, 6]

sum = lambda x, y: x + y

s = list(map(sum, a, b))
print(s)