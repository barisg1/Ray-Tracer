from lib.object import Object
from lib.AABB import AABB
from lib.vector import Vector3f

class Triangle(Object):
    def __init__(self, v0, v1, v2, color):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.color = color

    def normal_at(self, point):
        edge1 = self.v1 - self.v0
        edge2 = self.v2 - self.v0
        return edge1.cross(edge2).normalize()

    def intersect(self, ray):
        edge1 = self.v1 - self.v0
        edge2 = self.v2 - self.v0
        h = ray.direction.cross(edge2)
        a = edge1.dot(h)
        if a == 0:
            return None
        f = 1.0 / a
        s = ray.origin - self.v0
        u = f * s.dot(h)
        if u < 0.0 or u > 1.0:
            return None
        q = s.cross(edge1)
        v = f * ray.direction.dot(q)
        if v < 0.0 or u + v > 1.0:
            return None
        t = f * edge2.dot(q)
        if t > 1e-6:
            return t
        else:
            return None
        
    def bounding_box(self):
        min_x = min(self.v0.x, self.v1.x, self.v2.x)
        max_x = max(self.v0.x, self.v1.x, self.v2.x)
        min_y = min(self.v0.y, self.v1.y, self.v2.y)
        max_y = max(self.v0.y, self.v1.y, self.v2.y)
        min_z = min(self.v0.z, self.v1.z, self.v2.z)
        max_z = max(self.v0.z, self.v1.z, self.v2.z)

        min_point = Vector3f(min_x, min_y, min_z)
        max_point = Vector3f(max_x, max_y, max_z)
        return AABB(min_point, max_point)