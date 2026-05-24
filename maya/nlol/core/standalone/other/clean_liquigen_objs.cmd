:: Place this script in the OBJ sequence folder with "clean_liquigen_objs.py".
:: Double click this cmd script to launch the cleanup session.
@echo off
echo --- STARTING OBJ MESH CLEANUP ---
pushd "%~dp0"
 
"C:\Program Files\Autodesk\Maya2026\bin\mayapy.exe" clean_liquigen_objs.py
 
echo --- CLEANUP HAS FINISHED ---
popd
pause
 