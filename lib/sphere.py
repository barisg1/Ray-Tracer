from lib.vector import Vector3f
from lib.AABB import AABB

class Sphere():
    def __init__(self, radius, color, pos):
        self.radius = radius
        self.color = color
        self.position = pos

    def normal_at(self, point):
        return (point - self.position).normalize()
    
    def intersect(self, ray):
        oc = ray.origin - self.position
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return -1
        else:
            return (-b - discriminant ** 0.5) / (2.0 * a)
        
    def bounding_box(self):
        radius = Vector3f(self.radius, self.radius, self.radius)
        min_point = self.position - radius
        max_point = self.position + radius
        return AABB(min_point, max_point)