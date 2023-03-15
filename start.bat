@ECHO OFF
echo --- Installing / Verifying Packages ---
call pip install -r requirements.txt
echo --- Starting Bot ---
call python Discordbot.py
pause>nul