from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

from omni.isaac.core import World
from isaacsim.core.prims import SingleArticulation
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

joint_names = franka.dof_names

print("Franka controllable joints:")
for i, name in enumerate(joint_names):
    print(f"{i}: {name}")

print(f"Total joint count = {len(joint_names)}")
print("Close the window manually when you finish looking.")

for _ in range(10000):
    world.step(render=True)

simulation_app.close()
