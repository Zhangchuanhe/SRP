# 摄像头配置
CAMERA_SOURCE = 0  # 默认摄像头
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# 动作检测配置
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7

# 动作识别阈值
JUMP_THRESHOLD = 0.05  # 跳跃检测阈值
SPIN_THRESHOLD = 15    # 旋转角度阈值(度)
HANDS_UP_THRESHOLD = 10  # 连续帧数阈值

# 音乐接口配置
MUSIC_HOST = '127.0.0.1'  # 音乐组程序运行的IP
MUSIC_PORT = 12345        # 音乐组程序监听的端口