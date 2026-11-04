@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PY=
where py >nul 2>nul && set PY=py
if "%PY%"=="" ( where python >nul 2>nul && set PY=python )
if "%PY%"=="" (
  echo [안내] 이 컴퓨터에 Python 이 없습니다.
  echo https://www.python.org/downloads/ 에서 설치하세요. 설치 첫 화면에서 "Add python.exe to PATH" 체크!
  pause
  exit /b
)
%PY% -c "import openpyxl, msoffcrypto, tkinter, win32com.client" >nul 2>nul || (
  echo 처음 실행: 필요한 부품 설치 중...
  %PY% -m pip install openpyxl msoffcrypto-tool pywin32
)
rem 켤 때마다 GitHub 에서 우리 관 최신 프로그램을 받아서 실행 (관.txt · 토큰.txt)
%PY% "%~dp0update_run.py"
if errorlevel 1 pause
