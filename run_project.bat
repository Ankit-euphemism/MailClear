@echo off
setlocal

cd /d "%~dp0"

echo Activating virtual environment...
call ".venv\Scripts\activate"
REM call ".venv\Scripts\activate.bat" (alternate)
if errorlevel 1 (
    echo Failed to activate the virtual environment.
    exit /b 1
)
echo Virtual environment activated.

REM This training will take a while and will require a GPU.
echo Prefer to run untrained model to save time(recommended for first time users).

choice /C YN /M "Do you want to train the model now? This will take a while and will require a GPU."
if errorlevel 2 goto skip_training
if errorlevel 1 (
    echo Starting model training...
    python -m train
    if errorlevel 1 (
        echo Model training failed.
        exit /b 1
    )
)

:skip_training
echo Skipped model training.

echo Changing to the spam_detector directory...
cd /d "spam_detector"
if errorlevel 1 (
    echo Could not change to the spam_detector directory.
    exit /b 1
)
echo Current directory: %cd%

echo Starting Django development server...
python manage.py runserver

endlocal
