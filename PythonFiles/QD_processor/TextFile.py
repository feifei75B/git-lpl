import os
import matplotlib.pyplot as plt
from ExcelFile import PointIVXlsx, PointIVXlsxs
from warnings import filterwarnings

filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def dict_to_list(dic, lis):
    for value in dic.values():
        if isinstance(value, dict):
            dict_to_list(value, lis)
        else:
            lis.append(value)


class ProcessException(Exception):

    def __init__(self):
        super().__init__()


class TextFileInterface(object):

    def get_show_data(self):
        pass

    def write_excel_data(self):
        pass

    def plot_curves(self):
        pass


class PointIVTxt(TextFileInterface):

    def __init__(self, path, power, area, wavelength):
        self.path = path
        self.name = os.path.basename(self.path)
        self.power_mw = power
        self.area_cm2 = area
        self.wavelength_nm = wavelength
        self.dir_path = os.path.dirname(self.path)
        self.device_id = self.get_device_id()
        self.point_num = self.name[0]
        self.data_titles, self.data = self.get_curve_data()
        self.add_current_density()
        self.dark_current_data = self.get_dark_current_data()
        self.light_current_data = self.get_light_current_data()

    def get_device_id(self):
        return os.path.basename(os.path.dirname(self.path))

    def get_curve_data(self):
        with open(self.path, 'r') as text_file:
            data_list = [[value.strip() for value in line.split('\t')] for line in text_file]
        data_titles = data_list.pop(0)
        data = [[row_list[0], float(row_list[1]), float(row_list[2])] for row_list in data_list]
        return data_titles, data

    def get_single_curve_data(self, curve_num):
        for row_index, row_list in enumerate(self.data):
            if row_list[0].startswith(str(curve_num) + '/'):
                single_curve_data = {}
                for column_index, title in enumerate(self.data_titles):
                    if column_index == 0:
                        continue
                    else:
                        data_index = row_index
                        max_row_index = len(self.data) - 1
                        single_curve_data[title] = []
                        while self.data[data_index][0].startswith(str(curve_num) + '/'):
                            single_curve_data[title].append(self.data[data_index][column_index])
                            data_index += 1
                            if data_index > max_row_index:
                                break
                return single_curve_data
        raise ProcessException()

    @staticmethod
    def get_current_density(current_a, area_cm2):
        return current_a * 1e9 / area_cm2

    @staticmethod
    def get_external_quantum_effiency(dark_current_a, light_current_a, power_mw, area_cm2, wavelength_nm):
        return (light_current_a - dark_current_a) * 1240 / (power_mw * 1e-3 * area_cm2 * wavelength_nm)

    def add_current_density(self):
        self.data_titles.append('J (nA/cm2)')
        for row_list in self.data:
            row_list.append(self.get_current_density(row_list[2], self.area_cm2))

    def get_dark_current_data(self):
        return self.get_single_curve_data(1)

    def get_light_current_data(self):
        return self.get_single_curve_data(2)

    def get_certain_jdark(self, voltage_v):
        for index, value in enumerate(self.dark_current_data['V1 (V)']):
            if value == voltage_v:
                return self.dark_current_data['J (nA/cm2)'][index]
        raise ProcessException()

    def get_certain_eqe(self, voltage_v):
        for index, value in enumerate(self.light_current_data['V1 (V)']):
            if value == voltage_v:
                return self.get_external_quantum_effiency(
                    self.dark_current_data['I1 (A)'][index],
                    self.light_current_data['I1 (A)'][index],
                    self.power_mw,
                    self.area_cm2,
                    self.wavelength_nm
                )
        raise ProcessException()

    def plot_dark_curve(self, label_name):
        x = self.dark_current_data['V1 (V)']
        y_dark = list(map(abs, self.dark_current_data['J (nA/cm2)']))
        y_dark.reverse()
        plt.plot(x, y_dark, linewidth=1.5, label=label_name)

    def plot_light_curve(self, label_name):
        x = self.dark_current_data['V1 (V)']
        y_light = list(map(abs, self.light_current_data['J (nA/cm2)']))
        y_light.reverse()
        plt.plot(x, y_light, linewidth=1.5, label=label_name)

    def plot_curves(self):
        plt.figure(self.device_id + ' P' + self.point_num + 'IV curve')
        self.plot_dark_curve('dark')
        self.plot_light_curve('light')
        plt.legend(loc='right')
        plt.yscale('log')
        plt.xlabel('voltage (V)')
        plt.ylabel('current density (nA/cm2)')
        plt.show()

    def get_show_data(self):
        return {
            'point_num': self.point_num,
            '-0.5V': {
                'J (nA/cm2)': '%.3f' % self.get_certain_jdark(0.5),
                'EQE': '%.3f' % self.get_certain_eqe(0.5)
            },
            '-2V': {
                'J (nA/cm2)': '%.3f' % self.get_certain_jdark(2),
                'EQE': '%.3f' % self.get_certain_eqe(2)
            }
        }

    def write_excel_data(self):
        excel = PointIVXlsx(self.path.replace('.txt', '.xlsx'))
        excel.write_data_list(self.data_titles)
        for row_list in self.data:
            excel.write_data_list(row_list)
        excel.set_max_column(len(self.data_titles))
        excel.write_data_dict(self.get_show_data(), 1, 6)
        excel.save()


class PointIVTxts(TextFileInterface):

    def __init__(self, text_files):
        self.text_files = text_files
        self.device_id = text_files[0].device_id

    def get_average_data(self):
        sum_data = [0, 0, 0, 0]
        for text_file in self.text_files:
            sum_data[0] = sum_data[0] + text_file.get_certain_jdark(0.5)
            sum_data[1] = sum_data[1] + text_file.get_certain_eqe(0.5)
            sum_data[2] = sum_data[2] + text_file.get_certain_jdark(2)
            sum_data[3] = sum_data[3] + text_file.get_certain_eqe(2)
        average_data = ['%0.3f' % (data / len(self.text_files)) for data in sum_data]
        average_data.insert(0, 'Ave.')
        return average_data

    def get_show_data(self):
        data_list = []
        for text_file in self.text_files:
            text_file_data = []
            dict_to_list(text_file.get_show_data(), text_file_data)
            data_list.append(text_file_data)
        return data_list

    def plot_dark(self):
        plt.figure(self.device_id + ' dark IV curves')
        for text_file in self.text_files:
            text_file.plot_dark_curve('P' + str(text_file.point_num))
        plt.legend(loc='right')
        plt.yscale('log')
        plt.xlabel('voltage (V)')
        plt.ylabel('dark current density (nA/cm2)')
        plt.show()

    def plot_light(self):
        plt.figure(self.device_id + ' light IV curves')
        for text_file in self.text_files:
            text_file.plot_light_curve('P' + str(text_file.point_num))
        plt.legend(loc='right')
        plt.yscale('log')
        plt.xlabel('voltage (V)')
        plt.ylabel('light current density (nA/cm2)')
        plt.show()

    def plot_all(self):
        plt.figure('IV curves')
        for text_file in self.text_files:
            text_file.plot_dark_curve(text_file.device_id + ' P' + str(text_file.point_num) + ' dark')
            text_file.plot_light_curve(text_file.device_id + ' P' + str(text_file.point_num) + ' light')
        plt.legend(loc='right')
        plt.yscale('log')
        plt.xlabel('voltage (V)')
        plt.ylabel('current density (nA/cm2)')
        plt.show()

    def plot_curves(self):
        plt.figure('IV curves')
        plt.subplot(2, 1, 1)
        for text_file in self.text_files:
            x_dark = text_file.dark_current_data['V1 (V)']
            y_dark = list(map(abs, text_file.dark_current_data['J (nA/cm2)']))
            y_dark.reverse()
            plt.plot(x_dark, y_dark, linewidth=1.5, label='Point ' + text_file.name[0])
        plt.legend(loc='right')
        plt.yscale('log')
        plt.xlabel('voltage (V)')
        plt.ylabel('dark current density (nA/cm2)')
        plt.subplot(2, 1, 2)
        for text_file in self.text_files:
            x_light = text_file.light_current_data['V1 (V)']
            y_light = list(map(abs, text_file.light_current_data['J (nA/cm2)']))
            y_light.reverse()
            plt.plot(x_light, y_light, linewidth=1.5, label='Point ' + text_file.name[0])
        plt.legend(loc='right')
        plt.yscale('log')
        plt.xlabel('voltage (V)')
        plt.ylabel('light current density (nA/cm2)')
        plt.show()

    def write_excel_data(self):
        excel = PointIVXlsxs(self.text_files[0].dir_path, self.text_files[0].device_id)
        excel.write_data_list(['No.', '', '-0.5V', '', '-2V'])
        excel.write_data_list(['', 'J (nA/cm2)', 'EQE', 'J (nA/cm2)', 'EQE'])
        excel.write_show_data(self.get_show_data())
        excel.write_data_list(self.get_average_data())
        excel.save()
