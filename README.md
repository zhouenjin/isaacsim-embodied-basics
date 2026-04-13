# Isaac Sim Embodied Basics

This repository contains my early Isaac Sim learning exercises for embodied AI.

## Covered Topics

- minimal scene setup
- camera creation and RGB capture
- Prim, USD, and pose basics
- Franka robot structure and tool center pose
- rigid body vs. collision behavior

## Environment

- Isaac Sim 5.1.0
- Windows
- Python via `conda` environment `env_isaacsim`

## Scripts

- `scripts/first_scene.py`
  Minimal scene with a falling cube.

- `scripts/camera_scene.py`
  Creates a cube and captures an RGB image from a camera.

- `scripts/prim_intro.py`
  Intro exercise for Prim, applied schemas, and attributes.

- `scripts/usd_intro.py`
  Loads a saved USD asset into the current stage.

- `scripts/franka_intro.py`
  Loads Franka and inspects hand/tool-center pose and target relation.

- `scripts/rigid_only.py`
  Demonstrates rigid body without collision.

- `scripts/rigid_collision.py`
  Demonstrates rigid body with collision enabled.

## Notes

- These are learning scripts, so they are intentionally small and focused.
- Some scripts may print deprecation warnings from Isaac Sim 5.1.0. The warnings do not block the core demonstrations.
