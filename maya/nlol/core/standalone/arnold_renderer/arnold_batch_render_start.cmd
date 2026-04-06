:: Place this script in the render output folder with "arnold_batch_render.py".
:: Double click this cmd script to launch the render session.
@echo off
echo --- STARTING GUI SESSION RENDER ---
pushd "%~dp0"

"C:\Program Files\Autodesk\Maya2026\bin\maya.exe" ^
    -command "python(\"exec(open('arnold_batch_render.py').read())\")"

echo --- MAYA HAS FINISHED ---
popd
pause
