class PlotSettings(object):
    """作图设置类"""

    def __init__(self):
        """构造函数，初始化结构设置"""
        self.log_x_label = 'voltage (V)'
        self.log_y_label = 'current density (mA/cm2)'
        self.line_x_label = 'voltage (V)'
        self.line_y_label = 'current density (mA/cm2)'
        self.line_x_min = 0
        self.line_x_max = 0.7
        self.line_y_min = 0
        self.line_y_max = 20


class DeviceSettings(object):
    """器件设置类"""

    def __init__(self):
        """构造函数，初始化器件设置"""
        self.id = ''
        self.label = ''
        self.area_cm2 = 0.09
