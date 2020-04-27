class Timer:
    sch_list = []
    
    @staticmethod
    def sch_fun(delay, fun, arg):
        Timer.sch_list.append((delay, fun, arg))
        
    @staticmethod
    def update():
        expired = []
        for i, sch in enumerate(Timer.sch_list):
            if sch[0] == 0:
                sch[1](*sch[2])
                expired.append(i)

        Timer.sch_list = [
            (sch[0] - 1, sch[1], sch[2])
            for i, sch in enumerate(Timer.sch_list) if i not in expired
        ]
