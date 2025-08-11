import cv2
import time
from config import CAMERA_SOURCE, FRAME_WIDTH, FRAME_HEIGHT
from dance.pose_capture import PoseCapture
from dance.action_detector import ActionDetector
from dance.feature_extractor import FeatureExtractor
from dance.sequence_analyzer import SequenceAnalyzer
from utils import send_to_music, calculate_fps, draw_debug_info


def main():
    # 初始化摄像头
    cap = cv2.VideoCapture(CAMERA_SOURCE)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    # 初始化各模块
    pose_capture = PoseCapture()
    action_detector = ActionDetector()
    feature_extractor = FeatureExtractor()
    sequence_analyzer = SequenceAnalyzer()

    prev_time = time.time()

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 计算FPS
            fps, prev_time = calculate_fps(prev_time)

            # 姿态捕捉
            landmarks = pose_capture.process_frame(frame)

            # 初始化变量
            actions = []
            features = None  # 确保features变量已定义

            if landmarks:
                # 检测各种动作
                if action_detector.detect_jump(landmarks):
                    actions.append("JUMP")
                if action_detector.detect_spin(landmarks):
                    actions.append("SPIN")
                if action_detector.detect_hands_up(landmarks):
                    actions.append("HANDS_UP")

                # 更新前一帧数据
                action_detector.update_previous(landmarks)

                # 特征提取
                features = feature_extractor.extract_features(landmarks)  # 始终提取特征
                if features and actions:
                    features['action_type'] = actions[0]  # 取主要动作

                # 动作序列分析
                if actions:
                    sequence_analyzer.add_action(actions[0])  # 取主要动作
                sequence = sequence_analyzer.detect_sequence()
                if sequence:
                    actions.append(f"SEQUENCE:{sequence}")

                # 发送给音乐组
                if features and actions:
                    action_data = {
                        "actions": actions,
                        "features": features,
                        "timestamp": time.time()
                    }
                    send_to_music(action_data)

            # 绘制调试信息
            frame = draw_debug_info(frame, fps, actions, features)

            # 显示画面
            cv2.imshow('Dance Action Recognition', frame)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC键退出
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
