import cv2
import mediapipe as mp
import numpy as np
# import tensorflow as tf
import tflite_runtime.interpreter as tflite


SCALING_FACTOR = 1.5  # 화면 크기 조정 비율

# ✅ 웹캠을 전역 변수로 설정하여 모든 파일에서 공유
cap = cv2.VideoCapture(0)

# ✅ MediaPipe 손 인식 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# ✅ 손동작 인식 (제스처 매핑)
rps_gesture = {
    0: 'zero',
    1: 'one',
    2: 'two',  # pen/erase
    3: 'three',
    4: 'four',
    5: 'five',  # toggle
    6: 'scissors',
    7: 'spiderman',
    8: 'okay',
}

# ✅ TFLite 모델 로드
model_name = 'hand_keypoint_classifier_weights[leaky_3dense].weights'
interpreter = tflite.Interpreter(model_path=f'weights/{model_name}.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# ✅ 손 인식 함수 (웹캠 사용)
def detect_hand_gesture(screen_width, screen_height):
    """손 인식 후 손동작과 좌표 반환"""
    
    # 🔹 웹캠이 열려 있는지 확인
    if not cap.isOpened():
        print("[ERROR] 웹캠이 열려 있지 않음")
        return "None", screen_width // 2, screen_height // 2
    
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] 웹캠에서 프레임을 읽을 수 없음")
        return "None", screen_width // 2, screen_height // 2

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    cursor_x, cursor_y = None, None
    hand_data = "None"

    if result.multi_hand_landmarks:
        for res in result.multi_hand_landmarks:
            joint = np.zeros((21, 3))
            for j, lm in enumerate(res.landmark):
                joint[j] = [lm.x, lm.y, lm.z]

            # 벡터 계산
            v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :]
            v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :]
            v = v2 - v1

            if np.linalg.norm(v, axis=1).min() == 0:
                continue  # 예외 처리

            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

            angle = np.arccos(np.einsum('nt,nt->n',
                v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:],
                v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:]))
            angle = np.degrees(angle)
            data = np.array([angle], dtype=np.float32)

            # ✅ TFLite 모델을 이용한 제스처 인식
            interpreter.set_tensor(input_details[0]['index'], data)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            predicted_idx = np.argmax(output_data)
            
            hand_data = rps_gesture[predicted_idx] if predicted_idx in rps_gesture else "None"

            # 손의 좌표 가져오기 (검지손가락 기준)
            raw_x = res.landmark[12].x * screen_width
            raw_y = res.landmark[12].y * screen_height

            # 중앙 기준 상대적 거리 1.5배 확대
            cursor_x = int((raw_x - screen_width // 2) * SCALING_FACTOR + screen_width // 2)
            cursor_y = int((raw_y - screen_height // 2) * SCALING_FACTOR + screen_height // 2) + 120

            # 화면을 벗어나지 않도록 제한
            cursor_x = min(max(0, cursor_x), screen_width - 1)
            cursor_y = min(max(0, cursor_y), screen_height - 1)


    # 손이 감지되지 않은 경우 기본 좌표 설정
    if cursor_x is None or cursor_y is None:
        cursor_x, cursor_y = screen_width // 2, screen_height // 2

    # print(f"[hand_tracking.py] hand_data: {hand_data}, cursor_x: {cursor_x}, cursor_y: {cursor_y}")
    return hand_data, cursor_x, cursor_y
 