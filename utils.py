import json
import socket
import time
from config import MUSIC_HOST, MUSIC_PORT
import cv2








def send_to_music(action_data):
    """发送动作数据给音乐生成模块"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            data_str = json.dumps(action_data)
            sock.sendto(data_str.encode(), (MUSIC_HOST, MUSIC_PORT))
        return True
    except Exception as e:
        print(f"发送到音乐组失败: {e}")
        return False


def calculate_fps(prev_time):
    """计算并显示帧率"""
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    return fps, prev_time


def draw_debug_info(frame, fps, actions, features):
    """在视频帧上绘制调试信息"""
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    if actions:
        action_text = "Actions: " + ", ".join(actions)
        cv2.putText(frame, action_text, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    if features:
        feature_text = f"Amplitude: {features.get('amplitude', 0):.2f} | Symmetry: {features.get('symmetry', 0):.2f}"
        cv2.putText(frame, feature_text, (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    return frame