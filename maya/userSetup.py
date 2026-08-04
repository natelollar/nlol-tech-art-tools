import inspect
import threading
from pathlib import Path

from nlol.defaults import rig_folder_path
from nlol.shelves_menus import reload_menus

from maya import cmds, utils


def run_on_start():
    print("=" * 75)
    print("-" * 75)
    try:
        current_file = inspect.getfile(inspect.currentframe())
        print(Path(current_file))
    except Exception:
        pass
    print(f"userSetup.py Executing{'.' * 50}")
    print("-" * 75)
    print("=" * 75)

    # create nlol menu in maya
    reload_menus.main_menu()

    # initialize rig context environment variables and paths
    rig_folder_path.set_environment_variables()
    rig_folder_path.check_rig_context_file()
    rig_folder_path.rig_folderpath_log()


# don't run in batch mode
if not cmds.about(batch=True):
    try:
        # "executeDeferred" delays until maya idle
        # "threading.Time" adds delay to create after other shelves
        timer = threading.Timer(10.0, lambda: utils.executeDeferred(run_on_start))
        timer.start()
    except Exception:
        print("----- nLol Menu creation FAILED. -----")
        raise
