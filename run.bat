@echo off
title TIA Level Editor - Launcher

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PYTHON_PATH=<PYTHON_PATH

echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo What do you want to do!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.
echo #1 - Run TIA Level Editor
echo. 
:selection

set INPUT=-1
set /P INPUT=Selection:


if %INPUT%==1 (
    goto run
) else (
	goto selection
)


:run
CLS
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Welcome to the TIA Level Editor!
echo This tool is still in its early stages!
echo Bugs are EXPECTED!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
:startgame
title TIA Level Editor - Debugger
%PYTHON_PATH% -m ttle
PAUSE
goto startgame