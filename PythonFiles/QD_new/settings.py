class PlotSettings(object):
    """作图设置类"""

    def __init__(self):
        # 构造函数
        self.log_x_label = 'Voltage (V)'
        self.log_y_label = 'Current Density (nA/cm2)'
        self.line_x_label = 'Voltage (V)'
        self.line_y_label = 'Current Density (nA/cm2)'
        self.line_x_min = None
        self.line_x_max = None
        self.line_y_min = None
        self.line_y_max = None


class LightSettings(object):
    """光源设置类"""

    def __init__(self):
        # 构造函数
        self.power_mw = 1
        self.wavelength_nm = 970


class DeviceSettings(object):
    """器件设置类"""

    def __init__(self):
        # 构造函数
        self.id = ''
        self.label = ''
        self.area_cm2 = 0.0706858
