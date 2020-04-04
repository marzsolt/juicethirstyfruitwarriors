import random as ra
import math as mat
import bresenham as br


class Terrain:
    def __init__(self):
        self.screen_width = 800  # let screen width 800 pixels
        self.screen_height = 600
        self.base_level = 120

        self.min_level = 50
        self.max_abs_slope = 15
        self.no_slope_base_p = 0.45

        ra.seed()  # initializing the pseudo-random generator
        self.points = [0, self.screen_width - 1]
        self.slopes = []
        self.levels = [self.base_level, ]

        self.regenerate_terrain() # initial terrain generation

    def regenerate_terrain(self):
        # generating the points for the piecewise linear terrain
        for discard in range(int(self.screen_width/100)): # how many middle points shall be generated
            [a, b] = self._get_longest_interval_of_points()
            self.points.append(ra.randint(a+1, b+1))
            self.points.sort()


        # generating the slope values for the piecewise linear sections and the levels at points (section ends).
        prev_point = 0
        for point in self.points[1:]:
            self._slope_rand_gen_and_append()
            y_point = max(
                mat.tan(mat.radians(self.slopes[-1])) * (point - prev_point) + self.levels[prev_point],
                self.min_level
            )

            br_line = list(br.bresenham(prev_point, self.levels[prev_point], point, y_point)) # list of tuples (x, y)
            br_line = [p[1] for p in br_line]
            self.levels.pop()
            self.levels.extend(br_line)
            prev_point = point

    def _get_longest_interval_of_points(self):
        max_len = 0
        a = None
        b = None
        for intervals in range(len(self.points) - 1):  # always insert a random point into the longest interval
            curr_diff = self.points[intervals + 1] - self.points[intervals]
            if max_len < curr_diff:
                max_len = curr_diff
                a = self.points[intervals]
                b = self.points[intervals + 1]

        return a, b

    def _slope_rand_gen_and_append(self):
        p_gen = ra.random()
        if p_gen <= self.no_slope_base_p:
            self.slopes.append(0)
        else:
            self.slopes.append(ra.randint(-self.max_abs_slope, self.max_abs_slope))

    def get_slope(self, p):
        for i in range(1, len(self.points)):
            if p <= self.points[i]:
                return self.slopes[i - 1]

    def get_level(self, p):
        return self.levels[p] # this could be accesed directly...

    def get_terrain_levels(self):
        return self.levels

    def get_terrain_points(self):
        return self.points

    def get_terrain_slopes(self):
        return self.slopes
