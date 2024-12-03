import math

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector(self.x + other[0], self.y + other[1])
        else:
            raise TypeError("Unsupported operand type(s) for +: 'Vector' and '{}'".format(type(other).__name__))

        
    def sub(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector(self.x - other[0], self.y - other[1])
        else:
            raise TypeError("Unsupported operand type(s) for -: 'Vector' and '{}'".format(type(other).__name__))

    def mul(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x * other, self.y * other)
        else:
            raise TypeError("Unsupported operand type(s) for *: 'Vector' and '{}'".format(type(other).__name__))

    def div(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x / other, self.y / other)
        else:
            raise TypeError("Unsupported operand type(s) for /: 'Vector' and '{}'".format(type(other).__name__))

    def size(self):
        return math.sqrt((self.x**2) + (self.y**2))
    
    def normalize(self):
        sz = self.size()
        if sz == 0 : return Vector(0,0)
        else : return self / sz

    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def cross(self, other):
        return self.x * other.y - self.y * other.x

    # Operator Overloading
    def __add__(self, other):
        return self.add(other)
    def __radd__(self, other):
        return self.add(other)
    
    def __sub__(self, other):
        return self.sub(other)
    def __rsub__(self, other):
        return Vector(0, 0).sub(self).add(other)
    
    def __mul__(self, other):
        return self.mul(other)
    def __rmul__(self, other):
        return self.mul(other)
    
    def __truediv__(self, other):
        return self.div(other)

    def  __pos__(self):
        return Vector(self.x, self.y)
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index out of range")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = float(value)
        elif index == 1:
            self.y = float(value)
        else:
            raise IndexError("Index out of range")
        
    def __str__(self):
        return "Vector : ({}, {})".format(self.x, self.y)

