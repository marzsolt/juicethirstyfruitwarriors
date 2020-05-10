import random as ra
import math as mat
import bresenham as br

from src.utils.Vector2D import Vector2D
from src.utils.general_constants import SCREEN_WIDTH


class Terrain:
    """" Class for building terrain for the game. """

    BASE_LEVEL = 120
    MIN_LEVEL = 50

    MAX_ABS_ANGLE = 25
    ZERO_ANGLE_BASE_PROB = 0.25

    def __init__(self):
        ra.seed()  # initializing the pseudo-random generator
        self.__points = [0, SCREEN_WIDTH - 1]
        self.__angles = []
        self.__levels = [self.BASE_LEVEL, ]

        self.generate_terrain()  # initial terrain generation

    def generate_terrain(self):
        """" Function responsible for generating the terrain. """
        # generating the points for the piecewise linear terrain
        for _ in range(int(SCREEN_WIDTH/100)):  # how many middle points shall be generated
            # always insert a random point into the longest interval
            [a, b] = self.__get_longest_interval_of_points()
            # self.__points.append(ra.randint(a+1, b-1))  # - previously done randomly
            self.__points.append(int((a + b) / 2))  # always divide at middle, for longer parts
            self.__points.sort()

        #  generating the angle values for the piecewise linear sections and the levels at points (section ends)
        prev_point = 0
        for point in self.__points[1:]:
            self.__angle_rand_gen_and_append()

            angle_in_radians = mat.radians(self.__angles[-1])
            y_prev_point = self.__levels[prev_point]
            y_point = max(  # correction: don't go below min level.
                mat.tan(angle_in_radians) * (point - prev_point) + y_prev_point,
                self.MIN_LEVEL
            )
            # recalculate angle as it's altered (in case correction done, as angles were initially randomly gen.)
            if y_point == self.MIN_LEVEL:
                self.__angles[-1] = mat.atan(mat.degrees((y_point - y_prev_point) / (point - prev_point)))

            # get line points with a discrete line point generator algorithm (pyGame uses the same on client side)
            br_line = list(br.bresenham(prev_point, self.__levels[prev_point], point, y_point))  # list of tuples (x, y)
            br_line = [p[1] for p in br_line]
            self.__levels.pop()
            self.__levels.extend(br_line)
            prev_point = point

    def __get_longest_interval_of_points(self):
        """" Helper function, returns the points that constitute the longest interval. """
        max_len = 0
        a = None
        b = None
        for intervals in range(len(self.__points) - 1):
            curr_diff = self.__points[intervals + 1] - self.__points[intervals]
            if max_len < curr_diff:
                max_len = curr_diff
                a = self.__points[intervals]
                b = self.__points[intervals + 1]

        return a, b

    def __angle_rand_gen_and_append(self):
        """ Helper function, randomly generates angle and appends. """
        p_gen = ra.random()
        if p_gen <= self.ZERO_ANGLE_BASE_PROB:
            self.__angles.append(0)
        else:
            self.__angles.append(ra.randint(-self.MAX_ABS_ANGLE, self.MAX_ABS_ANGLE))

    def get_angle_deg(self, x):
        """" Gets the angle in degrees at point x. """
        for i in range(1, len(self.__points)):
            if x <= self.__points[i]:
                return self.__angles[i - 1]

    def get_angle_rad(self, x):
        """" Gets the angle in radians at point x. """
        for i in range(1, len(self.__points)):
            if x <= self.__points[i]:
                return mat.radians(self.__angles[i - 1])

    def get_level(self, x):
        """" Get level (y) at point x. """
        return self.__levels[round(x)]

    def slope_grad(self, x):
        """" Get slope gradient at point x. """
        return Vector2D.mag_ang_init(1, self.get_angle_rad(x))

    def get_terrain_levels(self):
        """" Gets levels (y). """
        return self.__levels

    def get_terrain_points(self):
        """ Gets point (x). """
        return self.__points

    def get_terrain_angles(self):
        """" Gets angles (in degrees) """
        return self.__angles
