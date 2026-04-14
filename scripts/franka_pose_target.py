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

target_positions = np.array([0.0, -0.8, 0.0, -2.0, 0.0, 2.2, 0.8, 0.04, 0.04])
action = ArticulationAction(joint_positions=target_positions)
franka.apply_action(action)

print("Applied full Franka target pose:")
print(target_positions)

for _ in range(400):
    world.step(render=True)

current_positions = franka.get_joint_positions()
print("Current joint positions:")
print(current_positions)
print("Close the window manually when you finish looking.")

for _ in range(10000):
    world.step(render=True)

simulation_app.close()
