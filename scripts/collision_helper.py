from pxr import PhysxSchema, UsdPhysics
from omni.isaac.core.utils.prims import get_prim_at_path


def set_colliders(prim_path, collision_approximation="convexDecomposition"):
    prim = get_prim_at_path(prim_path)

    collider = UsdPhysics.CollisionAPI.Apply(prim)
    mesh_collider = UsdPhysics.MeshCollisionAPI.Apply(prim)
    mesh_collider.CreateApproximationAttr().Set(collision_approximation)
    collider.GetCollisionEnabledAttr().Set(True)

    if collision_approximation == "convexDecomposition":
        collision_api = PhysxSchema.PhysxConvexDecompositionCollisionAPI.Apply(prim)
        collision_api.CreateHullVertexLimitAttr().Set(64)
        collision_api.CreateMaxConvexHullsAttr().Set(64)
        collision_api.CreateMinThicknessAttr().Set(0.001)
        collision_api.CreateShrinkWrapAttr().Set(True)
        collision_api.CreateErrorPercentageAttr().Set(0.1)
    elif collision_approximation == "convexHull":
        collision_api = PhysxSchema.PhysxConvexHullCollisionAPI.Apply(prim)
        collision_api.CreateHullVertexLimitAttr().Set(64)
        collision_api.CreateMinThicknessAttr().Set(0.00001)
    elif collision_approximation == "sdf":
        collision_api = PhysxSchema.PhysxSDFMeshCollisionAPI.Apply(prim)
        collision_api.CreateSdfResolutionAttr().Set(1024)

    return prim
