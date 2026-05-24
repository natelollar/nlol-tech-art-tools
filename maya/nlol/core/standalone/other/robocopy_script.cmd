@echo off
@REM Robocopy Batch Script for Windows 11

set SOURCE=C:\folder_name\Source_Folder
set DESTINATION=D:\folder_name\folder_name\Destination_Folder

@REM Check destination exists, error if not
if not exist "%DESTINATION%" (
    echo Error: Destination folder does not exist: %DESTINATION%
    pause
    exit /b 1
)

@REM Safety checks to prevent accidental data loss
if not "%DESTINATION:~0,1%"=="D" (
    echo Error: DESTINATION should be on D: drive. Aborting to prevent data loss.
    pause
    exit /b 1
)

echo.
echo About to backup:
echo   FROM: %SOURCE%
echo   TO:   %DESTINATION%
echo.
set /p CONFIRM="Continue? (Y/N): "
if /I not "%CONFIRM%"=="Y" exit /b 1

@REM Run robocopy with common options
@REM /MIR = Mirror directories (copy new/changed files, delete files not in source)
@REM /R:3 = Retry 3 times for failed copies
@REM /W:5 = Wait 5 seconds between retries
@REM /V = Verbose output to console (shows file transfers in real-time)
@REM /TEE = Display output in console AND save to log file simultaneously
@REM /LOG = Create a log file

@REM Uncomment to run robocopy.
@REM robocopy "%SOURCE%" "%DESTINATION%" /MIR /R:3 /W:5 /V /TEE /LOG:"%DESTINATION%\..\backup_log.txt"

@REM Check if robocopy was successful
if %ERRORLEVEL% LSS 8 (
    echo Backup completed successfully!
) else (
    echo Backup failed or completed with warnings. Check the log file.
)

pause