import numpy as np
from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

from omni.isaac.core import World
from omni.isaac.core.objects import VisualCuboid
from isaacsim.core.prims import SingleArticulation
from isaacsim.core.utils.types import ArticulationAction
from pxr import UsdGeom, UsdLux


FRANKA_USD_PATH = (
    "https://omniverse-content-production.s3-us-west-2.amazonaws.com/"
    "Assets/Isaac/5.1/Isaac/Robots/FrankaRobotics/FrankaPanda/franka.usd"
)


def get_world_translation(stage, prim_path):
    prim = stage.GetPrimAtPath(prim_path)
    transform = UsdGeom.Xformable(prim)
    matrix = transform.ComputeLocalToWorldTransform(0)
    return np.array(matrix.ExtractTranslation())


world = World()
world.scene.add_default_ground_plane()
stage = world.stage

light = UsdLux.DistantLight.Define(stage, "/World/defaultLight")
light.CreateIntensityAttr(3000)

stage.DefinePrim("/World/franka", "Xform").GetReferences().AddReference(FRANKA_USD_PATH)

target_cube = world.scene.add(
    VisualCuboid(
        prim_path="/World/target_cube",
        name="target_cube",
        position=np.array([0.35, 0.0, 0.25]),
        scale=np.array([0.05, 0.05, 0.05]),
        color=np.array([1.0, 0.0, 0.0]),
    )
)

world.reset()

franka = SingleArticulation(prim_path="/World/franka", name="franka")
franka.initialize()

target_positions = np.array([0.0, -0.8, 0.0, -2.0, 0.0, 2.2, 0.8, 0.04, 0.04])
franka.apply_action(ArticulationAction(joint_positions=target_positions))

for _ in range(400):
    world.step(render=True)

tool_center_position = get_world_translation(stage, "/World/franka/panda_hand/tool_center")
target_position = target_cube.get_world_pose()[0]

vector_to_target = target_position - tool_center_position
distance_to_target = np.linalg.norm(vector_to_target)

print(f"Tool center world position = {tool_center_position}")
print(f"Target cube world position = {target_position}")
print(f"Vector from tool_center to target = {vector_to_target}")
print(f"Distance from tool_center to target = {distance_to_target}")
print("Close the window manually when you finish looking.")

for _ in range(10000):
    world.step(render=True)

simulation_app.close()
