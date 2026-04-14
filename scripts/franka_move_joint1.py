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

joint1_index = franka.get_dof_index("panda_joint1")
print(f"panda_joint1 index = {joint1_index}")

for _ in range(120):
    world.step(render=True)

action = ArticulationAction(
    joint_positions=np.array([0.8]),
    joint_indices=np.array([joint1_index]),
)
franka.apply_action(action)

print("Applied target: panda_joint1 -> 0.8 rad")

for _ in range(300):
    world.step(render=True)

joint_positions = franka.get_joint_positions()
print(f"Current panda_joint1 position = {joint_positions[joint1_index]}")
print("Close the window manually when you finish looking.")

for _ in range(10000):
    world.step(render=True)

simulation_app.close()
