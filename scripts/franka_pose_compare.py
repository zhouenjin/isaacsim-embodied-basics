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


def evaluate_pose(world, franka, stage, joint_positions, label, settle_steps=300):
    franka.apply_action(ArticulationAction(joint_positions=joint_positions))
    for _ in range(settle_steps):
        world.step(render=True)

    tool_center_position = get_world_translation(stage, "/World/franka/panda_hand/tool_center")
    return tool_center_position


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

pose_a = np.array([0.0, -0.8, 0.0, -2.0, 0.0, 2.2, 0.8, 0.04, 0.04])
pose_b = np.array([0.3, -0.5, 0.2, -2.2, 0.2, 2.0, 1.0, 0.04, 0.04])

target_position = target_cube.get_world_pose()[0]

tool_a = evaluate_pose(world, franka, stage, pose_a, "pose_a")
distance_a = np.linalg.norm(target_position - tool_a)

tool_b = evaluate_pose(world, franka, stage, pose_b, "pose_b")
distance_b = np.linalg.norm(target_position - tool_b)

print(f"Target cube world position = {target_position}")
print(f"Pose A tool_center = {tool_a}")
print(f"Pose A distance = {distance_a}")
print(f"Pose B tool_center = {tool_b}")
print(f"Pose B distance = {distance_b}")

if distance_a < distance_b:
    print("Pose A is closer to the target cube.")
else:
    print("Pose B is closer to the target cube.")

print("Close the window manually when you finish looking.")

for _ in range(10000):
    world.step(render=True)

simulation_app.close()
