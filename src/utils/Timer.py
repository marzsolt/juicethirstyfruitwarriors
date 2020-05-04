class Timer:
    """" Timer that executes a function in a clock signal count delayed ticks.
        Needs setup i.e. giving a clock signal by calling its update function periodically. """
    sch_list = []
    
    @staticmethod
    def sch_fun(delay, fun, arg):
        """" Schedule a function. """
        Timer.sch_list.append((delay, fun, arg))  # arg: arguments of function, (): None, (a, b,):

    @staticmethod
    def update():
        """" The de-facto clock signaling of the timer """
        expired = []
        for i, sch in enumerate(Timer.sch_list):
            if sch[0] == 0:
                sch[1](*sch[2])
                expired.append(i)

        Timer.sch_list = [
            (sch[0] - 1, sch[1], sch[2])
            for i, sch in enumerate(Timer.sch_list) if i not in expired
        ]
