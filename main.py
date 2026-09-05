import cv2
import easyocr
import numpy as np
import threading
import time
from PIL import ImageDraw, ImageFont, Image
import requests
import json
from collections import deque
import tkinter as tk
from tkinter import ttk
import subprocess
import sys

class GameTranslator:
    def __init__(self):
        self.reader = None
        self.running = False
        self.paused = False
        self.translation_cache = {}
        self.recent_translations = deque(maxlen=50)
        self.screen_width = 1920
        self.screen_height = 1080
        self.overlay_alpha = 0.7
        self.font_size = 20
        
    def init_ocr(self):
        """OCR 엔진 초기화"""
        print("OCR 엔진 초기화 중... (첫 실행 시 모델 다운로드, 시간이 걸릴 수 있습니다)")
        self.reader = easyocr.Reader(['ja', 'ko'], gpu=False)
        print("OCR 엔진 준비 완료!")
        
    def get_screen_capture(self):
        """화면 캡처"""
        try:
            import mss
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                return frame
        except:
            # mss가 없으면 pyautogui 사용
            import pyautogui
            screenshot = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return frame
    
    def recognize_text(self, frame):
        """이미지에서 텍스트 인식"""
        try:
            # 인식 정확도 향상을 위해 상단 영역에 집중
            h, w = frame.shape[:2]
            
            # 게임 UI 영역 (상단 30%, 중앙 40%)
            roi_y1, roi_y2 = 0, int(h * 0.4)
            roi_x1, roi_x2 = int(w * 0.3), int(w * 0.7)
            roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]
            
            results = self.reader.readtext(roi, detail=1)
            
            text_boxes = []
            for (bbox, text, confidence) in results:
                if confidence > 0.3 and len(text.strip()) > 0:
                    # 바운딩 박스 좌표 조정
                    pts = np.array(bbox, dtype=np.int32)
                    pts[:, 0] += roi_x1
                    pts[:, 1] += roi_y1
                    
                    text_boxes.append({
                        'text': text,
                        'bbox': pts,
                        'confidence': confidence
                    })
            
            return text_boxes
        except Exception as e:
            print(f"OCR 오류: {e}")
            return []
    
    def translate_text(self, text):
        """Papago API를 사용한 번역"""
        if not text.strip():
            return text
        
        # 캐시 확인
        if text in self.translation_cache:
            return self.translation_cache[text]
        
        try:
            # Google Translate 사용 (API 키 없이도 작동)
            url = "https://translate.googleapis.com/translate_a/element.js?cb=googleTranslateElementInit"
            
            # 더 간단한 방법: 로컬 번역 서비스 사용
            translated = self._translate_with_fallback(text)
            self.translation_cache[text] = translated
            return translated
        except Exception as e:
            print(f"번역 오류: {e}")
            return text
    
    def _translate_with_fallback(self, text):
        """폴백 번역 함수"""
        try:
            # requests를 사용한 Google Translate
            params = {
                'client': 'gtx',
                'sl': 'ja',
                'tl': 'ko',
                'dt': 't',
                'q': text
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(
                'https://translate.google.com/translate_a/single',
                params=params,
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                if result and result[0]:
                    translated_text = ''.join([item[0] for item in result[0]])
                    return translated_text
        except:
            pass
        
        return text
    
    def draw_translations(self, frame, text_boxes):
        """프레임에 번역 텍스트 그리기"""
        frame_copy = frame.copy()
        
        for box in text_boxes:
            text = box['text']
            translated = self.translate_text(text)
            bbox = box['bbox']
            
            # 바운딩 박스 그리기
            cv2.polylines(frame_copy, [bbox], True, (0, 255, 0), 2)
            
            # 텍스트 배경
            x, y = int(bbox[0][0]), int(bbox[0][1])
            cv2.rectangle(frame_copy, (x, y - 30), (x + 300, y), (0, 0, 0), -1)
            
            # 원본 텍스트 (일본어)
            cv2.putText(frame_copy, text, (x, y - 15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            # 번역된 텍스트 (한국어)
            cv2.putText(frame_copy, translated, (x, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            
            self.recent_translations.append({
                'original': text,
                'translated': translated,
                'time': time.time()
            })
        
        return frame_copy
    
    def run(self):
        """메인 루프"""
        self.running = True
        self.init_ocr()
        
        print("프로그램 시작됨!")
        print("게임을 실행하고 이 창을 활성화 상태로 유지하세요.")
        print("ESC를 누르면 종료됩니다.")
        
        frame_count = 0
        start_time = time.time()
        
        try:
            while self.running:
                if not self.paused:
                    # 화면 캡처
                    frame = self.get_screen_capture()
                    
                    # OCR 수행
                    text_boxes = self.recognize_text(frame)
                    
                    # 번역 결과 그리기
                    frame_with_translation = self.draw_translations(frame, text_boxes)
                    
                    # 화면 표시
                    cv2.imshow('Lineage M Translator', frame_with_translation)
                    
                    frame_count += 1
                    
                    # FPS 표시 (10프레임마다)
                    if frame_count % 10 == 0:
                        elapsed = time.time() - start_time
                        fps = frame_count / elapsed
                        print(f"FPS: {fps:.1f} | 인식된 텍스트: {len(text_boxes)} | 캐시: {len(self.translation_cache)}")
                
                # 키 입력 처리
                key = cv2.waitKey(100) & 0xFF
                if key == 27:  # ESC
                    self.running = False
                    print("프로그램을 종료합니다...")
                elif key == ord('p'):  # P: 일시정지/재개
                    self.paused = not self.paused
                    status = "일시정지" if self.paused else "재개"
                    print(f"상태: {status}")
        
        except KeyboardInterrupt:
            print("중단됨")
        except Exception as e:
            print(f"오류 발생: {e}")
        finally:
            cv2.destroyAllWindows()
            self.running = False

def install_dependencies():
    """필수 패키지 설치"""
    print("필수 패키지를 설치하고 있습니다...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("설치 완료!")

if __name__ == "__main__":
    # 의존성 확인 및 설치
    try:
        import mss
    except ImportError:
        print("mss 설치 중...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mss"])
    
    translator = GameTranslator()
    translator.run()