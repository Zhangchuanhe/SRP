# 特征提取
import numpy as np


class FeatureExtractor:
    def extract_features(self, landmarks):
        """提取动作特征"""
        if landmarks is None:
            return None

        features = {}

        # 1. 动作幅度（关节移动范围）
        features['amplitude'] = self._calc_amplitude(landmarks)

        # 2. 动作速度（平均位移速度）
        # 注意：需要连续帧数据，这里简化处理
        features['speed'] = 0.0  # 实际实现需要前一帧数据

        # 3. 身体对称性
        features['symmetry'] = self._calc_symmetry(landmarks)

        # 4. 动作类型（由动作检测器提供）
        features['action_type'] = "UNKNOWN"

        return features

    def _calc_amplitude(self, landmarks):
        """计算动作幅度"""
        # 计算关键点之间的最大距离
        min_x = min(lm.x for lm in landmarks.landmark)
        max_x = max(lm.x for lm in landmarks.landmark)
        min_y = min(lm.y for lm in landmarks.landmark)
        max_y = max(lm.y for lm in landmarks.landmark)

        return (max_x - min_x) + (max_y - min_y)

    def _calc_symmetry(self, landmarks):
        """计算身体对称性"""
        # 左侧关键点索引（MediaPipe Pose）
        left_indices = [11, 13, 15, 17, 19, 21]
        # 右侧关键点索引
        right_indices = [12, 14, 16, 18, 20, 22]

        left_positions = np.array([(landmarks.landmark[i].x, landmarks.landmark[i].y)
                                   for i in left_indices])
        right_positions = np.array([(landmarks.landmark[i].x, landmarks.landmark[i].y)
                                    for i in right_indices])

        # 计算镜像位置（关于身体中线）
        mirrored_right = np.copy(right_positions)
        mirrored_right[:, 0] = 1.0 - mirrored_right[:, 0]  # x坐标镜像

        # 计算平均距离误差
        distances = np.linalg.norm(left_positions - mirrored_right, axis=1)
        return 1.0 - np.mean(distances)  # 对称性分数（1表示完全对称）