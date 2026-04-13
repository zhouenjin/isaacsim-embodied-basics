import numpy as np
from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

from omni.isaac.core import World
from omni.isaac.core.objects import VisualCuboid
from omni.isaac.core.utils.prims import get_prim_at_path
from pxr import PhysxSchema, UsdPhysics

world = World()
world.scene.add_default_ground_plane()

world.scene.add(
    VisualCuboid(
        prim_path="/World/cube1",
        name="cube1",
        position=np.array([0.0, 0.0, 1.0]),
        scale=np.array([0.5, 0.5, 0.5]),
        color=np.array([1.0, 0.0, 0.0]),
    )
)

cube1_prim = get_prim_at_path("/World/cube1")

UsdPhysics.RigidBodyAPI.Apply(cube1_prim)
rigid_body_schema = PhysxSchema.PhysxRigidBodyAPI.Apply(cube1_prim)
rigid_body_schema.CreateDisableGravityAttr().Set(True)

print("RigidBodyAPI applied to /World/cube1")
print("PhysxRigidBodyAPI applied to /World/cube1")
print("DisableGravity = True")

for _ in range(10000):
    world.step(render=True)

simulation_app.close()
