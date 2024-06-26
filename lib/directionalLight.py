class DirectionalLight:
    def __init__(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction.normalize()

    def set_direction(self, direction):
        self.direction = direction