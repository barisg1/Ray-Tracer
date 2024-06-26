class Object:
    def __init__(self, color):
        self.color = color

    def normal_at(self, point):
        raise NotImplementedError("Subclasses must implement normal_at method")

    def intersect(self, ray):
        raise NotImplementedError("Subclasses must implement intersect method")
