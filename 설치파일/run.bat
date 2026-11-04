@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "PYLOCAL=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
set PY=
where py >nul 2>nul && set PY=py
if not defined PY where python >nul 2>nul && set PY=python
rem 마이크로소프트 스토어 가짜 python 은 실행이 안 되니 진짜로 돌아가는지 확인
if defined PY %PY% -c "import sys" >nul 2>nul || set PY=
if not defined PY if exist "%PYLOCAL%" set PY="%PYLOCAL%"
if defined PY goto :have_py

echo [안내] 이 컴퓨터에 파이썬이 없어서 자동으로 설치해요. 처음 한 번만, 몇 분 걸려요...
powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; $o=Join-Path $env:TEMP 'python-3.12.10-amd64.exe'; Invoke-WebRequest 'https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe' -OutFile $o -UseBasicParsing; Start-Process $o -ArgumentList '/quiet InstallAllUsers=0 PrependPath=1 Include_launcher=0 Include_test=0' -Wait"
if exist "%PYLOCAL%" set PY="%PYLOCAL%"
if defined PY goto :have_py
echo [안내] 파이썬을 자동으로 설치하지 못했어요. 인터넷 연결을 확인하거나 직접 설치해주세요:
echo https://www.python.org/downloads/ 에서 설치, 첫 화면에서 "Add python.exe to PATH" 체크!
pause
exit /b

:have_py
%PY% -c "import openpyxl, msoffcrypto, tkinter, win32com.client" >nul 2>nul && goto :run
echo 처음 실행: 필요한 부품 설치 중...
%PY% -m pip install openpyxl msoffcrypto-tool pywin32

:run
rem 켤 때마다 GitHub 에서 우리 관 최신 프로그램을 받아서 실행 - 관.txt, 토큰.txt
%PY% "%~dp0update_run.py"
if errorlevel 1 pause
