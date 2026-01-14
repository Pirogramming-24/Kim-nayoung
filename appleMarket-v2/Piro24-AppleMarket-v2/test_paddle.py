import os
# [필수] Mac M1/M2 충돌 방지
os.environ['FLAGS_use_mkldnn'] = '0'
os.environ['FLAGS_enable_mkldnn'] = '0'

from paddleocr import PaddleOCR
import cv2

def test_ocr():
    print("🔄 PaddleOCR 모델을 로딩 중입니다...")
    
    try:
        # PaddleOCR 초기화
        ocr = PaddleOCR(lang='korean', use_angle_cls=False)
        print("✅ 모델 로딩 성공!")
    except Exception as e:
        print(f"❌ 모델 로딩 실패: {e}")
        return
    
    image_path = '/Users/kimnayoung/shrimp.png' 

    if not os.path.exists(image_path):
        print(f"❌ 이미지를 찾을 수 없습니다: {image_path}")
        return

    print(f"📸 이미지 읽는 중: {image_path}")
    
    # 3. OCR 실행 (predict 함수 사용 시)
    # predict는 결과가 딕셔너리 형태로 나옵니다.
    result = ocr.predict(image_path)
    
    # 4. 결과 출력
    print("\n" + "="*20 + " [최종 추출 텍스트] " + "="*20)
    
    if not result:
        print("결과가 없습니다.")
    else:
        # result[0]은 딕셔너리입니다. 여기서 'rec_texts' 키를 꺼내야 합니다.
        # 로그를 보면 result[0] 안에 'rec_texts' 리스트가 들어있습니다.
        data = result[0]
        if 'rec_texts' in data:
            text_list = data['rec_texts']
            
            # 리스트 안의 텍스트들을 하나씩 출력
            for text in text_list:
                # 빈 문자열은 건너뜀
                if text.strip():
                    print(text)
                    
            # (옵션) 한 줄로 합쳐서 보기
            print("-" * 40)
            print("[한 줄 요약]")
            print(" ".join(text_list))
        else:
            print("❌ 텍스트를 찾을 수 없습니다 (rec_texts 키 없음).")

    print("="*50)

if __name__ == "__main__":
    test_ocr()