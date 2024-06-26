from PySide2.QtGui import *
from lib.vector import Vector3f
from lib.ray import Ray
from lib.bvhNode import BVHNode
from lib import *

class RayTracerTask:
    def __init__(self, start_x, end_x, start_y, end_y, width, height, camera_pos, focal_length, objects, colors, light):
        self.start_x = start_x
        self.end_x = end_x
        self.start_y = start_y
        self.end_y = end_y
        self.width = width
        self.height = height
        self.camera_pos = camera_pos
        self.focal_length = focal_length
        self.objects = objects
        self.colors = colors
        self.directionalLight = light
        self.bvh_root = self.build_bvh(objects)

    def run(self, depth=3):
        result = []
        for y in range(self.start_y, self.end_y):
            for x in range(self.start_x, self.end_x):
                aspect_ratio = self.width / self.height
                u = aspect_ratio * ((x + 0.5) / self.width - 0.5)
                v = (y + 0.5) / self.height - 0.5
                direction = Vector3f(u, v, -self.focal_length)

                ray = Ray(self.camera_pos, direction)

                color = self.trace_ray(ray, depth)
                
                result.append(((x, y), color))

        return result

    def trace_ray(self, ray, depth):
        if depth <= 0:
            return (0, 0, 0)

        hit_info = self.intersect_bvh(self.bvh_root, ray)
        if hit_info is not None:
            hit_object, min_t = hit_info
            hit_point = ray.hit_point(min_t)
            normal = hit_object.normal_at(hit_point)
            normal = normal.normalize()
            light_dir = self.directionalLight.get_direction()
            light_intensity = max(0, normal.dot(light_dir))
            color = tuple(int(c * light_intensity) for c in hit_object.color)

            if depth > 0:
                reflection_dir = ray.direction - 2 * ray.direction.dot(normal) * normal
                reflection_ray = Ray(hit_point, reflection_dir)
                reflection_color = self.trace_ray(reflection_ray, depth - 1)
                reflection_intensity = 0.5
                color = tuple(int(c * (1 - reflection_intensity) + reflection_intensity * rc) for c, rc in zip(color, reflection_color))

        else:
            color = (0, 0, 0)

        return color

    def intersect_bvh(self, node, ray):
        if not node.bbox.intersect(ray):
            return None

        if node.is_leaf():
            min_t = float('inf')
            hit_object = None
            for obj in node.objects:
                t = obj.intersect(ray)
                if t is not None and t > 0 and t < min_t:
                    min_t = t
                    hit_object = obj
            return (hit_object, min_t) if hit_object else None

        hit_left = self.intersect_bvh(node.left, ray)
        hit_right = self.intersect_bvh(node.right, ray)

        if hit_left and hit_right:
            return hit_left if hit_left[1] < hit_right[1] else hit_right
        return hit_left if hit_left else hit_right

    
    def build_bvh(self, objects):
        if len(objects) <= 2:
            bbox = AABB.from_objects(objects)
            return BVHNode(bbox, objects=objects)

        bbox = AABB.from_objects(objects)
        axis = bbox.longest_axis()

        def sort_key(obj):
            center = obj.bounding_box().center()
            if axis == 0:
                return center.x
            elif axis == 1:
                return center.y
            else:
                return center.z
        
        objects.sort(key=sort_key)

        mid = len(objects) // 2
        left_child = self.build_bvh(objects[:mid])
        right_child = self.build_bvh(objects[mid:])

        return BVHNode(bbox, left_child, right_child)

