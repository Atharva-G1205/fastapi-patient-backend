@echo off
REM create_venv_and_install.bat
REM Creates a Python virtual environment and installs packages from patient-api\requirements.txt (Windows CMD)

SETLOCAL ENABLEDELAYEDEXPANSION

REM -- Find Python executable (python or py -3)
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
  where py >nul 2>&1
  if %ERRORLEVEL% neq 0 (
    echo Python not found. Please install Python 3 and ensure "python" or "py" is on PATH.
    exit /b 1
  ) else (
    set "PYEXEC=py -3"
  )
) else (
  set "PYEXEC=python"
)

REM -- Create venv if it doesn't exist
if not exist venv (
  %PYEXEC% -m venv venv
  if %ERRORLEVEL% neq 0 (
    echo Failed to create virtual environment.
    exit /b 1
  )
) else (
  echo Using existing venv directory.
)

REM -- Activate venv
call venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
  echo Failed to activate virtual environment.
  exit /b 1
)

REM -- Upgrade pip and install requirements
%PYEXEC% -m pip install --upgrade pip
%PYEXEC% -m pip install -r patient-api\requirements.txt

echo.
echo Installation complete. To activate the venv later, run:
echo    venv\Scripts\activate.bat
echo.
ENDLOCAL
