import numpy as np
from Result import Result


class Point(object):
    """工作点类"""
    def __init__(self, point_id, size, data_array: np.ndarray, result_array: np.ndarray):
        # 构造函数
        self.id = point_id
        self.data = data_array
        self.result_array = result_array
        self.voltage_v_data = self.data[:, 0]
        self.current_a_data = self.data[:, 1]
        self.current_density_ma_cm2_data = self.current_a_data * 1e3 / size
        if self.result_array.size != 0:
            self.result = Result(self.result_array)

    def add_line_curve(self, ax, label):
        """添加线性显示曲线"""
        x = self.voltage_v_data
        y = self.current_density_ma_cm2_data
        if self.id == 'dark':
            ax.plot(x, y, linewidth=4, label=label, linestyle=':')
        else:
            ax.plot(x, y, linewidth=2, label=label, linestyle='-')

    def add_log_curve(self, ax, label):
        """添加对数显示曲线"""
        x = self.voltage_v_data
        y = np.abs(self.current_density_ma_cm2_data)
        ax.plot(x, y, linewidth=2, label=label, linestyle='-')
