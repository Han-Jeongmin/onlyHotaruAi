@echo off
set EMB_PYTHON_PATH=%~dp0\gas\python-3.6.8-embed-amd64\python

rem -----�v���W�F�N�g������-----
set PROJECT_NAME=�y���޽�z���ʃK�X�u�P�Ɛݒu
rem ----------------------------

rem �J�����g�Ɉړ�
cd /d %~dp0\gas
echo %EMB_PYTHON_PATH% app.py "%PROJECT_NAME%"
%EMB_PYTHON_PATH% app.py "%PROJECT_NAME%"

pause
