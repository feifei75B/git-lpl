import os
import pandas as pd
from point import AgilentPoint
from plot import Plot
import tkinter as tk
import tkinter.filedialog as tkf


class Device(object):
    """器件类"""

    def __init__(self, paths: list, area_cm2, power_mw, wavelength_nm):
        # 构造函数
        self.paths = paths
        self.area_cm2 = area_cm2
        self.power_mw = power_mw
        self.wavelength_nm = wavelength_nm
        self.id = os.path.basename(os.path.dirname(paths[0]))
        self.points = self.get_points_object()
        self.results = self.get_results_df()

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
        return pd.concat([point.get_result_df() for point in self.points], axis=0).reset_index(drop=True)

    def add_dark_line_curves(self, ax, label, colors: list):
        for index, point in enumerate(self.points):
            point.add_dark_line_curve(ax, label, colors[index])

    def add_light_line_curves(self, ax, label, colors: list):
        for index, point in enumerate(self.points):
            point.add_light_line_curve(ax, label, colors[index])

    def add_all_line_curves(self, ax, label, colors: list):
        for index, point in enumerate(self.points):
            point.add_dark_line_curve(ax, label, colors[index])
            point.add_light_line_curve(ax, label, colors[index])

    def add_dark_log_curves(self, ax, label, colors: list):
        for index, point in enumerate(self.points):
            point.add_dark_log_curve(ax, label, colors[index])

    def add_light_log_curves(self, ax, label, colors: list):
        for index, point in enumerate(self.points):
            point.add_light_log_curve(ax, label, colors[index])

    def add_all_log_curves(self, ax, label, colors: list):
        for index, point in enumerate(self.points):
            point.add_dark_log_curve(ax, label, colors[index])
            point.add_light_log_curve(ax, label, colors[index])


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


if __name__ == '__main__':
    root = tk.Tk()
    paths = tkf.askopenfilenames(filetypes=[('Text Files', '*.txt*')])
    device = SiliconDevice(paths, 0.0706858, 0.153, 970)
    print(device.results)
    print(device.id)
    Plot.plot_log_curves(device.id,
                         'all',
                         'Voltage (V)',
                         'Current Density (nA/cm2)',
                         None, None, None, None,
                         [device],
                         [device.id])
    root.mainloop()

