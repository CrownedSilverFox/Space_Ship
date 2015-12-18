import math


class Vector:
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]

    def __str__(self):
        return '(%.2f, %.2f)' % (self.x, self.y)

    def __add__(self, other):
        return Vector((self.x + other.x, self.y + other.y))

    def __mul__(self, other):
        return Vector((self.x * other, self.y * other))

    def __sub__(self, other):
        return self + other * -1

    @property
    def len(self):
        return math.sqrt(self.x**2 + self.y**2)

    def rotate(self, angle):
        x = self.x
        y = self.y
        self.x = x*math.cos(math.radians(angle)) - y*math.sin(math.radians(angle))
        self.y = y*math.cos(math.radians(angle)) + x*math.sin(math.radians(angle))

    def as_point(self):
        return self.x, self.y

    def normal(self):
        return Vector((self.x/self.len, self.y/self.len))
