@echo off
echo Setting up Nahw Exercises Backend Environment...

echo Creating virtual environment...
cd backend
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt

echo Populating database with initial data...
python populate_db.py

echo Backend setup complete!
echo You can now run 'start_backend.bat' to start the server.
pause
