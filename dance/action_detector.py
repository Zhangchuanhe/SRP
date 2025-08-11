# 基础动作识别（跳跃、旋转等）
from config import JUMP_THRESHOLD, SPIN_THRESHOLD, HANDS_UP_THRESHOLD


class ActionDetector:
    def __init__(self):
        # 状态变量
        self.prev_landmarks = None
        self.hands_up_counter = 0

    def detect_jump(self, landmarks):
        """检测跳跃动作"""
        if landmarks is None or self.prev_landmarks is None:
            return False

        # 获取关键点索引（MediaPipe Pose的索引）
        left_ankle_curr = landmarks.landmark[27]
        right_ankle_curr = landmarks.landmark[28]
        left_ankle_prev = self.prev_landmarks.landmark[27]
        right_ankle_prev = self.prev_landmarks.landmark[28]

        # 计算垂直位移
        left_dy = left_ankle_prev.y - left_ankle_curr.y  # 正值表示向上
        right_dy = right_ankle_prev.y - right_ankle_curr.y

        # 判断是否发生跳跃
        return left_dy > JUMP_THRESHOLD and right_dy > JUMP_THRESHOLD

    def detect_spin(self, landmarks):
        """检测旋转动作"""
        if landmarks is None:
            return False

        left_shoulder = landmarks.landmark[11]
        right_shoulder = landmarks.landmark[12]

        # 计算肩部水平位置差异
        shoulder_diff = abs(left_shoulder.x - right_shoulder.x)
        # 判断是否旋转（差异越大表示旋转角度越大）
        return shoulder_diff > SPIN_THRESHOLD / 100  # 转换为比例

    def detect_hands_up(self, landmarks):
        """检测举手动作"""
        if landmarks is None:
            self.hands_up_counter = 0
            return False

        left_wrist = landmarks.landmark[15]
        left_shoulder = landmarks.landmark[11]
        right_wrist = landmarks.landmark[16]
        right_shoulder = landmarks.landmark[12]

        # 判断手腕是否高于肩膀
        hands_up = (left_wrist.y < left_shoulder.y) or (right_wrist.y < right_shoulder.y)

        if hands_up:
            self.hands_up_counter += 1
            if self.hands_up_counter >= HANDS_UP_THRESHOLD:
                self.hands_up_counter = 0  # 重置计数器
                return True
        else:
            self.hands_up_counter = max(0, self.hands_up_counter - 1)  # 逐渐减少计数器

        return False

    def update_previous(self, landmarks):
        """更新前一帧的姿态数据"""
        self.prev_landmarks = landmarks