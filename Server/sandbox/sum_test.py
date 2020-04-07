from Vector2D import Vector2D
import math

v1 = Vector2D(3, 4)
for i in range(100):
    v1.change_dir(i)
v1.change_dir(3.14)
v2 = Vector2D(4, 1)
v = [v1, v2]
print(Vector2D.sum(v))

v3 = Vector2D.mag_ang_init(2, 3.1415*1.5)
print(v3.ang())
v3 = Vector2D.mag_ang_init(2, 3.1415/2)
print(v3.ang())
v3 = Vector2D.mag_ang_init(2, -3.1415/4)
print(v3.ang())
v3 = Vector2D.mag_ang_init(2, -3.1415)
print(v3.ang())
v3 = Vector2D.mag_ang_init(2, 0)
print(v3.ang())
print(math.sin(25*3.14/180))