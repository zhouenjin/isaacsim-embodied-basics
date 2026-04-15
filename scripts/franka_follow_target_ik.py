import math
import numpy as np
from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

from omni.isaac.core import World
from omni.isaac.core.objects import VisualCuboid
from isaacsim.core.prims import SingleArticulation
from isaacsim.robot.manipulators.examples.franka.kinematics_solver import KinematicsSolver
from pxr import UsdLux


FRANKA_USD_PATH = (
    "https://omniverse-content-production.s3-us-west-2.amazonaws.com/"
    "Assets/Isaac/5.1/Isaac/Robots/FrankaRobotics/FrankaPanda/franka.usd"
)


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
        position=np.array([0.45, 0.0, 0.35]),
        scale=np.array([0.05, 0.05, 0.05]),
        color=np.array([1.0, 0.0, 0.0]),
    )
)

world.reset()

franka = SingleArticulation(prim_path="/World/franka", name="franka")
franka.initialize()

ik_solver = KinematicsSolver(franka)

# Keep the gripper pointing in a grasp-like downward pose.
target_orientation = np.array([0.0, 1.0, 0.0, 0.0])

center = np.array([0.45, 0.0, 0.35])
radius_y = 0.12
radius_z = 0.06

for step in range(900):
    t = step / 60.0

    moving_target_position = np.array(
        [
            center[0],
            center[1] + radius_y * math.sin(t),
            center[2] + radius_z * math.cos(t),
        ]
    )

    target_cube.set_world_pose(position=moving_target_position)

    ik_action, success = ik_solver.compute_inverse_kinematics(
        target_position=moving_target_position,
        target_orientation=target_orientation,
        position_tolerance=0.01,
        orientation_tolerance=0.1,
    )

    if success:
        franka.apply_action(ik_action)

    if step % 120 == 0:
        print(f"\nstep = {step}")
        print(f"moving_target_position = {moving_target_position}")
        print(f"ik success = {success}")

    world.step(render=True)

print("Close the window manually when you finish looking.")

for _ in range(10000):
    world.step(render=True)

simulation_app.close()
