import json
import random

class JsonParser():
    def __init__(self, json_file):
        self.renderSettings, self.spheres, self.camera, self.objPath, self.light = self.parse_json(json_file)

    def is_valid_json(self, file_path):
        try:
            with open(file_path, 'r') as f:
                json.load(f)
            return True
        except (ValueError, IOError) as e:
            return False

    def parse_json(self, json_file):
        if self.is_valid_json(json_file):
            with open(json_file, 'r') as f:
                scene_data = json.load(f)
        else:
            return None, None, None, None

        renderSettings = scene_data.get("renderSettings", {})
        camera = scene_data.get("camera", {})
        objPath = scene_data.get("objFile", {})
        light = scene_data.get("directionalLight", {})
        spheres = []
        if "spheres" in scene_data:
            spheres = (scene_data["spheres"])
        elif "proceduralSpheres" in scene_data:
            spheres = spheres + self.generate_procedural_spheres(scene_data["proceduralSpheres"])

        return renderSettings, spheres, camera, objPath, light

    def generate_procedural_spheres(self, procedural_spheres_data):
        spheres = []
        for sphere_data in procedural_spheres_data:
            upper_left = sphere_data["upperLeft"]
            bottom_right = sphere_data["bottomRight"]
            nof_spheres = sphere_data["nofSpheres"]
            radius_lo = sphere_data["radiusLo"]
            radius_hi = sphere_data["radiusHi"]

            for _ in range(nof_spheres):
                pos_x = random.uniform(upper_left["x"], bottom_right["x"])
                pos_y = random.uniform(upper_left["y"], bottom_right["y"])
                pos_z = random.uniform(upper_left["z"], bottom_right["z"])
                radius = random.uniform(radius_lo, radius_hi)
                color = {"r": random.randint(0, 255), "g": random.randint(0, 255), "b": random.randint(0, 255)}

                sphere = {
                    "radius": radius,
                    "posX": pos_x,
                    "posY": pos_y,
                    "posZ": pos_z,
                    "color": color
                }
                spheres.append(sphere)
        return spheres
