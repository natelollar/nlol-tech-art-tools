import debugpy

from maya import cmds

def main():
    maya_install_dir = cmds.internalVar(mayaInstallDir=True)
    maya_python_path = f"{maya_install_dir}/bin/mayapy.exe"
    debugpy.configure(python=maya_python_path)
    debugpy.listen(5678)

# https://gist.github.com/joaen/bdc154ecb3f28d8481b9fb23411d1008

# Create ".vscode/launch.json"
# {
#     "version": "0.2.0",
#     "configurations": [
#         {
#             "name": "Python: Remote Attach",
#             "type": "debugpy",
#             "request": "attach",
#             "connect": {
#                 "host": "localhost",
#                 "port": 5678
#             },
#             "justMyCode": true
#         }
#     ]
# }

# Download debugpy release: https://github.com/microsoft/debugpy/releases
# Copy folder "debugpy" from "src" folder.
# Paste debugpy folder into Maya scripts folder. 
#   C:\Users\%USERNAME%\Documents\maya\MAYA_VERSION\scripts
