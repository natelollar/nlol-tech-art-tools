@REM # -------------------------------------------------- #
@REM # Delete __pycache__ folders from current directory.
@REM # -------------------------------------------------- #
@echo off
echo Deleting all __pycache__ folders...
@REM `/d` Directories.
@REM `/r` Recursive.
@REM `.` Current directory.
@REM `%%d` Arbitrary variable.
@REM `%%d in (__pycache__)` Folders named __pycache__.
@REM `rd` Remove directory.
@REM `/s` Subdirectories.
@REM `/q` Quiet.
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo Done.
pause