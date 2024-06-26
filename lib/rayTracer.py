import multiprocessing
from PySide2.QtGui import *
from lib.vector import Vector3f
from lib.rayTracerTask import RayTracerTask
from lib import *

class RayTracer:
    def __init__(self, width, height, scene, num_processes):
        self.width = width
        self.height = height
        self.scene = scene
        self.objects = self.scene.spheres + self.scene.triangles
        self.camera = self.scene.camera
        self.colors = [object.color for object in self.objects]
        self.num_processes = num_processes

    def rayTrace(self):
        camera_pos = Vector3f(self.camera["posX"], self.camera["posY"], self.camera["posZ"]) 
        focal_length = self.camera["focalLength"]

        section_height = self.height // self.num_processes
        processes = []
        with multiprocessing.Pool(self.num_processes) as pool:
            for i in range(self.num_processes):
                start_y = i * section_height
                end_y = start_y + section_height
                processes.append(pool.apply_async(self.process_section, args=(0, self.width, start_y, end_y, self.width, self.height, camera_pos, focal_length, self.objects, self.colors, self.scene.light)))
            img_data_list = [p.get() for p in processes]

        img_data = bytearray()
        for data in img_data_list:
            for (x, y), color in data:
                img_data.extend(color)
        return img_data

    def process_section(self, start_x, end_x, start_y, end_y, width, height, camera_pos, focal_length, objects, colors, light):
        task = RayTracerTask(start_x, end_x, start_y, end_y, width, height, camera_pos, focal_length, objects, colors, light)
        return task.run()
    
    