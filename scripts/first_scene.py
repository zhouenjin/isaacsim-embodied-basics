from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

import numpy as np
from omni.isaac.core import World
from omni.isaac.core.objects import DynamicCuboid

world = World(stage_units_in_meters=1.0)

world.scene.add_default_ground_plane()

world.scene.add(
    DynamicCuboid(
        prim_path="/World/my_cube",
        name="my_cube",
        position=[0.0, 0.0, 1.0],
        scale=[0.3, 0.3, 0.3],
        color=np.array([1.0, 0.2, 0.2]),
    )
)

world.reset()

for i in range(300):
    world.step(render=True)

print("Scene ran successfully. Close the window manually.")

while simulation_app.is_running():
    world.step(render=True)


