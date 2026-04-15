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

target_position = target_cube.get_world_pose()[0]
print(f"Target cube world position = {target_position}")
print(f"IK end effector frame = {ik_solver.get_end_effector_frame()}")

ik_action, success = ik_solver.compute_inverse_kinematics(
    target_position=target_position,
    position_tolerance=0.01,
)

print(f"IK success = {success}")
print(f"IK action = {ik_action}")

if success:
    franka.apply_action(ik_action)
    for _ in range(400):
        world.step(render=True)

    joint_positions = franka.get_joint_positions()
    print("Applied joint positions:")
    print(joint_positions)
else:
    print("IK did not converge.")

print("Close the window manually when you finish looking.")

for _ in range(10000):
    world.step(render=True)

simulation_app.close()
