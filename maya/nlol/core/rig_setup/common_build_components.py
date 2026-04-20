from importlib import reload

from maya import cmds
from nlol.core import general_utils
from nlol.core.rig_components import create_control_groups, create_nurbs_curves
from nlol.core.rig_setup import rig_variables
from nlol.utilities import nlol_maya_logger, nlol_maya_registry

reload(rig_variables)

add_divider_attribue = general_utils.add_divider_attribue
create_ctrl_grps = create_control_groups.create_ctrl_grps
logger = nlol_maya_logger.get_logger()
registry = nlol_maya_registry.get_registry()


class CommonBuildComponents:
    def __init__(self):
        """Initialize class for common shared rig components."""

    def build_top_dynamics_grps(self):
        """Create top groups for nDynamics organization."""
        top_grp_name = rig_variables.dynamics_main_grp
        if not cmds.objExists(top_grp_name):
            self.top_grp = cmds.group(empty=True, name=top_grp_name)
        else:
            self.top_grp = top_grp_name

        components_grp_name = rig_variables.dynamics_components_grp
        if not cmds.objExists(components_grp_name):
            self.components_grp = cmds.group(empty=True, name=components_grp_name)
        else:
            self.components_grp = components_grp_name

        cmds.parent(self.components_grp, self.top_grp)

        top_nodes = cmds.ls(assemblies=True)
        for obj in top_nodes:
            if "_rigGrp" in obj:
                cmds.parent(self.top_grp, obj)  # parent to main rig group

        for grp in [self.top_grp, self.components_grp]:
            for axis in "XYZ":
                cmds.setAttr(f"{grp}.translate{axis}", lock=True)
                cmds.setAttr(f"{grp}.rotate{axis}", lock=True)
                cmds.setAttr(f"{grp}.scale{axis}", lock=True)
        cmds.setAttr(f"{self.components_grp}.visibility", 0)

        # variables to global dict
        registry.register_obj("dynamics_main_grp", self.top_grp)
        registry.register_obj("dynamics_components_grp", self.components_grp)

    def build_dynamics_aux_ctrl(self):
        """Create nDynamics auxiliary ctrl."""
        aux_ctrl_name = rig_variables.dynamics_aux_ctrl
        if not cmds.objExists(aux_ctrl_name):
            aux_ctrl = create_nurbs_curves.CreateCurves(
                name=aux_ctrl_name,
                size=1.0,
                color_rgb=(0.2, 0.1, 0.7),
            ).dodecagon_curve()
            aux_ctrl_grp = create_ctrl_grps(aux_ctrl)[0]
        else:
            aux_ctrl = aux_ctrl_name
            aux_ctrl_grp = f"{aux_ctrl}Grp"

        # lock and hide attrs
        lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
        for axis in "XYZ":
            cmds.setAttr(f"{aux_ctrl}.translate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{aux_ctrl}.rotate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{aux_ctrl}.scale{axis}", **lock_hide_kwargs)
        cmds.setAttr(f"{aux_ctrl}.visibility", **lock_hide_kwargs)

        # top grp parenting
        dynamics_main_grp = rig_variables.dynamics_main_grp
        cmds.parent(aux_ctrl_grp, dynamics_main_grp)

        # variables to global dict
        registry.register_obj("dynamics_aux_ctrl", aux_ctrl)

    def aux_ctrl_nucleus_attrs(self, nucleus_nd) -> None:
        """Set up auxiliary ctrl attributes fot the nucleus node.

        Args:
            nucleus_nd: The nCloth nucleus node.

        """
        aux_ctrl = registry.get_obj("dynamics_aux_ctrl")

        add_divider_attribue(control_name=aux_ctrl)

        cmds.addAttr(
            aux_ctrl,
            longName="nucleusEnable",
            attributeType="bool",
            defaultValue=False,
            keyable=True,
        )
        cmds.connectAttr(f"{aux_ctrl}.nucleusEnable", f"{nucleus_nd}.enable")
        cmds.addAttr(
            aux_ctrl,
            longName="nucleusSpaceScale",
            attributeType="double",
            defaultValue=0.01,
            keyable=True,
        )
        cmds.setAttr(f"{aux_ctrl}.nucleusSpaceScale", lock=True)
        cmds.connectAttr(f"{aux_ctrl}.nucleusSpaceScale", f"{nucleus_nd}.spaceScale")
        cmds.addAttr(
            aux_ctrl,
            longName="nucleusStartFrame",
            attributeType="double",
            defaultValue=1,
            keyable=True,
        )
        cmds.connectAttr(f"{aux_ctrl}.nucleusStartFrame", f"{nucleus_nd}.startFrame")

        add_divider_attribue(control_name=aux_ctrl)
