# Isaac Sim Embodied Basics

This repository records my first hands-on Isaac Sim exercises while learning embodied AI.

The project goal is not to build a full robot system yet. The current goal is to understand the core stack clearly and quickly:

- scene setup
- physics basics
- Prim / API / Attribute
- USD loading
- camera basics
- Franka robot structure
- joint control
- gripper control
- target evaluation
- inverse kinematics (IK)
- closed-loop target following

## What I Learned

This repository currently covers:

- basic Isaac Sim scene startup
- simple object creation
- camera RGB capture
- Prim and applied schema inspection
- USD loading and transform control
- rigid body vs collision behavior
- Franka robot structure understanding
- end-effector / tool-center pose reading
- Franka joint and gripper control
- target distance evaluation
- pose comparison and simple pose search
- inverse kinematics for target reaching
- inverse kinematics with target orientation
- closed-loop target following with repeated IK

## Environment

- Isaac Sim `5.1.0`
- Windows
- Conda environment: `env_isaacsim`

## Project Structure

```text
isaacsim-embodied-basics/
|-- README.md
|-- .gitignore
`-- scripts/
    |-- first_scene.py
    |-- camera_scene.py
    |-- collision_helper.py
    |-- prim_intro.py
    |-- usd_intro.py
    |-- franka_intro.py
    |-- franka_joints.py
    |-- franka_move_joint1.py
    |-- franka_pose_target.py
    |-- franka_gripper.py
    |-- franka_target_task.py
    |-- franka_pose_compare.py
    |-- franka_pose_search.py
    |-- franka_ik_reach.py
    |-- franka_ik_pose.py
    |-- franka_follow_target_ik.py
    |-- franka_reach_loop.py
    |-- rigid_only.py
    |-- rigid_collision.py
    `-- rigid_no_gravity.py
```

## Scripts

### Scene and physics

- `scripts/first_scene.py`
  Minimal falling-cube scene.

- `scripts/rigid_only.py`
  Rigid body without collision. The cube falls through the ground.

- `scripts/rigid_collision.py`
  Rigid body with collision. The cube falls and stops on the ground.

- `scripts/rigid_no_gravity.py`
  Rigid body with gravity disabled. The cube stays suspended.

Key point:
- understand the difference between entering the physics system, colliding, and being affected by gravity

### Camera, Prim, and USD

- `scripts/camera_scene.py`
  Create a cube and capture an RGB image.

- `scripts/prim_intro.py`
  Inspect Prim path, schemas, and attributes.

- `scripts/usd_intro.py`
  Load a USD scene and manipulate poses.

- `scripts/collision_helper.py`
  Helper for applying mesh collision approximations such as `convexHull`, `convexDecomposition`, and `sdf`.

Key point:
- understand scene representation and how geometry, metadata, and assets are wired together

### Franka structure and direct control

- `scripts/franka_intro.py`
  Read Franka world pose, hand pose, tool-center pose, and target relation.

- `scripts/franka_joints.py`
  Print all controllable Franka joints.

- `scripts/franka_move_joint1.py`
  Move one joint to understand single-DOF control.

- `scripts/franka_pose_target.py`
  Apply a full 9-DOF Franka target pose.

- `scripts/franka_gripper.py`
  Open and close the gripper.

Key point:
- understand articulation control from one joint to the full robot

### Target evaluation and simple search

- `scripts/franka_target_task.py`
  Add a target cube and compute tool-center to target geometry.

- `scripts/franka_pose_compare.py`
  Compare two candidate poses and choose the closer one.

- `scripts/franka_pose_search.py`
  Evaluate several candidate poses and select the best one.

- `scripts/franka_reach_loop.py`
  Use a crude hand-written closed-loop heuristic to iteratively reduce target error.

Key point:
- understand the minimal embodied loop of state, action candidate, evaluation, and repeated correction

### Inverse kinematics

- `scripts/franka_ik_reach.py`
  Use IK to reach a target position.

- `scripts/franka_ik_pose.py`
  Use IK to reach a target position with a target orientation.

- `scripts/franka_follow_target_ik.py`
  Continuously recompute IK to follow a moving target.

Key point:
- move from hand-written joint updates to solver-based task-space control

## How To Run

Activate the Isaac Sim environment first:

```powershell
conda activate env_isaacsim
cd D:\isaacsim-embodied-basics
```

## License

This project is released under the [MIT License](./LICENSE).

Then run scripts such as:

```powershell
python .\scripts\prim_intro.py
python .\scripts\rigid_collision.py
python .\scripts\franka_joints.py
python .\scripts\franka_ik_reach.py
python .\scripts\franka_ik_pose.py
python .\scripts\franka_follow_target_ik.py
```

## Notes

- These scripts are intentionally small and focused.
- They are built for learning, not for production deployment.
- Isaac Sim 5.1.0 prints some deprecation and performance warnings; they do not block the main learning goals here.

## Next Steps

Planned future additions:

- camera mounted on robot links
- image-based target localization
- simple pick-and-place skeleton
- more structured embodied AI mini-projects
