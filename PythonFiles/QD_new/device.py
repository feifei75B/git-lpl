import os
import re
import pandas as pd
from point import AgilentPoint


class Device(object):
    """器件类"""

    def __init__(self, paths: list, area_cm2, power_mw, wavelength_nm):
        # 构造函数
        self.paths = paths
        self.area_cm2 = area_cm2
        self.power_mw = self.get_power(power_mw)
        self.wavelength_nm = wavelength_nm
        self.id = os.path.basename(os.path.dirname(paths[0]))
        self.points = self.get_points_object()
        self.results = self.get_results_df()

    def get_power(self, power_mw):
        # 获取光功率
        search_obj = re.search(r'\d{8}\s(\d+)', self.paths[0])
        if search_obj:
            return float(search_obj.group().split(' ')[-1]) / 1000
        else:
            return power_mw

    @staticmethod
    def get_point_id(path):
        # 获取id
        basename = os.path.basename(path)
        if basename[1].isdigit():
            return int(basename[0:2])
        else:
            return int(basename[0])

    def get_points_object(self):
        # 获取工作点对象，返回list
        if '.txt' in self.paths[0]:
            return [AgilentPoint(
                path,
                Device.get_point_id(path),
                self.area_cm2,
                self.power_mw,
                self.wavelength_nm
            ) for path in self.paths]

    def get_results_df(self):
        # 获取器件结果dataframe
        return pd.concat([point.get_result_df() for point in self.points], axis=0).reset_index(drop=True)

    def add_dark_line_curves(self, ax, label, colors: list):
        # 添加暗态线性曲线
        for index, point in enumerate(self.points):
            point.add_dark_line_curve(ax, label, colors[index])

    def add_light_line_curves(self, ax, label, colors: list):
        # 添加光态线性曲线
        for index, point in enumerate(self.points):
            point.add_light_line_curve(ax, label, colors[index])

    def add_all_line_curves(self, ax, label, colors: list):
        # 添加器件线性曲线
        for index, point in enumerate(self.points):
            point.add_dark_line_curve(ax, label, colors[index])
            point.add_light_line_curve(ax, label, colors[index])

    def add_dark_log_curves(self, ax, label, colors: list):
        # 添加暗态对数曲线
        for index, point in enumerate(self.points):
            point.add_dark_log_curve(ax, label, colors[index])

    def add_light_log_curves(self, ax, label, colors: list):
        # 添加光态线性曲线
        for index, point in enumerate(self.points):
            point.add_light_log_curve(ax, label, colors[index])

    def add_all_log_curves(self, ax, label, colors: list):
        # 添加器件线性曲线
        for index, point in enumerate(self.points):
            point.add_dark_log_curve(ax, label, colors[index])
            point.add_light_log_curve(ax, label, colors[index])

    def delete_point(self, index):
        # 删除工作点，返回器件对象
        self.paths.pop(index)
        if self.paths:
            return Device(self.paths, self.area_cm2, self.power_mw, self.wavelength_nm)
        else:
            return None


class SiliconDevice(Device):
    """硅片器件类"""

    def __init__(self, paths: list, area_cm2, power_mw, wavelength_nm):
        # 构造函数
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
        super().__init__(paths, area_cm2, power_mw, wavelength_nm)

    def get_points_object(self):
        # 获取工作点对象，返回list
        if '.txt' in self.paths[0]:
            return [AgilentPoint(
                path,
                Device.get_point_id(path),
                self.areas_cm2[Device.get_point_id(path)],
                self.power_mw,
                self.wavelength_nm
            ) for path in self.paths]

    def delete_point(self, index):
        # 删除工作点， 返回器件对象
        self.paths.pop(index)
        if self.paths:
            return SiliconDevice(self.paths, self.area_cm2, self.power_mw, self.wavelength_nm)
        else:
            return None
