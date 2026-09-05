# Lineage M 실시간 번역기 🎮

Lineage M 게임 화면의 일본어를 실시간으로 한국어로 번역하고 화면에 오버레이로 표시하는 프로그램입니다.

## 기능 ✨

- 🎮 **실시간 화면 캡처** - 게임 화면을 실시간으로 캡처
- 🔤 **OCR 인식** - EasyOCR을 사용한 고정확 일본어 인식
- 🌐 **자동 번역** - Google Translate API를 사용한 번역
- 💾 **번역 캐싱** - 같은 텍스트는 캐시에서 빠르게 제공
- 🎨 **오버레이 표시** - 게임 화면 위에 번역 결과 표시

## 설치 및 실행 🚀

### 필수 요구사항

- **Python 3.8 이상** ([다운로드](https://www.python.org/downloads/))
- **Windows/Mac/Linux** 운영체제
- **4GB 이상 RAM** (권장: 8GB)
- **인터넷 연결** (번역 및 OCR 모델 다운로드)

### 한 줄 설치

#### Windows
```bash
run.bat
```

#### Mac/Linux
```bash
chmod +x run.sh
./run.sh
```

### 수동 설치

1. **저장소 클론**
```bash
git clone https://github.com/youkill87-ui/lineage-m-translator.git
cd lineage-m-translator
```

2. **Python 패키지 설치**
```bash
pip install -r requirements.txt
```

3. **프로그램 실행**
```bash
python main.py
```

## 사용 방법 📖

1. **프로그램 실행**
   - Windows: `run.bat` 더블클릭
   - Mac/Linux: `./run.sh` 실행

2. **Lineage M 게임 실행**
   - 게임을 실행하고 게임 화면을 활성화합니다

3. **번역 시작**
   - 프로그램이 자동으로 화면을 캡처하고 번역을 시작합니다
   - 원본 텍스트(일본어)는 **초록색**
   - 번역 텍스트(한국어)는 **파란색**으로 표시됩니다

4. **단축키**
   - **ESC**: 프로그램 종료
   - **P**: 일시정지/재개

## 성능 정보 ⚡

- **첫 실행**: 약 2-3분 (OCR 모델 다운로드 및 초기화)
- **이후 실행**: 즉시 시작
- **번역 속도**: CPU 기준 1-2초 (GPU 있으면 더 빠름)
- **FPS**: 약 2-5 FPS (정확도 우선)

### 더 빠른 성능을 원한다면?
- NVIDIA GPU 설치 추천
- CUDA 설치 후 `easyocr`를 GPU 모드로 실행

## 트러블슈팅 🔧

### Python이 설치되지 않았다고 나옴
→ [Python 공식 사이트](https://www.python.org/downloads/)에서 최신 버전 설치

### 패키지 설치 오류
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### OCR이 느림
→ GPU가 없으면 느립니다. 인내심을 가져주세요!

### 번역이 안 됨
→ 인터넷 연결 확인
→ 방화벽이 번역 서비스를 차단하지 않는지 확인

## 주의사항 ⚠️

- 게임에서 금지하는 프로그램이 아닌지 확인하세요
- 개인 학습용으로만 사용을 권장합니다
- 번역 정확도는 텍스트 크기와 품질에 따라 다릅니다

## 라이선스 📄

MIT License - 자유롭게 사용하세요!

## 피드백 💬

버그 report나 기능 제안은 Issues에 등록해주세요!

---

**만든이**: youkill87-ui  
**마지막 업데이트**: 2026년