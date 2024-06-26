class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()

    def hit_point(self, t):
        return self.origin + t * self.direction
