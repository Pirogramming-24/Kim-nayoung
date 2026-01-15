import os
os.environ['FLAGS_use_mkldnn'] = '0'
os.environ['FLAGS_enable_mkldnn'] = '0'

from paddleocr import PaddleOCR
import cv2
import re
import numpy as np

class OCRService:
    def __init__(self):
        self.ocr = PaddleOCR(lang='korean', use_angle_cls=False)

    def extract_nutrient_from_image(self, image_array):
        # 1. 전처리
        processed_img = self._preprocess_image(image_array)

        # 2. OCR 실행 (test_ocr의 predict 방식 사용)
        result = self.ocr.predict(processed_img)

        # 3. 결과 텍스트 추출
        full_text = ""
        if result and len(result) > 0:
            data = result[0]
            if 'rec_texts' in data:
                # 리스트 안의 텍스트들을 공백으로 연결
                full_text = " ".join(data['rec_texts'])
        
        # [디버깅] 추출된 텍스트 확인
        print("="*40)
        print(f"[PaddleOCR Final Text]\n{full_text}")
        print("="*40)

        # 4. 영양성분 추출 (기존 로직 유지)
        return self._extract_nutrition_info(full_text)

    def _preprocess_image(self, img):
        """이미지 전처리 (기존 유지)"""
        if img is None: return None
        img_resized = cv2.resize(img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        
        return cv2.cvtColor(clahe.apply(gray), cv2.COLOR_GRAY2BGR)

    def _extract_nutrition_info(self, text):
        """텍스트 파싱 및 데이터 추출 (기존 EasyOCR 코드의 로직 유지)"""
        t = text.lower()
        
        # 띄어쓰기 된 키워드 합치기
        keywords_map = {
            "탄 수 화 물": "탄수화물",
            "단 백 질": "단백질",
            "지 방": "지방",
            "칼 로 리": "칼로리",
            "나 트 륨": "나트륨",
            "당 류": "당류"
        }
        for k, v in keywords_map.items():
            t = t.replace(k, v)

        data = {
            'calorie': self._find_value(t, ['칼로리', 'kcal']),
            'carbohydrate': self._find_value(t, ['탄수화물'], unit='g'),
            'protein': self._find_value(t, ['단백질'], unit='g'),
            'fat': self._find_value(t, ['지방'], unit='g'),
        }
        return data

    def _find_value(self, text, keywords, unit=None):
        """값 찾기 (기존 EasyOCR 코드의 9/g 구분 및 소수점 유지 로직)"""
        for key in keywords:
            if unit is None: 
                # 칼로리 패턴
                pattern = rf'{key}.*?([0-9]+(?:\.[0-9]+)?)'
            else:
                # 정규식 끝에 (mg|g|9) -> '9'를 단위로 인식
                pattern = rf'{key}.*?([0-9]+(?:\.[0-9]+)?)\s*(mg|g|9)?'

            match = re.search(pattern, text)
            if match:
                try:
                    val = float(match.group(1))
                    
                    if unit and match.group(2):
                        captured_unit = match.group(2)
                        
                        # '9'가 잡히면 'g'로 간주
                        if captured_unit == '9':
                            pass 
                        # 'mg'이면 g로 변환
                        elif captured_unit == 'mg':
                            val = val / 1000.0
                    return val
                except ValueError:
                    continue
        return 0