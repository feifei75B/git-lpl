import os
import numpy as np
from Point import Point
from Result import Result
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from pandas import DataFrame, ExcelWriter


class Device(object):
    """器件类"""

    def __init__(self, size, label, data_path, result_path):
        """构造函数，初始化数据路径、电极面积、器件id、数据numpy数组、工作点对象、暗电流数组、最大效率点、整流比"""
        self.result_path = result_path
        self.data_path = data_path
        self.dir_path = os.path.dirname(self.data_path)
        self.size = size
        self.id = str(os.path.basename(self.result_path).split('.')[0])
        self.label = self.get_device_label(label)
        self.result_array = self.get_result_array()
        self.data_array = self.get_data_array()
        self.points = self.get_point_objects()
        # self.dark_point = self.get_dark_point()
        self.max_efficiency_point = self.get_max_efficiency_point()
        self.mean_result = Result(self.get_mean_array())
        self.cv_result = Result(self.get_cv_array())

    def get_device_label(self, label):
        if label == '':
            return self.id
        else:
            return label

    def get_result_array(self) -> np.ndarray:
        """读取性能数据txt，返回numpy数组类型"""
        with open(self.result_path, 'r') as result_file:
            result_file_lines = result_file.readlines()
        result_list = [list(map(float, [value.strip() for value in line.split('\t')][1:-2]))
                       for line in result_file_lines[1:]]
        return np.array(result_list)

    def get_data_array(self) -> np.ndarray:
        """读取曲线数据txt，返回numpy数组类型"""
        with open(self.data_path, 'r') as data_file:
            data_file_lines = data_file.readlines()
        data_list = [[float(value.strip()) for value in line.split('\t')] for line in data_file_lines[2:]]
        return np.array(data_list)

    def get_point_objects(self):
        """返回工作点对象列表"""
        return [Point(index + 1, self.size, self.data_array[:, 2 * index:(2 * index + 2)], point_result)
                for index, point_result in enumerate(self.result_array[:]) if not np.isnan(point_result[7])]  # [:-1]

    # def get_dark_point(self):
    #     """返回暗电流numpy数组"""
    #     return Point('dark', self.size, self.data_array[:, -2:], np.array([]))

    def get_max_efficiency_point(self):
        """按效率大小降序排序工作点，返回最大效率点对象"""
        points_list = list(self.points)
        points_list.sort(key=lambda point: point.result.efficiency, reverse=True)
        return points_list[0]

    # def get_certain_dark_current(self, voltage_v):
    #     """返回特定电压值下暗电流"""
    #     last_v, last_a = self.dark_point.data[0]
    #     for row in self.dark_point.data:
    #         if row[0] <= voltage_v < last_v:
    #             if abs(row[0] - voltage_v) < abs(last_v - voltage_v):
    #                 return row[1]
    #             else:
    #                 return last_a
    #         last_v, last_a = row
    #     return np.nan

    # def get_rectification_ratio(self, voltage_v):
    #     """计算返回整流比"""
    #     return abs(self.get_certain_dark_current(abs(voltage_v)) / self.get_certain_dark_current(-abs(voltage_v)))

    def get_max_list(self):
        """计算返回最大值numpy数组"""
        array = np.array([point.result_array for point in self.points])
        return [np.max(array[:-1, 0]),
                np.max(array[:-1, 2]),
                np.max(array[:-1, 6]),
                np.max(array[:-1, 7])]

    def get_mean_array(self):
        """返回平均值numpy数组"""
        array = np.array([point.result_array for point in self.points])
        return np.mean(array, axis=0)

    def get_cv_array(self):
        """返回变异系数numpy数组"""
        array = np.array([point.result_array for point in self.points])
        return np.std(array, axis=0) / np.mean(array, axis=0)

    def add_device_curve(self, ax, color):
        """添加器件曲线"""
        x = self.max_efficiency_point.voltage_v_data
        y = self.max_efficiency_point.current_density_ma_cm2_data
        # z = self.dark_point.current_density_ma_cm2_data
        ax.plot(x, y, linewidth=2, label=self.label, color=color)
        # ax.plot(x, z, linewidth=4, label=self.label + ' dark', linestyle=':', color=color)

    def export_excel(self, dir_path):
        """数据导出至excel表格"""
        excel_path = dir_path + '\\' + self.id + ' result' + '.xlsx'
        # 数据列表
        result = [point.result.get_show_list() for point in self.points]
        result.append(self.mean_result.get_show_list())
        result.append(self.cv_result.get_show_list())
        result_df = DataFrame(np.array(result))
        # 列标签
        result_df.columns = Result.get_title_list()
        # 行标签
        index = [point.id for point in self.points]
        index.append('Ave.')
        index.append('CV%.')
        result_df.index = index
        # 写入excel表格
        writer = ExcelWriter(excel_path)
        result_df.to_excel(writer, 'Result', float_format='%.5f')
        writer.save()

    def save_as_txt(self, dir_path):
        with open(dir_path + '\\' + self.id + ' result' + '.txt', 'w') as file:
            file.write('\t')
            for value in Result.get_title_list():
                if value == 'Jsc (mA/cm2)':
                    file.write(value + '\t')
                else:
                    file.write(value + '\t\t')
            file.write('\n')
            for point in self.points:
                file.write(str(point.id) + '\t')
                for value in point.result.get_show_list():
                    file.write('{:.3f}'.format(value) + '\t\t')
                file.write('\n')
            file.write('Ave.\t')
            for value in self.mean_result.get_show_list():
                file.write('{:.3f}'.format(value) + '\t\t')
            file.write('\n')
            file.write('CV%.\t')
            for value in self.cv_result.get_show_list():
                file.write('{:.3f}'.format(value) + '\t\t')
            file.write('\n')

    @staticmethod
    def plot_log_curves(title, x_label, y_label, points: list, labels: list):
        """静态方法，画对数曲线"""
        if points:
            plt.figure(title)
            ax = plt.gca()
            for index, point in enumerate(points):
                point.add_log_curve(ax, labels[index])
            ax.axvline(x=0, color='k', linewidth=1)
            ax.legend(loc='upper left', frameon=False)
            ax.set_yscale('log')
            ax.set_xlim(-1, 1)
            ax.xaxis.set_label_text(x_label)
            ax.yaxis.set_label_text(y_label)
            plt.show()

    @staticmethod
    def plot_line_curves(title, x_label, y_label, x_min, x_max, y_min, y_max, points: list, labels: list):
        """静态方法，画工作点JV曲线"""
        if points:
            plt.figure(title)
            ax = plt.gca()
            for index, point in enumerate(points):
                point.add_line_curve(ax, labels[index])
            ax.axhline(y=0, color='k', linewidth=1)
            ax.axvline(x=0, color='k', linewidth=1)
            ax.xaxis.set_major_locator(MultipleLocator(0.1))
            ax.xaxis.set_minor_locator(MultipleLocator(0.05))
            ax.yaxis.set_major_locator(MultipleLocator(10))
            ax.yaxis.set_minor_locator(MultipleLocator(5))
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)
            ax.legend(loc='upper right', frameon=False)
            ax.xaxis.set_label_text(x_label)
            ax.yaxis.set_label_text(y_label)
            plt.show()

    @staticmethod
    def plot_devices_line_curves(title, x_label, y_label, x_min, x_max, y_min, y_max, devices: list):
        """静态方法，画器件JV曲线"""
        if devices:
            color = ['navy', 'orange', 'forestgreen', 'red', 'gray', 'purple']
            plt.figure(title)
            ax = plt.gca()
            for index, device in enumerate(devices):
                device.add_device_curve(ax, color[index])
            ax.axhline(y=0, color='k', linewidth=1)
            ax.axvline(x=0, color='k', linewidth=1)
            ax.xaxis.set_major_locator(MultipleLocator(0.1))
            ax.xaxis.set_minor_locator(MultipleLocator(0.05))
            ax.yaxis.set_major_locator(MultipleLocator(10))
            ax.yaxis.set_minor_locator(MultipleLocator(5))
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)
            ax.legend(loc='upper right', frameon=False)
            ax.xaxis.set_label_text(x_label)
            ax.yaxis.set_label_text(y_label)
            plt.show()


# if __name__ == '__main__':
#     """测试用例"""
#     dev = Device(result_path='F:\\PythonProgram\\solar_cell_processor\\data\\AF1-13.txt',
#                  data_path='F:\\PythonProgram\\solar_cell_processor\\data\\AF1-13 IV Graph.txt', size=0.09, label='')
    # print(dev.id)
    # print(dev.dir_path)
    # print(dev.data_array)
    # print(dev.result_array)
    # for point in dev.points:
    #     print(point.result.efficiency)
    # print(dev.max_efficiency_point.id,
    #       dev.max_efficiency_point.result.oc_voltage_v,
    #       dev.max_efficiency_point.result.sc_current_density_ma_cm2,
    #       dev.max_efficiency_point.result.fill_factor,
    #       dev.max_efficiency_point.result.efficiency,
    #       dev.max_efficiency_point.result.s_resistance_ohms,
    #       dev.max_efficiency_point.result.sh_resistance_ohms)
    # print(dev.max_efficiency_point.data)
    # print(dev.dark_point.data)
    # print(dev.get_certain_dark_current(0.798))
    # print(dev.get_rectification_ratio(0.8))
    # for obj in dev.points:
    #     print(obj.current_density_ma_cm2_data)
    # Device.plot_log_curves(dev.id, 'voltage (V)', 'dark current density(mA/cm2)', [dev.dark_point], ['dark'])
    # Device.plot_line_curves(dev.id, 'voltage (V)', 'current density (mA/cm2)', -0.2, 0.5, -10, 40,
    #                         [dev.max_efficiency_point, dev.dark_point], ['max efficiency curve', 'dark curve'])
    # Device.plot_devices_line_curves(dev.id, 'voltage (V)', 'current density (mA/cm2)', -0.2, 0.5, -10, 40, [dev])
    # print(dev.mean_result.efficiency)
    # print(dev.cv_result.efficiency)
    # dev.export_excel('F:\PythonProgram\solar_cell_processor\data')
    # dev.save_as_txt('F:\PythonProgram\solar_cell_processor\data')
    # print(dev.get_max_list())
