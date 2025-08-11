import cv2
import mediapipe as mp
import numpy as np
import os
import json
from tqdm import tqdm

# 配置路径
VIDEO_DIR = 'dance_videos'
OUTPUT_DIR = 'dance_database'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 初始化MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()


def extract_pose_features(video_path):
    """从视频中提取姿态序列特征"""
    cap = cv2.VideoCapture(video_path)
    features = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 姿态估计
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            # 提取关键点 (髋部、肩部等核心点)
            key_points = []
            for i in [11, 12, 13, 14, 23, 24]:
                lm = results.pose_landmarks.landmark[i]
                key_points.extend([lm.x, lm.y, lm.z])
            features.append(key_points)

    cap.release()
    # 取视频中间段作为代表特征
    mid_idx = len(features) // 2
    return np.array(features[mid_idx])


# 处理所有舞蹈视频
dance_features = []
music_mapping = {}

for idx, video_file in enumerate(tqdm(os.listdir(VIDEO_DIR))):
    if video_file.endswith('.mp4'):
        video_path = os.path.join(VIDEO_DIR, video_file)

        # 提取特征
        features = extract_pose_features(video_path)
        dance_features.append(features)

        # 创建音乐映射 (假设音乐文件同名)
        music_file = os.path.splitext(video_file)[0] + '.wav'
        music_mapping[str(idx)] = os.path.join('music_library', music_file)

# 保存数据库
np.save(os.path.join(OUTPUT_DIR, 'dance_poses.npy'), dance_features)
with open(os.path.join(OUTPUT_DIR, 'music_mapping.json'), 'w') as f:
    json.dump(music_mapping, f)

print(f"数据库构建完成! 共{len(dance_features)}个舞蹈动作")

