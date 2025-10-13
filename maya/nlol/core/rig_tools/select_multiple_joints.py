"""Various functions for selecting multiple joints
in different ways.
"""

from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()


def select_joint_chain(start_end_joint: list[str]) -> list[str]:
    """Select joint chain based on first and last joint
    or just first joint. Requires end joint if joint branching anywhere along chain.

    Args:
        start_end_joint: Start joint or start and end joint, for a joint chain.
            If only start joint, will continue down the chain until the end.

    Returns:
        List of all joints in chain.

    """
    jnt_chain = [start_end_joint[0]]  # add start joint
    end_joint = None

    if len(start_end_joint) > 2:  # only accept 1 or 2 joints
        error_msg = "Too many joints for select_joint_chain. Requires 1 or 2 joints."
        logger.error(error_msg)
        raise ValueError(error_msg)
    if len(start_end_joint) == 2:  # get end joint
        end_joint = start_end_joint[1]

    for jnt in jnt_chain:
        # get next joint to iterate on
        jnt_child = cmds.listRelatives(jnt, children=True) or []

        # get around joint branching by quering branch with end_joint
        if len(jnt_child) > 1:
            if end_joint:
                for jnt in jnt_child:
                    all_descendents = (
                        cmds.listRelatives(jnt, allDescendents=True, type="joint") or []
                    )
                    all_descendents.append(jnt) # append immediate child back incase its end jnt
                    if end_joint in all_descendents:
                        jnt_chain.extend([jnt])
                        break
                continue  # stop iteration or joint children still get added below
            error_msg = (
                "Need end joint listed when joint branching in joint chain.\n"
                f"Joint: {jnt}\n"
                f"Branching joints: {jnt_child}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        if jnt == end_joint:  # stop at end joint
            if end_joint not in jnt_chain:
                jnt_chain.extend([end_joint])
            break

        if jnt_child:  # add child joint to chain list
            jnt_chain.extend(jnt_child)

    logger.debug(jnt_chain)
    return jnt_chain
