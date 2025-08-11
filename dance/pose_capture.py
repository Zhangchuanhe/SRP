#姿态捕捉（使用MediaPipe）
import cv2
import mediapipe as mp
from config import MIN_DETECTION_CONFIDENCE, MIN_TRACKING_CONFIDENCE


class PoseCapture:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )

    def process_frame(self, frame):
        """处理视频帧，提取姿态关键点"""
        # 将BGR图像转换为RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 处理帧
        results = self.pose.process(rgb_frame)
        return results.pose_landmarks

    def release(self):
        """释放资源"""
        pass  # MediaPipe不需要显式释放