import inspect
import threading
from pathlib import Path

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

    # Create nlol mnu in maya
    reload_menus.main_menu()


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
