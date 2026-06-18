@echo off
cd /d "%~dp0"

for /d /r . %%d in (__pycache__) do (
    if exist "%%d" rd /s /q "%%d"
)

for /r . %%f in (*.pyc) do (
    del /q "%%f"
)

set ZIPNAME=common-code-api_%date:~0,4%%date:~5,2%%date:~8,2%.zip
powershell Compress-Archive -Path '%~dp0.' -DestinationPath '%~dp0..\%ZIPNAME%' -Force

echo Done: %ZIPNAME%
pause
