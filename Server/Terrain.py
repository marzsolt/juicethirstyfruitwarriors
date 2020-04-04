import random as ra


class Terrain:
    def __init__(self):
        self.screen_width = 800  # let screen width 800 pixels
        self.base_level = 200
        self.min_level = 50
        self.max_abs_slope = 15
        self.no_slope_base_p = 0.45

        ra.seed()  # initializing the pseudo-random generator
        self.points = [0, self.screen_width]
        self.slopes = []

        self.regenerate_terrain() # initial terrain generation

    def regenerate_terrain(self):
        # generating the points for the piecewise linear terrain
        for i in range(int(self.screen_width/100)): # how many middle points shall be generated
            [a, b] = self._get_longest_interval_of_points()
            self.points.append(ra.randint(a+1, b+1))
            self.points.sort()

            self._slope_rand_gen_and_append() # for the last - 1 sections
        self._slope_rand_gen_and_append() # for the last section


        #  TODO: implement Bresenham's line algorithm


        print(self.points, '\n', self.slopes)

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


terr = Terrain()

