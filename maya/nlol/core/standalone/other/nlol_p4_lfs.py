import os
import subprocess
from pathlib import Path

env_var = os.environ.get("NLOL_P4_LFS")
if not env_var:
    raise EnvironmentError("NLOL_P4_LFS is not set")

path = Path(env_var) / "projects/project_name/assets/character_name/animation/"
if not path.exists():
    raise FileNotFoundError(f"Path does not exist: {path}")

print(f"Opening: {path}")
subprocess.Popen(["explorer", "/n,", str(path)])