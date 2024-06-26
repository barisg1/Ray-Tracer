from math import pi, sin, cos, sqrt, acos

__all__ = ['HCoord', 'Vector3f', 'Point3f', 'ColorRGBA']


class HCoord:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def toArray(self):
        return [self.x, self.y, self.z, self.w]

    def sqrlen(self):
        return 1.0 * self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w

    def len(self):
        return sqrt(self.sqrlen())

    def dot(self, other):
        return 1.0 * other.x * self.x + other.y * self.y + other.z * self.z + other.w * self.w

    def cross(self, other):
        return HCoord(self.y * other.z - self.z * other.y, \
                      self.z * other.x - self.x * other.z, \
                      self.x * other.y - self.y * other.x, \
                      self.w)

    def subtract(self, other):
        return HCoord(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def cosa(self, other):
        # return self.dot(other) / (self.len() * other.len())
        return min(max(self.dot(other) / (self.len() * other.len()), 0.0), 1.0)

    def angle(self, other):
        return acos(self.cosa(other))

    def normalize(self):
        l = self.len()
        if l == 0:
            return self
        return HCoord(self.x / l, self.y / l, self.z / l, self.w / l)

    def project(self, other):
        return other.unit() * (self.len() * self.cosa(other))

    def middlePoint(self, other):
        return HCoord((self.x + other.x) / 2, (self.y + other.y)/2, (self.z + other.z)/2, self.w)

    def S(self, scalar):
        return self * scalar

    def __add__(self, other):
        x = 1.0 * self.x + other.x
        y = 1.0 * self.y + other.y
        z = 1.0 * self.z + other.z
        w = 1.0 * self.w + other.w
        return HCoord(x, y, z, w)

    def __sub__(self, other):
        return self + (-1 * other)

    def __div__(self, scalar):
        if (scalar == 0):
            return self
        else:
            return HCoord(self.x / scalar, self.y / scalar, self.z / scalar, self.w / scalar)

    def __mul__(self, scalar):
        return HCoord(scalar * self.x, scalar * self.y, scalar * self.z, self.w * scalar)

    def __rmul__(self, scalar):
        return HCoord(scalar * self.x, scalar * self.y, scalar * self.z, self.w * scalar)

    def __str__(self):
        return "(" + str(self.x) + " " + str(self.y) + " " + str(self.z) + " " + str(self.w) + ")"

    def __repr__(self):
        return self.__str__()


class Vector3f(HCoord):
    def __init__(self, x, y, z):
        HCoord.__init__(self, x, y, z, 0)


class Point3f(HCoord):
    def __init__(self, x, y, z):
        HCoord.__init__(self, x, y, z, 1.0)

    def __sub__(self, other):
        if isinstance(other, HCoord):
            return Vector3f(self.x - other.x,
                            self.y - other.y,
                            self.z - other.z)
        else:
            return Vector3f(self.x - other,
                            self.y - other,
                            self.z - other)

    def __add__(self, other):
        return Point3f(self.x + other.x, \
                       self.y + other.y, \
                       self.z + other.z)


class ColorRGBA(HCoord):
    def __init__(self, r, g, b, a):
        HCoord.__init__(self, r, g, b, a)
        self.r = self.x
        self.g = self.y
        self.b = self.z
        self.a = self.w
