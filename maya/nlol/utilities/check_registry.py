from nlol.utilities import nlol_maya_logger, nlol_maya_registry

logger = nlol_maya_logger.get_logger()
registry = nlol_maya_registry.get_registry()


def verify_registry() -> None:
    """Check current registry values."""
    logger.info("Registry Data...")

    # keys = registry.nlol_objs
    # for key, key_value in keys.items():
    #     logger.info(f"{key!r} ({type(key_value).__name__}): {key_value!r}")

    keys = [
        "main_skeletalmesh_grp",
        "main_rig_grp",
        "dynamics_main_grp",
        "dynamics_components_grp",
        "dynamics_nucleus_nd",
        "dynamics_aux_ctrl",
    ]

    for key in keys:
        key_value = registry.get_obj(key)

        logger.info(f"{key!r} ({type(key_value).__name__}): {key_value!r}")
