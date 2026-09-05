import cv2
import easyocr
import numpy as np
import time
import subprocess
import sys
from collections import deque
import requests

class GameTranslator:
    def __init__(self):
        self.reader = None
        self.running = False
        self.paused = False
        self.translation_cache = {}
        self.recent_translations = deque(maxlen=50)
        
    def init_ocr(self):
        print("OCR 엔진 초기화 중...")
        self.reader = easyocr.Reader(['ja', 'ko'], gpu=False)
        print("OCR 엔진 준비 완료!")
        
    def get_screen_capture(self):
        try:
            import mss
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                return frame
        except:
            import pyautogui
            screenshot = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return frame
    
    def recognize_text(self, frame):
        try:
            h, w = frame.shape[:2]
            roi_y1, roi_y2 = 0, int(h * 0.4)
            roi_x1, roi_x2 = int(w * 0.3), int(w * 0.7)
            roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]
            
            results = self.reader.readtext(roi, detail=1)
            
            text_boxes = []
            for (bbox, text, confidence) in results:
                if confidence > 0.3 and len(text.strip()) > 0:
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
        if not text.strip():
            return text
        
        if text in self.translation_cache:
            return self.translation_cache[text]
        
        try:
            translated = self._translate_with_fallback(text)
            self.translation_cache[text] = translated
            return translated
        except Exception as e:
            print(f"번역 오류: {e}")
            return text
    
    def _translate_with_fallback(self, text):
        try:
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
        frame_copy = frame.copy()
        
        for box in text_boxes:
            text = box['text']
            translated = self.translate_text(text)
            bbox = box['bbox']
            
            cv2.polylines(frame_copy, [bbox], True, (0, 255, 0), 2)
            
            x, y = int(bbox[0][0]), int(bbox[0][1])
            cv2.rectangle(frame_copy, (x, y - 30), (x + 300, y), (0, 0, 0), -1)
            
            cv2.putText(frame_copy, text, (x, y - 15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            cv2.putText(frame_copy, translated, (x, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        
        return frame_copy
    
    def run(self):
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
                    frame = self.get_screen_capture()
                    text_boxes = self.recognize_text(frame)
                    frame_with_translation = self.draw_translations(frame, text_boxes)
                    
                    cv2.imshow('Lineage M Translator', frame_with_translation)
                    
                    frame_count += 1
                    
                    if frame_count % 10 == 0:
                        elapsed = time.time() - start_time
                        fps = frame_count / elapsed
                        print(f"FPS: {fps:.1f} | 인식: {len(text_boxes)} | 캐시: {len(self.translation_cache)}")
                
                key = cv2.waitKey(100) & 0xFF
                if key == 27:
                    self.running = False
                    print("종료 중...")
                elif key == ord('p'):
                    self.paused = not self.paused
                    status = "일시정지" if self.paused else "재개"
                    print(f"상태: {status}")
        
        except KeyboardInterrupt:
            print("중단됨")
        except Exception as e:
            print(f"오류: {e}")
        finally:
            cv2.destroyAllWindows()
            self.running = False

if __name__ == "__main__":
    translator = GameTranslator()
    translator.run()