from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

import os

import numpy as np
from PIL import Image

from isaacsim.core.api import World
from isaacsim.core.api.objects import DynamicCuboid
from isaacsim.sensors.camera import Camera
import isaacsim.core.utils.numpy.rotations as rot_utils


OUTPUT_DIR = r"D:\isaac\outputs"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "camera_rgb.png")

os.makedirs(OUTPUT_DIR, exist_ok=True)

world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()

cube = world.scene.add(
    DynamicCuboid(
        prim_path="/World/my_cube",
        name="my_cube",
        position=np.array([0.0, 0.0, 0.15]),
        scale=np.array([0.3, 0.3, 0.3]),
        color=np.array([1.0, 0.2, 0.2]),
    )
)

camera = Camera(
    prim_path="/World/camera",
    position=np.array([0.0, 0.0, 5.0]),
    frequency=20,
    resolution=(640, 480),
    orientation=rot_utils.euler_angles_to_quats(np.array([0.0, 90.0, 0.0]), degrees=True),
)

world.reset()

cube_position, cube_orientation = cube.get_world_pose()
camera_position, camera_orientation = camera.get_world_pose()

print("Cube world position =", cube_position)
print("Cube world orientation =", cube_orientation)
print("Camera world position =", camera_position)
print("Camera world orientation =", camera_orientation)


camera.initialize()

saved_image = False

while simulation_app.is_running():
    world.step(render=True)

    if not saved_image and world.current_time_step_index > 30:
        rgba = camera.get_rgba()
        rgb = np.clip(rgba[:, :, :3], 0, 255).astype(np.uint8)
        Image.fromarray(rgb).save(OUTPUT_PATH)
        print(f"Saved camera image to: {OUTPUT_PATH}")
        saved_image = True
        break

simulation_app.close()
