# Isaac Sim Embodied Basics

This repository records my first hands-on Isaac Sim exercises while learning embodied AI.

The goal of this project is not to build a complete robot system yet. It is to understand the core building blocks clearly:

- how a scene is created
- how a cube falls under physics
- why `RigidBody` and `Collision` are different
- what a Prim / API / Attribute means in practice
- how USD assets are loaded into a stage
- how to read robot hand and tool-center poses
- how a camera relates to world coordinates and local coordinates

## What I Learned

This repository currently covers:

- basic Isaac Sim scene startup
- simple object creation
- camera RGB capture
- Prim and applied schema inspection
- USD loading and transform control
- Franka robot structure understanding
- end-effector / tool-center pose reading
- rigid body vs collision behavior

## Environment

- Isaac Sim `5.1.0`
- Windows
- Conda environment: `env_isaacsim`

## Project Structure

```text
isaacsim-embodied-basics/
├── README.md
├── .gitignore
└── scripts/
    ├── first_scene.py
    ├── camera_scene.py
    ├── prim_intro.py
    ├── usd_intro.py
    ├── franka_intro.py
    ├── rigid_only.py
    └── rigid_collision.py
```

## Scripts

### `scripts/first_scene.py`

Creates a minimal scene and drops a cube.

Key point:
- the simplest possible Isaac Sim physics example

### `scripts/camera_scene.py`

Creates a cube and captures an RGB image from a camera.

Key point:
- camera pose determines what the image sees

### `scripts/prim_intro.py`

Inspects a cube Prim, its applied schemas, and its attributes.

Key point:
- understand `Prim`, `API`, and `Attribute` through a real object

### `scripts/usd_intro.py`

Loads a saved USD scene into the current stage and reads / modifies pose information.

Key point:
- understand how USD assets are mounted and transformed

### `scripts/franka_intro.py`

Loads a Franka robot and prints:

- robot world pose
- hand world pose
- tool-center world pose
- target vector and distance

Key point:
- understand the geometry relation between robot end-effector and task target

### `scripts/rigid_only.py`

Applies rigid body behavior without collision.

Observed result:
- the cube falls through the ground

Key point:
- `RigidBody` alone does not create collision geometry

### `scripts/rigid_collision.py`

Applies both rigid body and collision.

Observed result:
- the cube falls and stops on the ground

Key point:
- collision is what allows physical contact

## How To Run

Activate the Isaac Sim environment first:

```powershell
conda activate env_isaacsim
cd D:\isaacsim-embodied-basics
```

## License

This project is released under the [MIT License](./LICENSE).

Then run a script, for example:

```powershell
python .\scripts\prim_intro.py
python .\scripts\rigid_only.py
python .\scripts\rigid_collision.py
python .\scripts\franka_intro.py
```

## Notes

- These scripts are intentionally small and focused.
- They are built for learning, not for production deployment.
- Isaac Sim 5.1.0 may print deprecation warnings; they do not affect the main learning goals here.

## Next Steps

Planned future additions:

- articulated robot control
- camera mounted on robot links
- grasping / pick-and-place style tasks
- more structured embodied AI mini-projects
