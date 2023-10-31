@echo off
start /min cmd /c "pip install -r requirements.txt"
start /min cmd /c "python GetGoogleImages.py"