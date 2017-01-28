from math import hypot
from operator import add, mod, mul, sub, truediv

def apply(op):
    return lambda self, a: Vector(map(op, self, a if hasattr(a, '__iter__') else (a, a)))

class Vector:

    def __init__(self, coordinates=(0, 0)):
        self.coordinates = tuple(coordinates)

    @property
    def magnitude(self):
        return hypot(*self)

    __add__ = apply(add)
    __radd__ = __add__
    __sub__ = apply(sub)
    __mul__ = apply(mul)
    __truediv__ = apply(truediv)
    __mod__ = apply(mod)

    def __iter__(self):
        return iter(self.coordinates)

    def normalize(self):
        return self / self.magnitude if self.magnitude else self

    def limit(self, n):
        return self.normalize() * n if self.magnitude ** 2 > n ** 2 else self