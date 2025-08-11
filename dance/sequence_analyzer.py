# 动作序列分析
from collections import deque


class SequenceAnalyzer:
    def __init__(self, window_size=10):
        self.action_history = deque(maxlen=window_size)
        self.sequence_patterns = {
            "WAVE": ['HANDS_UP', 'HANDS_DOWN', 'HANDS_UP', 'HANDS_DOWN'],
            "SPIN_JUMP": ['SPIN', 'JUMP']
        }

    def add_action(self, action):
        """添加新动作到历史记录"""
        if action:
            self.action_history.append(action)

    def detect_sequence(self):
        """检测动作序列模式"""
        current_sequence = list(self.action_history)

        for pattern_name, pattern in self.sequence_patterns.items():
            if self._matches_pattern(current_sequence, pattern):
                return pattern_name

        return None

    def _matches_pattern(self, sequence, pattern):
        """检查序列是否匹配模式"""
        # 简化实现：检查模式是否在序列中连续出现
        pattern_length = len(pattern)
        if len(sequence) < pattern_length:
            return False

        # 检查序列的最后部分是否匹配模式
        return sequence[-pattern_length:] == pattern