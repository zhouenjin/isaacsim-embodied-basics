import numpy as np
from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

from omni.isaac.core import World
from omni.isaac.core.objects import DynamicCuboid
from omni.isaac.core.utils.prims import get_prim_at_path


world = World()
world.scene.add_default_ground_plane()

cube1 = world.scene.add(
    DynamicCuboid(
        prim_path="/World/cube1",
        name="cube1",
        position=np.array([0.0, 0.0, 1.0]),
        scale=np.array([0.5015, 0.5015, 0.5015]),
        color=np.array([0.0, 0.0, 1.0]),
    )
)

cube1_prim = get_prim_at_path("/World/cube1")

print("cube1.prim_path =", cube1.prim_path)
print("cube1_prim.GetPath() =", cube1_prim.GetPath())
print("cube1_prim.GetAppliedSchemas() =", cube1_prim.GetAppliedSchemas())
print(
    "cube1_prim.GetAttribute('physxRigidBody:maxLinearVelocity').Get() =",
    cube1_prim.GetAttribute("physxRigidBody:maxLinearVelocity").Get(),
)

world.reset()
for _ in range(10):
    world.step(render=True)

print("Close the window manually when you finish looking.")

while simulation_app.is_running():
    world.step(render=True)
