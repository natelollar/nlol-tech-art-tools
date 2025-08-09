from maya import cmds


class ShowAttributes:
    """Show or hide useful joint attributes in channel box.
    Select objects or enter target objects argument.
    """

    def __init__(
        self,
        target_objects: str | list | None = None,
        show_attrs: bool = True,
    ) -> None:
        """Args:
        target_objects: Object to perform function on.
        show_attrs: Show or hide these attributes in channel box.
        """
        self.target_objects = target_objects
        self.show_attrs = show_attrs

    def show_joint_attrs(self):
        """Show or hide useful joint attributes in channel box."""
        if self.target_objects is None:
            self.target_objects = cmds.ls(selection=True)

        attrs_list = [
            "wireColorR",
            "wireColorG",
            "wireColorB",
            "useObjectColor",
            "rotateAxisX",
            "rotateAxisY",
            "rotateAxisZ",
            "displayLocalAxis",
            "jointOrientX",
            "jointOrientY",
            "jointOrientZ",
            "drawStyle",
            "segmentScaleCompensate",
        ]

        if not isinstance(self.target_objects, list):
            self.target_objects = [self.target_objects]
        for obj in self.target_objects:
            for attr in attrs_list:
                try:
                    cmds.setAttr(f"{obj}.{attr}", channelBox=self.show_attrs)
                except Exception:
                    print(f"Failed to show/ hide: {obj}.{attr}")

    def show_curve_attrs(self):
        """Show or hide useful curve attributes in channel box."""
        if self.target_objects is None:
            self.target_objects = cmds.ls(selection=True)

        attrs_list = [
            "wireColorR",
            "wireColorG",
            "wireColorB",
            "useObjectColor",
        ]

        if not isinstance(self.target_objects, list):
            self.target_objects = [self.target_objects]
        for obj in self.target_objects:
            for attr in attrs_list:
                try:
                    cmds.setAttr(f"{obj}.{attr}", channelBox=self.show_attrs)
                except Exception:
                    print(f"Failed to show/ hide: {obj}.{attr}")
