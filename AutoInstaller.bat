@echo off
setlocal enabledelayedexpansion

:: ----------------------------------------------------------------------
:: Auto Installer Script...
:: This script automates the setup process for the TempMail project.
:: It performs the following steps:
:: 1. Checks for an active internet connection.
:: 2. Detects installed Python versions on the system.
:: 3. Prompts the user to select a Python version for creating a virtual environment.
:: 4. Installs dependencies from requirements.txt (if available) in project dir.
:: 5. Optionally runs the TempMail program immediately.
:: ----------------------------------------------------------------------

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
echo Detecting installed Python versions on your system...
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
    echo No Python installations detected. Please install Python and try again. & echo.
    pause
    exit /b
)

echo.

:: Step 3: Ask User to Select Python Version
:: Prompt the user to choose a Python version based on the index displayed earlier.
set /p choice=Which Python version do you want to use? 

:: Validate the user selection.
if not defined python%choice% (
    echo Invalid selection. Please try again. & echo.
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
    echo Installing dependencies from requirements.txt... & echo.
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    cls
    echo Installation complete. & echo.

) else (
    echo No requirements.txt found. Skipping dependency installation. & echo.
)

:: Step 6: Ask User to Run the Program
:: Prompt the user if they want to run the TempMail program immediately.
set /p "choice=Do you want to run the program right now (Y/N)? "

if /I "%choice%" == "y" (
    cls 
    echo Running TempMail program...
    .venv\Scripts\python.exe TempMail.py
    pause

) else (
    cls
    echo You can run the program anytime using the command:
    echo     ".venv\Scripts\python.exe TempMail.py" & echo.
    pause
)
