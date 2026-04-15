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


def apply_pose_and_wait(world, franka, joint_positions, steps=180):
    franka.apply_action(ArticulationAction(joint_positions=joint_positions))
    for _ in range(steps):
        world.step(render=True)


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
        position=np.array([0.42, 0.0, 0.32]),
        scale=np.array([0.05, 0.05, 0.05]),
        color=np.array([1.0, 0.0, 0.0]),
    )
)

world.reset()

franka = SingleArticulation(prim_path="/World/franka", name="franka")
franka.initialize()

joint_positions = np.array([0.0, -0.8, 0.0, -2.0, 0.0, 2.2, 0.8, 0.04, 0.04], dtype=float)
apply_pose_and_wait(world, franka, joint_positions)

target_position = target_cube.get_world_pose()[0]
print(f"Target cube world position = {target_position}")

for iteration in range(8):
    tool_position = get_world_translation(stage, "/World/franka/panda_hand/tool_center")
    vector = target_position - tool_position
    distance = np.linalg.norm(vector)

    print(f"\nIteration {iteration}")
    print(f"tool_center = {tool_position}")
    print(f"vector_to_target = {vector}")
    print(f"distance = {distance}")

    # Very crude heuristic controller:
    # joint1 roughly swings left/right based on target y
    # joint2/joint4/joint6 roughly change reach and height
    joint_positions[0] += 1.5 * vector[1]
    joint_positions[1] += -0.8 * vector[2]
    joint_positions[3] += 1.2 * vector[2]
    joint_positions[5] += -0.8 * vector[0]

    joint_positions[:7] = np.clip(
        joint_positions[:7],
        [-2.8, -1.7, -2.8, -3.0, -2.8, -0.01, -2.8],
        [2.8, 1.7, 2.8, -0.07, 2.8, 3.7, 2.8],
    )

    print(f"new_joint_positions = {joint_positions}")
    apply_pose_and_wait(world, franka, joint_positions, steps=120)

final_tool_position = get_world_translation(stage, "/World/franka/panda_hand/tool_center")
final_distance = np.linalg.norm(target_position - final_tool_position)

print("\nFinal result")
print(f"final tool_center = {final_tool_position}")
print(f"final distance = {final_distance}")
print("Close the window manually when you finish looking.")

for _ in range(10000):
    world.step(render=True)

simulation_app.close()
