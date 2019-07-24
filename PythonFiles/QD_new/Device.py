import os
from Point import AgilentPoint


class Device(object):
    """器件类"""

    def __init__(self, paths: list, area_cm2, power_mw, wavelength_nm):
        # 构造函数
        self.paths = paths
        self.area_cm2 = area_cm2
        self.power_mw = power_mw
        self.wavelength_nm = wavelength_nm
        self.id = os.path.dirname(paths[0])
        self.points = self.get_point_objects()

    @staticmethod
    def get_point_id(path):
        # 获取id
        basename = os.path.basename(path)
        if basename[1].isdigit():
            return int(basename[0:2])
        else:
            return int(basename[0])

    def get_point_objects(self):
        # 获取工作点对象，返回list
        if '.txt' in self.paths[0]:
            return []


class SiliconDevice(Device):
    """硅片器件类"""

    def __init__(self, paths: list, area_cm2, power_mw, wavelength_nm):
        # 构造函数，固定工作点面积
        super().__init__(paths, area_cm2, power_mw, wavelength_nm)
        self.areas_cm2 = [
            0.0706858,
            0.0025,
            0.0001,
            0.000025,
            0.00000225,
            0.00000225,
            0.00000225,
            0.00000225,
            0.00000225,
            0.0706858,
            0.0706858
        ]
