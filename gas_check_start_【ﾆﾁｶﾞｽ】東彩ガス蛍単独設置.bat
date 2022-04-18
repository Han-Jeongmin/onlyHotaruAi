@echo off
set EMB_PYTHON_PATH=%~dp0\gas\python-3.6.8-embed-amd64\python

rem -----プロジェクト名入力-----
set PROJECT_NAME=【ﾆﾁｶﾞｽ】東彩ガス蛍単独設置
rem ----------------------------

rem カレントに移動
cd /d %~dp0\gas
echo %EMB_PYTHON_PATH% app.py "%PROJECT_NAME%"
%EMB_PYTHON_PATH% app.py "%PROJECT_NAME%"

pause
