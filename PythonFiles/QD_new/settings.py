class PlotSettings(object):
    """作图设置类"""

    def __init__(self):
        # 构造函数
        self.line_x_label = 'Voltage (V)'
        self.line_y_label = 'Current Density (nA/cm2)'
        self.line_x_min = ''
        self.line_x_max = ''
        self.line_y_min = ''
        self.line_y_max = ''
        self.log_x_label = 'Voltage (V)'
        self.log_y_label = 'Current Density (nA/cm2)'
        self.log_x_min = ''
        self.log_x_max = ''
        self.log_y_min = ''
        self.log_y_max = ''


class ParaSettings(object):
    """参数设置类"""

    def __init__(self):
        # 构造函数
        self.area_cm2 = 0.0706858
        self.power_mw = 1
        self.wavelength_nm = 970
