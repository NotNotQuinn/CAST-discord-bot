@ECHO off
:CODE
PYTHON ./src/bot.py
ECHO The bot has stopped working!
CHOICE /C NY /M "Restart"
IF ERRORLEVEL 2 GOTO CODE