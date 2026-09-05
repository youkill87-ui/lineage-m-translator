@echo off
echo Lineage M Translator 시작 중...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo 오류: Python이 설치되어 있지 않습니다!
    echo Python을 설치해주세요: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 필수 패키지를 설치하고 있습니다...
pip install -q -r requirements.txt

if errorlevel 1 (
    echo 패키지 설치에 실패했습니다.
    pause
    exit /b 1
)

echo.
echo 프로그램을 시작합니다...
echo.
python main.py

pause