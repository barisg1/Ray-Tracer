class objParser:
    def __init__(self, obj):
        self.objects = []
        if not obj:
            return

        with open(obj, 'r') as file:
            lines = file.readlines()

        vertices = []
        faces = []
        objName = None

        for line in lines:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == 'v':
                vertices.append(list(map(float, parts[1:])))
            elif parts[0] == 'f':
                face = [int(v.split('/')[0]) - 1 for v in parts[1:]]
                faces.append(face)
            elif parts[0] == 'g':
                if vertices and faces:
                    self.objects.append((vertices, faces, objName))
                    vertices = []
                    faces = []
                objName = parts[1] if len(parts) > 1 else None

        if vertices and faces:
            self.objects.append((vertices, faces, objName))