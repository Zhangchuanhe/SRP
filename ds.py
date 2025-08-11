# 完整代码结构（复制到pose_detection.py）
import cv2
import mediapipe as mp
import time

# MediaPipe初始化
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# 摄像头初始化
cap = cv2.VideoCapture(0)
prev_time = 0

# 动作计数器（防抖动）
hand_up_counter = 0
squat_counter = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    # 转换为RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 姿态检测
    results = pose.process(rgb_frame)

    # 显示FPS
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if results.pose_landmarks:
        # 绘制骨架
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        landmarks = results.pose_landmarks.landmark

        # 1. 举手检测 -------------------------------------------
        left_wrist = landmarks[15]  # 左手腕
        left_shoulder = landmarks[11]  # 左肩
        right_wrist = landmarks[16]  # 右手腕
        right_shoulder = landmarks[12]  # 右肩

        # 判断逻辑：手腕高于肩膀
        if (left_wrist.y < left_shoulder.y or
                right_wrist.y < right_shoulder.y):
            hand_up_counter += 1
            if hand_up_counter > 5:  # 连续5帧确认
                cv2.putText(frame, "RAISE HAND DETECTED", (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                print("HANDS_UP")
        else:
            hand_up_counter = 0

        # 2. 深蹲检测 ------------------------------------------
        left_hip = landmarks[23]  # 左臀
        left_knee = landmarks[25]  # 左膝

        if left_hip.y > left_knee.y:  # 臀部低于膝盖
            squat_counter += 1
            if squat_counter > 8:  # 连续8帧确认
                cv2.putText(frame, "SQUAT DETECTED", (10, 110),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                print("SQUAT")
        else:
            squat_counter = 0

    # 显示画面
    cv2.imshow('Dance Action Recognition', frame)

    # 退出键
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()