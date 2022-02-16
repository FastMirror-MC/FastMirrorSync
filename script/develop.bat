@ECHO OFF

@REM Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
@REM If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

cd ../
mklink /D src client
cd src
mklink /D lib ..\lib
mklink /D spigot_jdk8 ..\docker\spigot_jdk8
mklink /D spigot_jdk16 ..\docker\spigot_jdk16
mklink /D spigot_jdk17 ..\docker\spigot_jdk17
mklink /H spigot.py ..\docker\sync.py
mklink /H info.py ..\docker\info.py
pause
