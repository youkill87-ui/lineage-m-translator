#!/bin/bash

echo "Lineage M Translator 시작 중..."
echo ""

# Python이 설치되어 있는지 확인
if ! command -v python3 &> /dev/null; then
    echo "오류: Python3이 설치되어 있지 않습니다!"
    echo "Python을 설치해주세요: https://www.python.org/downloads/"
    exit 1
fi

# 필수 패키지 설치
echo "필수 패키지를 설치하고 있습니다..."
pip3 install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "패키지 설치에 실패했습니다."
    exit 1
fi

# 프로그램 실행
echo ""
echo "프로그램을 시작합니다..."
echo ""
python3 main.py