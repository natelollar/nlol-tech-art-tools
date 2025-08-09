"""Drag and drop me into Maya viewport.
Installs nLol Maya shelves.
Adds project path to Maya.env.
Tested in Maya 2025 on Windows 11.
"""

import sys
from pathlib import Path


def onMayaDroppedPythonFile(*args) -> None:
    """Drag and drop Maya install.
    Drag "maya_install.py" file from Windows Explorer browser into Maya viewport.
    Installs Maya shelves.
    Adds project path to MAYA_MODULE_PATH variable in "Maya.env".
    This connects to "nlol_env.mod" instead of using PYTHONPATH.
    Appends project path to sys.path for current session.
    """
    # append project path to sys path for current maya session
    nlol_path = Path(__file__).parent / "maya"
    nlol_path_str = str(nlol_path)
    if nlol_path_str not in sys.path:
        sys.path.append(nlol_path_str)

    from importlib import reload

    from nlol.shelves_menus import reload_shelves, reload_menus
    from nlol.utilities import utils_install

    reload(reload_shelves)
    reload(reload_menus)
    reload(utils_install)

    # load shelves
    reload_shelves.update_nlol_shelves()

    # load menus
    reload_menus.main_menu()

    # add project directory path to MAYA_MODULE_PATH Maya.env
    utils_install.update_project_env_path(project_path=nlol_path, install=True)


# NOTE:
# Adjusted this file:
# C:\Program Files\Autodesk\Maya2025\Python\Lib\site-packages\maya\app\general\executeDroppedPythonFile.py
# Added "importlib.reload(loadedModule)" to line 64.
