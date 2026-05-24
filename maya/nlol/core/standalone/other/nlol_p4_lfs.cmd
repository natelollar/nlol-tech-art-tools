:: RUN PYTHON SCRIPT FROM THIS DIRECTORY

:: enable !errorlevel! expansion inside blocks
setlocal enabledelayedexpansion

set SCRIPT=nlol_p4_lfs.py
:: get script in current directory
set SCRIPT=%~dp0%SCRIPT%

:: run python script
where python >nul 2>&1
if %errorlevel%==0 (
    python "%SCRIPT%"
    :: keep window open if error
    if !errorlevel! neq 0 (
        cmd /k
    )
    exit /b
)

:: look for maya python if no system python
for %%y in (2030 2029 2028 2027 2026 2025) do (
    if exist "C:\Program Files\Autodesk\Maya%%y\bin\mayapy.exe" (
        "C:\Program Files\Autodesk\Maya%%y\bin\mayapy.exe" "%SCRIPT%"
        if !errorlevel! neq 0 (
            cmd /k
        )
        exit /b
    )
)

echo Python not found. Please install Python or Maya.
pause