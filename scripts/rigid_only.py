import numpy as np
from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

from omni.isaac.core import World
from omni.isaac.core.objects import VisualCuboid
from omni.isaac.core.utils.prims import get_prim_at_path
from pxr import UsdPhysics

world = World()
world.scene.add_default_ground_plane()

cube1 = world.scene.add(
    VisualCuboid(
        prim_path="/World/cube1",
        name="cube1",
        position=np.array([0.0, 0.0, 1.0]),
        scale=np.array([0.5015, 0.5015, 0.5015]),
        color=np.array([0.0, 0.0, 1.0]),
    )
)

cube1_prim = get_prim_at_path("/World/cube1")
UsdPhysics.RigidBodyAPI.Apply(cube1_prim)

print("RigidBodyAPI applied to /World/cube1")
print("No collision added yet.")

for _ in range(10000):
    world.step(render=True)

simulation_app.close()
