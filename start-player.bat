@echo off
cd /d "C:\Projects\PlayerSekai"

start cmd /k npx live-server

timeout /t 3 >nul

start http://127.0.0.1:5500/player.html
