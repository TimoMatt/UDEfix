
class NotInMError(Exception):
    pass


class NaturalOrder:
    @staticmethod
    def lt(x, y):
        return x < y

    @staticmethod
    def le(x, y):
        return x <= y

    @staticmethod
    def eq(x, y):
        return x == y

    @staticmethod
    def neq(x, y):
        return x != y

    @staticmethod
    def gt(x, y):
        return x > y

    @staticmethod
    def gte(x, y):
        return x >= y


class MVAlgebra(NaturalOrder):
    def __init__(self, M, e):
        self.M = M
        self.e = e

    def complement(self, x):
        raise NotImplementedError()

    def addition(self, x, y):
        raise NotImplementedError()

    def multiplication(self, x, y):
        return self.complement(self.addition(self.complement(x), self.complement(y)))

    def subtraction(self, x, y):
        return self.multiplication(x, self.complement(y))

    # for average-function
    def multi(self, x, y):
        if self.M[0] <= x <= self.M[1] and self.M[0] <= y <= self.M[1]:
            return x * y
        else:
            raise NotInMError()

    def minimalValue(self, list):
        minimum = self.complement(self.e)
        for elem in list:
            if self.lt(elem, minimum):
                minimum = elem
        return minimum


class Algebra1(MVAlgebra):
    def __init__(self, k=1):
        self.k = k
        super().__init__((0, k), 0)

    def complement(self, x):
        if self.M[0] <= x <= self.M[1]:
            return self.M[1]-x
        else:
            raise NotInMError()

    def addition(self, x, y):
        if self.M[0] <= x <= self.M[1] and self.M[0] <= y <= self.M[1]:
            if x + y <= self.M[1]:
                return x + y
            else:
                return self.M[1]
        else:
            raise NotInMError()


class Algebra2(MVAlgebra):
    def __init__(self, k):
        self.k = k
        super().__init__(range(0, self.k+1), 0)

    def complement(self, x):
        if x in self.M:
            return self.k - x
        else:
            raise NotInMError()

    def addition(self, x, y):
        if x in self.M and y in self.M:
            if x + y <= self.k:
                return x + y
            else:
                return self.k
        else:
            raise NotInMError()
