import numpy as np
from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

from omni.isaac.core import World
from omni.isaac.core.prims import XFormPrim
from omni.isaac.core.utils.stage import add_reference_to_stage

world = World()

asset_path = r"D:\isaac\scenes\drop_cube.usd"
prim_path = "/World/loaded_scene"

add_reference_to_stage(usd_path=asset_path, prim_path=prim_path)

loaded_scene = XFormPrim(
    prim_path=prim_path,
    name="loaded_scene",
    translation=np.array([1.5, 0.0, 0.0]),
    orientation=np.array([1.0, 0.0, 0.0, 0.0]),
    scale=np.array([1.0, 1.0, 1.0]),
)

print("Loaded USD:", asset_path)
print("Mounted at prim path:", prim_path)

world.reset()

cube = XFormPrim("/World/loaded_scene/Cube", name="cube_in_loaded_scene")

cube_world_position, cube_world_orientation = cube.get_world_pose()
cube_local_position, cube_local_orientation = cube.get_local_pose()

print("Cube world position =", cube_world_position)
print("Cube world orientation =", cube_world_orientation)
print("Cube local position =", cube_local_position)
print("Cube local orientation =", cube_local_orientation)


position, orientation = loaded_scene.get_world_pose()
print("Before move, world position =", position)
print("Before move, world orientation =", orientation)

position[2] += 2.0
loaded_scene.set_world_pose(position=position, orientation=orientation)

new_position, new_orientation = loaded_scene.get_world_pose()
print("After move, world position =", new_position)
print("After move, world orientation =", new_orientation)

print("Close the window manually when you finish looking.")

while simulation_app.is_running():
    world.step(render=True)

