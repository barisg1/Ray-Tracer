class BVHNode:
    def __init__(self, bbox, left=None, right=None, objects=None):
        self.bbox = bbox
        self.left = left
        self.right = right
        self.objects = objects

    def is_leaf(self):
        return self.objects is not None
