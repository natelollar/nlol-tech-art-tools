"""Remove nLol Tools from Maya.
Drag and drop me into Maya viewport.
"""

import sys
from pathlib import Path


def onMayaDroppedPythonFile(*args) -> None:
    """Unload nlol Maya shelves.
    Remove project path from MAYA_MODULE_PATH in Maya.env.
    """
    # append project path to sys path for current maya session
    nlol_path = Path(__file__).parent / "maya"
    nlol_path_str = str(nlol_path)
    if nlol_path_str not in sys.path:
        sys.path.append(nlol_path_str)

    from importlib import reload

    from nlol.shelves_menus import unload_shelves, unload_menus
    from nlol.utilities import utils_install

    reload(unload_shelves)
    reload(unload_menus)
    reload(utils_install)

    # unload shelves
    unload_shelves.remove_nlol_shelves()

    # unload shelves
    unload_menus.remove_nlol_menus()

    # remove project path from env
    utils_install.update_project_env_path(project_path=nlol_path, install=False)
