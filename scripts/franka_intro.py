from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

import numpy as np
from omni.isaac.core import World
from omni.isaac.core.prims import XFormPrim
from omni.isaac.core.utils.stage import add_reference_to_stage

world = World()

asset_path = r"https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/5.1/Isaac/Robots/FrankaRobotics/FrankaPanda/franka.usd"
prim_path = "/World/franka"

add_reference_to_stage(usd_path=asset_path, prim_path=prim_path)

franka = XFormPrim(prim_path="/World/franka", name="franka")
panda_hand = XFormPrim(prim_path="/World/franka/panda_hand", name="panda_hand")
tool_center = XFormPrim(prim_path="/World/franka/panda_hand/tool_center", name="tool_center")

world.reset()

franka_pos, franka_ori = franka.get_world_pose()
hand_pos, hand_ori = panda_hand.get_world_pose()
tool_pos, tool_ori = tool_center.get_world_pose()

print("Franka world position =", franka_pos)
print("Franka world orientation =", franka_ori)

print("Hand world position =", hand_pos)
print("Hand world orientation =", hand_ori)

print("Tool center world position =", tool_pos)
print("Tool center world orientation =", tool_ori)

camera_world_offset = np.array([0.0, 0.0, 0.1])
camera_guess_world = tool_pos + camera_world_offset

camera_local_offset = np.array([0.0, 0.0, 0.1])

print("World offset example:")
print("Camera guessed world position =", camera_guess_world)

print("Local offset example:")
print("Camera local offset relative to tool_center =", camera_local_offset)
print("This means the camera is defined relative to tool_center, not directly in world coordinates.")

target_position = np.array([0.3, 0.0, 0.3])
tool_to_target = target_position - tool_pos

print("Target world position =", target_position)
print("Vector from tool_center to target =", tool_to_target)

distance_to_target = np.linalg.norm(tool_to_target)
print("Distance from tool_center to target =", distance_to_target)


print("Close the window manually when you finish looking.")



while simulation_app.is_running():
    world.step(render=True)
