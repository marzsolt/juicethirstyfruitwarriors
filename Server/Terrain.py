import random as ra
import math as mat
import bresenham as br


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BASE_LEVEL = 120
MIN_LEVEL = 50

MAX_ABS_ANGLE = 15
NO_ANGLE_BASE_P = 0.45


class Terrain:
    def __init__(self):
        self.__screen_width = SCREEN_WIDTH
        self.__screen_height = SCREEN_HEIGHT

        self.__base_level = BASE_LEVEL
        self.__min_level = MIN_LEVEL

        self.__max_abs_slope = MIN_LEVEL
        self.__no_slope_base_p = NO_ANGLE_BASE_P

        ra.seed()  # initializing the pseudo-random generator
        self.__points = [0, self.__screen_width - 1]
        self.__angles = []
        self.__levels = [self.__base_level, ]

        self.regenerate_terrain()  # initial terrain generation

    def regenerate_terrain(self):
        # generating the points for the piecewise linear terrain
        for useless in range(int(self.__screen_width/100)):  # how many middle points shall be generated
            [a, b] = self.__get_longest_interval_of_points()
            self.__points.append(ra.randint(a+1, b-1))
            self.__points.sort()

        #  generating the angle values for the piecewise linear sections and the levels at points (section ends)
        prev_point = 0
        for point in self.__points[1:]:
            self.__angle_rand_gen_and_append()
            y_point = max(
                mat.tan(mat.radians(self.__angles[-1])) * (point - prev_point) + self.__levels[prev_point],
                self.__min_level
            )

            br_line = list(br.bresenham(prev_point, self.__levels[prev_point], point, y_point))  # list of tuples (x, y)
            br_line = [p[1] for p in br_line]
            self.__levels.pop()
            self.__levels.extend(br_line)
            prev_point = point

    def __get_longest_interval_of_points(self):
        max_len = 0
        a = None
        b = None
        for intervals in range(len(self.__points) - 1):  # always insert a random point into the longest interval
            curr_diff = self.__points[intervals + 1] - self.__points[intervals]
            if max_len < curr_diff:
                max_len = curr_diff
                a = self.__points[intervals]
                b = self.__points[intervals + 1]

        return a, b

    def __angle_rand_gen_and_append(self):
        p_gen = ra.random()
        if p_gen <= self.__no_slope_base_p:
            self.__angles.append(0)
        else:
            self.__angles.append(ra.randint(-self.__max_abs_slope, self.__max_abs_slope))

    def get_angle(self, x):
        for i in range(1, len(self.__points)):
            if x <= self.__points[i]:
                return self.__angles[i - 1]

    def get_level(self, x):
        return self.__levels[round(x)]

    def get_terrain_levels(self):
        return self.__levels

    def get_terrain_points(self):
        return self.__points

    def get_terrain_angles(self):
        return self.__angles
