import json
import os
from importlib import reload
from pathlib import Path

from PySide6.QtWidgets import QMessageBox

from maya import cmds
from nlol import defaults
from nlol.core.modeling_tools import materials_export_import
from nlol.core.rig_setup import rig_build, rig_build_mesh_skeleton
from nlol.core.ui import rig_context_ui
from nlol.defaults.rig_folder_path import rig_folderpath
from nlol.utilities.nlol_maya_logger import get_logger

reload(rig_build_mesh_skeleton)
reload(rig_build)
reload(materials_export_import)

RIG_CONTEXT_JSON = Path(defaults.__file__).parent / "rig_context.json"

logger = get_logger()


class RigBuildSaveAll:
    """Rebuild all Character auto-rig folders. Update materials. Save files.
    Also the option to only build/save active rig folder.
    """

    def __init__(self, show_confirmations: bool = True) -> None:
        """Initialize class.

        Args:
            show_confirmations: Show additional confirmation windows before each rig build.

        """
        self.show_confirmations = show_confirmations

        # parent to current active RIG folder
        self.initial_rig_folderpath = rig_folderpath()
        self.character_folderpath = self.initial_rig_folderpath.parent

    def build(self) -> None:
        """Build all auto-rig folders in Character folder.
        --------------------------------------------------

        Character folder defaults to parent folder of current active auto-rig folder.
        """
        try:
            self.get_rig_context_folderpaths()
            self.confirmation_window_main()
            self.build_save_all_rigs()
            rig_context_ui.refresh_if_open()
        except InterruptedError as e:
            logger.info(e)
            return

    def get_rig_context_folderpaths(self) -> list[Path]:
        """Query auto-rig folders (a.k.a., "RIG" folders), from the Character folder."""
        autorig_txt = {"auto_rig", "autorig", "auto-rig"}

        # ----- get auto_rig folder paths in character folder
        autorig_folderpaths = [
            folderpath
            for folderpath in self.character_folderpath.glob("*")
            if folderpath.is_dir() and any(txt in folderpath.name.lower() for txt in autorig_txt)
        ]
        if len(autorig_folderpaths) == 0:
            msg = f"No auto-rig folders found in: {self.character_folderpath}"
            logger.error(msg)
            raise FileNotFoundError(msg)

        # ----- main rig folder to build last
        # if only one auto-rig group, assign as main auto-rig folder
        main_autorig_folderpath = None
        if len(autorig_folderpaths) == 1:
            main_autorig_folderpath = autorig_folderpaths[0]
        else:
            # main auto-rig group must be named equal to autorig_txt
            main_autorig_folderpath = [
                fp
                for fp in autorig_folderpaths
                if any(fp.name.lower() == txt for txt in autorig_txt)
            ]
            if main_autorig_folderpath:
                main_autorig_folderpath = main_autorig_folderpath[0]
            autorig_folderpaths.remove(main_autorig_folderpath)

        # ----- variable instances
        self.autorig_folderpaths = autorig_folderpaths
        self.main_autorig_folderpath = main_autorig_folderpath

    def build_save_all_rigs(self) -> None:
        """Build all auto-rig folders within Character folder. Build main auto-rig folder last.
        Character folder defaults to parent of current active auto-rig folder.
        """
        # build auto-rig folders
        for fp in self.autorig_folderpaths:
            self.set_active_rig(fp)
            self.build_save_rig()

        # build main auto-rig folder
        self.set_active_rig(self.main_autorig_folderpath)
        self.build_save_rig()

    def build_save_rig(
        self,
        update_materials: bool = True,
        build_skeletalmeshes: bool = True,
    ) -> None:
        """Build and save auto-rig (and skeletal mesh) from current active rig folder.
        Update materials in model file as well.
        """
        if update_materials:
            self.update_model_materials()

        if build_skeletalmeshes:
            rig_build_mesh_skeleton.run_mesh_skeleton_build(
                show_confirmation=self.show_confirmations,
            )
            self.save_rig_build(save_suffix="_skeletalMesh")

        rig_build.run_rig_build(show_confirmation=self.show_confirmations)
        self.save_rig_build(save_suffix="_rig")

    def set_active_rig(self, autorig_folderpath: Path, check_active: bool = True) -> None:
        """Set active rig folder path in rig_context.json.

        Args:
            autorig_folderpath: Folderpath to activate for building rig.
            check_active: Double check json active rig folder.
                Gives extra time to update json incase of os buffer.

        """
        # rig context json data
        rig_context_data = self.load_rig_context()

        # set all rigs to non-active
        for rig in rig_context_data.get("rigs", []):
            rig["active"] = False

        # active current rig
        for rig in rig_context_data.get("rigs", []):
            rig_path_expanded = Path(os.path.expandvars(rig["folderpath"]))
            if rig_path_expanded == autorig_folderpath:
                rig["active"] = True
                break

        # save back json data
        self.save_rig_context(rig_context_data)

        # log active rig folder
        if check_active:
            rig_context_data = self.load_rig_context()
            for rig in rig_context_data.get("rigs", []):
                if rig["active"]:
                    logger.info(f"Active rig: {rig['folderpath']}")

    def update_model_materials(self):
        """Update materials for "model.ma" file (in active rig folder).
        Searches "materials" folder for materials to update (in active rig folder).
        Materials in model file will only be updated if they have a matching
        material in the "materials" folder.
        """
        model_filepath = rig_folderpath() / "model.ma"
        model_filepath = (model_filepath).as_posix()  # convert to string
        # ----- open model file
        cmds.file(model_filepath, open=True, force=True, ignoreVersion=True, options="v=0;")

        # ----- update materials
        materials_export_import.update_scene_materials()  # searches active rig "materials" folder

        # ----- save model file
        old_prompt = cmds.file(query=True, prompt=True)
        try:
            cmds.file(prompt=False)
            cmds.file(rename=model_filepath)
            cmds.file(save=True, force=True, type="mayaAscii", options="v=0;")
        except RuntimeError:
            self.read_only_popup(model_filepath)
        finally:
            cmds.file(prompt=old_prompt)

        # -----
        logger.info(f"Materials updated: {model_filepath}")

    def save_rig_build(self, save_suffix="") -> None:
        """Save open file which contains rig build.
        Save using name parameter in rig_context.json.
        """
        # -----
        character_nm = "characterName"
        rig_context_data = self.load_rig_context()
        for rig in rig_context_data.get("rigs", []):
            if rig["active"]:
                character_nm = rig["name"]

        rig_save_path = (self.character_folderpath / f"{character_nm}{save_suffix}.ma").as_posix()

        # ----- save
        old_prompt = cmds.file(query=True, prompt=True)
        try:
            cmds.file(prompt=False)
            cmds.file(rename=rig_save_path)
            cmds.file(save=True, force=True, type="mayaAscii", options="v=0;")
        except RuntimeError:
            self.read_only_popup(rig_save_path)
        finally:
            cmds.file(prompt=old_prompt)

    def load_rig_context(self) -> dict:
        """Load rig_context.json contents."""
        with open(RIG_CONTEXT_JSON) as f:
            return json.load(f)

    def save_rig_context(self, data: dict) -> None:
        """Write rig_context.json contents."""
        with open(RIG_CONTEXT_JSON, "w") as f:
            json.dump(data, f, indent=4)
            # ----- make sure json is written
            f.flush()
            os.fsync(f.fileno())

    def confirmation_window_main(self, active_rig_only: bool = False):
        """Main confirmation window to confirm the start of building all the rigs.

        Args:
            active_rig_only: Dialog options for when only building and saving active rig.

        """
        yes_str = "Yes"
        yes_str_confirms = "Yes w/ Confirm Windows"
        no_str = "No"
        if not active_rig_only:
            autorig_folderpaths_str = "\n".join(f"> {pth}" for pth in self.autorig_folderpaths)
            dialog_msg = (
                "Build ALL RIGs?\n-----Main auto-rig folder-----\n"
                f"> {self.main_autorig_folderpath}\n"
                f"-----Other auto-rig folders-----\n{autorig_folderpaths_str}"
            )
        else:
            dialog_msg = f"Build Active RIG?:  {self.initial_rig_folderpath.name}"
            logger.info(f"Active rig folder: {self.initial_rig_folderpath}")
        self.dialog_result = cmds.confirmDialog(
            title="Confirm",
            message=dialog_msg,
            button=[yes_str, yes_str_confirms, no_str],
            defaultButton="Yes",
            cancelButton=no_str,
            dismissString=no_str,
            bgc=(0.2, 0.2, 0.2),
        )
        if self.dialog_result == no_str:
            raise InterruptedError("RIG BUILDS CANCELLED...")

        if self.dialog_result == yes_str_confirms:
            self.show_confirmations = True
        else:
            self.show_confirmations = False

    def build_active_only(self) -> None:
        """Build current active auto-rig folder only.
        Will update materials and save out files too.
        """
        try:
            self.confirmation_window_main(active_rig_only=True)
            self.build_save_rig()
        except InterruptedError as e:
            logger.info(e)
            return

    def read_only_popup(self, filepath: Path | str):
        """Popup when trying to save read-only file."""
        filepath = Path(filepath)
        msg = f'(READ-ONLY) Permission denied saving: "{filepath}"'
        logger.info(msg)
        QMessageBox.warning(
            None,
            "Failed to Save",
            f'<Check Out> in Perforce!\n"{filepath.name}" is READ-ONLY and was NOT saved.\n',
        )
        raise InterruptedError(msg)
