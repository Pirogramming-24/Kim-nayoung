import cv2
import mediapipe as mp
import math, time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import visualization

# 1. 가위바위보 판별 로직 함수
def calculate_rps(landmarks):
    # 손가락 끝 인덱스: [검지, 중지, 약지, 소지]
    tip_ids = [8, 12, 16, 20]
    # 중간 관절 인덱스
    pip_ids = [6, 10, 14, 18]

    fingers_open = []

    # 검지~소지 4개 손가락의 펴짐 여부 확인
    for i in range(len(tip_ids)):
        if landmarks[tip_ids[i]].y < landmarks[pip_ids[i]].y:
            fingers_open.append(True)
        else:
            fingers_open.append(False)

    # 판별 로직 (엄지 제외 4손가락 기준)
    if fingers_open == [False, False, False, False]:
        return "Rock"
    elif fingers_open == [True, True, False, False]:
        return "Scissors"
    elif all(fingers_open): 
        return "Paper"
    else:
        return "Unknown"

# 2. 결과 저장을 위한 전역 변수 및 콜백 함수
latest_result = None

def print_result(result: vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global latest_result
    latest_result = result

# 3. 메인 실행 로직
if __name__ == "__main__":
    model_path = 'hand_landmarker.task'
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.LIVE_STREAM,
        num_hands=1,
        result_callback=print_result
    )

    detector = vision.HandLandmarker.create_from_options(options)
    cap = cv2.VideoCapture(0)

    print("웹캠을 시작합니다. 종료하려면 'q'를 누르세요.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        current_time_ms = int(time.time() * 1000)
        
        detector.detect_async(mp_image, current_time_ms)

        # 화면 그리기 로직
        if latest_result and latest_result.hand_landmarks:
            
            # 1. 랜드마크 시각화
            visualization.draw_manual(frame, latest_result)
            
            # 2. 가위바위보 판별
            for hand_landmarks in latest_result.hand_landmarks:
                rps_result = calculate_rps(hand_landmarks)
                cv2.putText(frame, f"Result: {rps_result}", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        cv2.imshow('Piro24 RPS Game', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    detector.close()
    cap.release()
    cv2.destroyAllWindows()