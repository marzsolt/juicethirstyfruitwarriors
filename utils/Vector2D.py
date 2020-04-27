import math
import cmath


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def mag_ang_init(cls, mag, ang_rad):  # second "constructor" usage: Vector2D.mag_ang_init(10, 3.1415)
        return cls(math.cos(ang_rad) * mag, math.sin(ang_rad) * mag)

    @classmethod
    def zero(cls):  # third "constructor" usage: Vector2D.zero()
        return cls(0, 0)

    def mag(self):
        return math.sqrt(self.x**2+self.y**2)

    def ang(self):
        return cmath.phase(complex(self.x, self.y))

    def domi_ang(self):
        if self.x < 0:
            if self.y < 0:
                return self.ang()+math.pi
            else:
                return self.ang()-math.pi
        return self.ang()

    '''Same magnitude, different angle'''
    def change_dir(self, new_angle_rad):
        m = self.mag()
        self.x = math.cos(new_angle_rad)*m
        self.y = math.sin(new_angle_rad)*m

    @staticmethod
    def sum(vectors):
        ret = Vector2D.zero()
        for v in vectors:
            ret += v
        return ret

    def __str__(self):
        return "(x: {0}, y: {1})".format(self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector2D(x, y)

    def scalar_div(self, scalar):
        self.x /= scalar
        self.y /= scalar
        return self

    def scalar_mult(self, scalar):
        self.x *= scalar
        self.y *= scalar
        return self

    def dot_product(self, other):
        return self.x*other.x + self.y*other.y
