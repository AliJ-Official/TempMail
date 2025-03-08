@echo off
setlocal enabledelayedexpansion

:: Step 1: Check Internet Connection
:: Pings Google to check for an active internet connection.
:: If no connection is detected, notify the user and exit.
echo Checking internet connection...
ping www.google.com -n 1 -w 1000 >nul

if errorlevel 1 (
    echo No internet connection found. Please check your connection.
    pause
    exit /b
)

:: Clear the screen for better readability
cls 

:: Step 2: Detect Installed Python Versions
:: Find all Python executables installed on the system and store them in a temporary file.
echo Installed versions of Python on your system:
where python > temp_python_versions.txt 2>nul

set "index=0"
:: Loop through the list of detected Python installations and display them.
for /f "delims=" %%A in (temp_python_versions.txt) do (
    set /a index+=1
    set "python!index!=%%A"
    echo    !index!. %%A
)

:: Delete the temporary file after processing.
del temp_python_versions.txt 2>nul

:: If no Python installations are detected, notify the user and exit.
if %index%==0 (
    echo No Python installations detected. Install Python and try again. & echo.
    pause
    exit /b
)

echo.

:: Step 3: Ask User to Select Python Version
:: Prompt the user to choose a Python version based on the index displayed earlier.
set /p choice=Which Python version do you want to use? 

:: Validate the user selection.
if not defined python%choice% (
    echo Invalid selection. & echo.
    pause
    exit /b
)

:: Store the selected Python executable's path.
set "PYTHON_EXEC=!python%choice%!"
echo Selected Python: %PYTHON_EXEC%

:: Clear the screen before proceeding.
cls 

:: Step 4: Create Virtual Environment
:: If a virtual environment does not exist, create one using the selected Python version.
if not exist .venv\Scripts\activate (
    echo Creating Virtual Environment... & echo.
    %PYTHON_EXEC% -m venv .venv
) else (
    echo Virtual Environment already exists. & echo.
)

:: Step 5: Install Dependencies (If requirements.txt Exists)
:: Check for a 'requirements.txt' file and install dependencies if found.
if exist requirements.txt (
    echo Installing dependencies... & echo.
    .venv\Scripts\python.exe -m pip install -r requirements.txt

    cls

    echo Installation complete. & echo.
) else (
    echo No requirements.txt found. Skipping dependency installation. & echo.
)

:: Step 6: Ask User to Activate Virtual Environment
:: Prompt user if they want to activate the virtual environment immediately.
set /p "choice=Do you want to activate the Virtual Environment (Y/N)? "

if /I "%choice%" == "y" (
    cls
    cmd /k ".venv\Scripts\activate.bat"
) else (
    echo You can manually activate the Virtual Environment using ".venv\Scripts\activate.bat"
)
