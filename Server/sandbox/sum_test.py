class A:
    def m(self):
        print("m of A called")


class B(A):
    def m(self):
        print("m of B called")
        A.m(self)


class C(A):
    def m(self):
        print("m of C called")
        A.m(self)


class D(B, C):
    def m(self):
        print("m of D called")
        B.m(self)
        C.m(self)

d = D()
d.m()

