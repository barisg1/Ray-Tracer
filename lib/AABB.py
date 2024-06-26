from lib.vector import Vector3f

class AABB:
    def __init__(self, min_point, max_point):
        self.min_point = min_point
        self.max_point = max_point

    def from_objects(objects):
        min_point = Vector3f(float('inf'), float('inf'), float('inf'))
        max_point = Vector3f(float('-inf'), float('-inf'), float('-inf'))

        for obj in objects:
            obj_bbox = obj.bounding_box()
            min_point = Vector3f(min(min_point.x, obj_bbox.min_point.x), min(min_point.y, obj_bbox.min_point.y), min(min_point.z, obj_bbox.min_point.z))
            max_point = Vector3f(max(max_point.x, obj_bbox.max_point.x), max(max_point.y, obj_bbox.max_point.y), max(max_point.z, obj_bbox.max_point.z))

        return AABB(min_point, max_point)

    def intersect(self, ray):
        tmin = (self.min_point.x - ray.origin.x) / ray.direction.x
        tmax = (self.max_point.x - ray.origin.x) / ray.direction.x
        if tmin > tmax: 
            tmin, tmax = tmax, tmin

        tymin = (self.min_point.y - ray.origin.y) / ray.direction.y
        tymax = (self.max_point.y - ray.origin.y) / ray.direction.y
        if tymin > tymax: tymin, tymax = tymax, tymin

        if (tmin > tymax) or (tymin > tmax):
            return False

        if tymin > tmin:
            tmin = tymin
        if tymax < tmax:
            tmax = tymax

        tzmin = (self.min_point.z - ray.origin.z) / ray.direction.z
        tzmax = (self.max_point.z - ray.origin.z) / ray.direction.z
        if tzmin > tzmax: tzmin, tzmax = tzmax, tzmin

        if (tmin > tzmax) or (tzmin > tmax):
            return False

        if tzmin > tmin:
            tmin = tzmin
        if tzmax < tmax:
            tmax = tzmax

        return tmax >= max(tmin, 0.0)

    def center(self):
        return (self.min_point + self.max_point) * 0.5

    def longest_axis(self):
        extents = self.max_point - self.min_point
        if extents.x > extents.y and extents.x > extents.z:
            return 0
        elif extents.y > extents.z:
            return 1
        else:
            return 2
