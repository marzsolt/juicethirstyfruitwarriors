class A:
    def __init__(self):
        print("-> A")
        super(A, self).__init__()
        print("<- A")

    def m(self):
        print("A m")

    def print(self):
        print("5")
        return 5

    def tick(self):
        self.print()


class B(A):
    def __init__(self):
        print("-> B")
        super(B, self).__init__()
        print("<- B")

    def m(self):
        print("B m")

    # def print(self):
    #     print("6")
    #     return 6


class C(A):
    def __init__(self):
        print("-> C")
        # Use super here, instead of explicit calls to __init__
        super(C, self).__init__()
        print("<- C")

    def m(self):
        print("C m")

    def print(self):
        print("7")
        return 7


class D(B, C):
    def __init__(self):
        print("-> D")
        # Use super here, instead of explicit calls to __init__
        super(D, self).__init__()
        print("<- D")

    def print(self):
        print("10")
        return print(super().print())


d = D()
d.m()
d.tick()

