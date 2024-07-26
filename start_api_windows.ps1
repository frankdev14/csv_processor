# Environment variable for enabling debug mode
$env:DEBUG_MODE = "false"

# Uncomment for Activate virtual environment if you have one
# Change this if you are using a virtual env for your virtualenv and put your venv path
#& "C:\path\to\your\venv\Scripts\Activate.ps1"

# Change directory to 'app'
Set-Location -Path "app"

# Run the FastAPI application with Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
