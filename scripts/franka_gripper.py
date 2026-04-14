import numpy as np
from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

from omni.isaac.core import World
from isaacsim.core.prims import SingleArticulation
from isaacsim.core.utils.types import ArticulationAction
from pxr import UsdLux


FRANKA_USD_PATH = (
    "https://omniverse-content-production.s3-us-west-2.amazonaws.com/"
    "Assets/Isaac/5.1/Isaac/Robots/FrankaRobotics/FrankaPanda/franka.usd"
)


world = World()
world.scene.add_default_ground_plane()
stage = world.stage
stage.DefinePrim("/World/franka", "Xform").GetReferences().AddReference(FRANKA_USD_PATH)

light = UsdLux.DistantLight.Define(stage, "/World/defaultLight")
light.CreateIntensityAttr(3000)

world.reset()

franka = SingleArticulation(prim_path="/World/franka", name="franka")
franka.initialize()

finger_indices = np.array(
    [
        franka.get_dof_index("panda_finger_joint1"),
        franka.get_dof_index("panda_finger_joint2"),
    ]
)

print(f"Finger joint indices = {finger_indices}")

for _ in range(120):
    world.step(render=True)

open_action = ArticulationAction(
    joint_positions=np.array([0.04, 0.04]),
    joint_indices=finger_indices,
)
franka.apply_action(open_action)
print("Applied open gripper action -> [0.04, 0.04]")

for _ in range(240):
    world.step(render=True)

close_action = ArticulationAction(
    joint_positions=np.array([0.0, 0.0]),
    joint_indices=finger_indices,
)
franka.apply_action(close_action)
print("Applied close gripper action -> [0.0, 0.0]")

for _ in range(240):
    world.step(render=True)

current_positions = franka.get_joint_positions(joint_indices=finger_indices)
print("Current finger positions:")
print(current_positions)
print("Close the window manually when you finish looking.")

for _ in range(10000):
    world.step(render=True)

simulation_app.close()
