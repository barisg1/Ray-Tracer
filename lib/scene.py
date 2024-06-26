from lib import *
from lib.vector import Vector3f
from lib.triangle import Triangle
from lib.sphere import Sphere

import random
import numpy as np

class Scene:
    def __init__(self, json_file = None):
        if not json_file:
            self.scene = JsonParser("scene3.json")
        else:
            self.scene = JsonParser(json_file)
        self.renderSettings = self.scene.renderSettings
        spheres = []
        for sphere in self.scene.spheres:
            s = Sphere(
                sphere["radius"], 
                (sphere["color"]["r"],sphere["color"]["g"],sphere["color"]["b"]), 
                Vector3f(sphere["posX"], sphere["posY"], sphere["posZ"]))
            spheres.append(s)
        self.obj = objParser(self.scene.objPath["path"])
        self.light = DirectionalLight(Vector3f(self.scene.light["posX"],self.scene.light["posY"],self.scene.light["posZ"]))

        self.spheres = spheres
        self.triangles = self.generate_triangles()
        
        rotation_x = Matrix.Rx(self.scene.objPath["RotX"])
        rotation_y = Matrix.Ry(self.scene.objPath["RotY"]) 
        rotation_z = Matrix.Rz(self.scene.objPath["RotZ"])

        scale = Matrix.S(self.scene.objPath["Scale"])
        translate = Matrix.T(
            self.scene.objPath["TranslateX"],
            self.scene.objPath["TranslateY"],
            self.scene.objPath["TranslateZ"]
        )

        transform_matrix = scale.product(rotation_x).product(rotation_y).product(rotation_z).product(translate)

        self.transform_triangles(transform_matrix)
        self.camera = self.scene.camera 

    def generate_triangles(self):
        triangles = []
        vertices = []
        faces = []
        for v, f, _ in self.obj.objects:
            vertices.extend(v)
            faces.extend(f)


        for face in faces:
            v0_index, v1_index, v2_index = face[:3]
            v0 = Vector3f(*vertices[v0_index])
            v1 = Vector3f(*vertices[v1_index])
            v2 = Vector3f(*vertices[v2_index])

            for i in range(2, len(face)):
                v1_index = face[i - 1]
                v2_index = face[i]
                v1 = Vector3f(*vertices[v1_index])
                v2 = Vector3f(*vertices[v2_index])
                triangles.append(Triangle(v0, v1, v2, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))))
        return triangles
    

    def transform_triangles(self, transform_matrix):
        for triangle in self.triangles:
            triangle.v0 = self.apply_transformation_to_vertex(triangle.v0, transform_matrix)
            triangle.v1 = self.apply_transformation_to_vertex(triangle.v1, transform_matrix)
            triangle.v2 = self.apply_transformation_to_vertex(triangle.v2, transform_matrix)

    def apply_transformation_to_vertex(self, vertex, transform_matrix):
        homogeneous_vertex = Vector3f(vertex.x, vertex.y, vertex.z)
        transform_homogeneous_vertex = transform_matrix.vecmul(homogeneous_vertex)
        return Vector3f(transform_homogeneous_vertex.x, transform_homogeneous_vertex.y, transform_homogeneous_vertex.z)