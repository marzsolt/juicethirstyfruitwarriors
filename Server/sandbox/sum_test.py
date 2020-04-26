class A:
    def __init__(self):
        print("-> A")
        super(A, self).__init__()
        print("<- A")

    def m(self):
        print("A m")


class B(A):
    def __init__(self):
        print("-> B")
        super(B, self).__init__()
        print("<- B")

    def m(self):
        print("B m")


class C(A):
    def __init__(self):
        print("-> C")
        # Use super here, instead of explicit calls to __init__
        super(C, self).__init__()
        print("<- C")

    def m(self):
        print("C m")


class D(B, C):
    def __init__(self):
        print("-> D")
        # Use super here, instead of explicit calls to __init__
        super(D, self).__init__()
        print("<- D")


d = D()
d.m()

