from Vector2D import Vector2D
import math

a = [1, 2, 3]
b = list(filter(lambda x: x < 2, a))
a.remove(b)
print(a, b)

