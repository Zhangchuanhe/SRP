def draw_skeleton(frame, landmarks):
    """绘制人体骨架"""
    # 确保有可绘制的关键点
    if not landmarks:
        return frame

    # 绘制关键点和连接线
    import mediapipe as mp  # 需要导入mediapipe
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # 创建副本避免修改原图
    annotated_frame = frame.copy()

    # 绘制骨架
    mp_drawing.draw_landmarks(
        annotated_frame,
        landmarks,
        mp_pose.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),  # 关键点颜色
        mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)  # 连接线颜色
    )

    return annotated_frame
