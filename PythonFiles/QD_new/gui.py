import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from device import *
from plot import Plot
from settings import *

# 全局变量
device_list = []
legend_list = []
device_index = 0
pls = PlotSettings()
pas = ParaSettings()
# 菜单字典
CN_MENU_DICT = {'文件': {'Item': ['选择器件数据',
                                '选择硅片器件数据',
                                '导出excel文件',
                                '保存txt文件',
                                '退出'],
                       'Command': ['select_device_data',
                                   'select_silicon_device_data',
                                   'export_excel',
                                   'save_as_txt',
                                   'exit_program']
                       },
                '器件': {'Item': ['添加器件',
                                '删除上一个器件',
                                '清空器件'],
                       'Command': ['add_device',
                                   'delete_last_device',
                                   'clear_devices']
                       },
                '作图': {'Item': ['暗态线性曲线',
                                '光态线性曲线',
                                '器件线性曲线',
                                '暗态对数曲线',
                                '光态对数曲线',
                                '器件对比曲线'],
                       'Command': ['plot_dark_line_curves',
                                   'plot_light_line_curves',
                                   'plot_device_line_curves',
                                   'plot_dark_log_curves',
                                   'plot_light_log_curves',
                                   'plot_device_log_curves']
                       },
                '设置': {'Item': ['参数设置',
                                '作图设置'],
                       'Command': ['parameters_settings',
                                   'plot_settings']
                       },
                '窗口': {'Item': ['语言-简体中文',
                                '语言-英语'],
                       'Command': ['language_simple_chinese',
                                   'language_english']
                       }
                }
EN_MENU_DICT = {'File': {'Item': ['Select Device Data',
                                  'Select Silicon Device Data',
                                  'Export Excel File',
                                  'Save As Text File',
                                  'Exit'],
                         'Command': ['select_device_data',
                                     'select_silicon_device_data',
                                     'export_excel',
                                     'save_as_txt',
                                     'exit_program']},
                'Device': {'Item': ['Add Device',
                                    'Delete Last Device',
                                    'Clear Devices'],
                           'Command': ['add_device',
                                       'delete_last_device',
                                       'clear_devices']},
                'Plot': {'Item': ['Plot Dark Line Curves',
                                  'Plot Light Line Curves',
                                  'Plot Device Line Curves',
                                  'Plot Dark Log Curves',
                                  'Plot Light Log Curves',
                                  'Plot Device Log Curves'],
                         'Command': ['plot_dark_line_curves',
                                     'plot_light_line_curves',
                                     'plot_device_line_curves',
                                     'plot_dark_log_curves',
                                     'plot_light_log_curves',
                                     'plot_device_log_curves']
                         },
                'Settings': {'Item': ['Parameters Settings',
                                      'Plot Settings'],
                             'Command': ['parameters_settings',
                                         'plot_settings']
                             },
                'Window': {'Item': ['Language-Simple Chinese',
                                    'Language-English'],
                           'Command': ['language_simple_chinese',
                                       'language_english']
                           }
                }


class Application(tk.Tk):
    """应用程序类"""

    def __init__(self):
        # 构造函数，创建主窗口，初始化窗口控件
        super().__init__()
        # 主框架
        self.frm = ttk.Frame(master=self)
        # 欢迎框架
        self.frm_welcome = ttk.Frame(master=self.frm)
        self.tv_welcome = tk.StringVar(value='Thanks for using! Please select IV files')
        # 结果框架
        self.frm_result = ttk.Frame(master=self.frm)
        self.frm_list = []
        self.create_window()

    def create_window(self):
        # 创建主窗口
        self.title('QDPD Processor')
        self.frm.grid(sticky=tk.W)
        self.frm_welcome.grid(row=0, column=0, padx=15, sticky=tk.W)
        ttk.Label(master=self.frm_welcome,
                  textvariable=self.tv_welcome,
                  justify='left',
                  font=('Comic Sans MS', 14, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.frm_result.grid(row=1, column=0, padx=10, sticky=tk.W)

    def add_menu(self, menu_class_name, menu_dict):
        # 添加菜单
        menu_class_name(self, menu_dict)


class LegendSettingWindow(tk.Toplevel):
    """图例设置窗口类"""
    def __init__(self):
        # 构造函数
        super().__init__()
        self.frm = ttk.Frame(master=self)
        self.tv_legend = tk.StringVar()
        self.legend = ''
        self.create_window()

    def create_window(self):
        self.title('图例设置 Legend Setting')
        self.focus_set()
        self.frm.grid()
        ttk.Label(master=self.frm,
                  text='图例 Legend',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master=self.frm,
                  textvariable=self.tv_legend,
                  justify='right').grid(row=0, column=1, pady=5, sticky=tk.W)
        ttk.Button(self.frm,
                   text='SAVE',
                   command=self.legend_setting_save).grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

    def legend_setting_save(self):
        self.legend = self.tv_legend.get()
        self.destroy()


class ParaSettingWindow(tk.Toplevel):
    """参数设置窗口类"""

    def __init__(self):
        # 构造函数
        super().__init__()
        self.frm = ttk.Frame(master=self)
        self.frm_setting = ttk.Frame(master=self.frm)
        self.frm_para_setting_btn = ttk.Frame(master=self.frm)
        self.tv_area_cm2 = tk.StringVar(value=pas.area_cm2)
        self.tv_power_mw = tk.StringVar(value=pas.power_mw)
        self.tv_wavelength_nm = tk.StringVar(value=pas.wavelength_nm)
        self.create_window()

    def create_window(self):
        # 创建参数设置窗口
        self.title('参数设置 Parameters Settings')
        self.focus_set()
        self.frm.grid(sticky=tk.W)
        self.frm_setting.grid(row=0, sticky=tk.W)
        ttk.Label(self.frm_setting,
                  text='电极面积 Electrode Area',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master=self.frm_setting,
                  textvariable=self.tv_area_cm2,
                  justify='right').grid(row=0, column=1, pady=5, sticky=tk.W)
        ttk.Label(self.frm_setting,
                  text='(cm2)',
                  justify='left').grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.frm_setting,
                  text='光源功率 Light Power',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master=self.frm_setting,
                  textvariable=self.tv_power_mw,
                  justify='right').grid(row=1, column=1, pady=5, sticky=tk.W)
        ttk.Label(self.frm_setting,
                  text='(mW)',
                  justify='left').grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.frm_setting,
                  text='光源波长 Light Wavelength',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master=self.frm_setting,
                  textvariable=self.tv_wavelength_nm,
                  justify='right').grid(row=2, column=1, pady=5, sticky=tk.W)
        ttk.Label(self.frm_setting,
                  text='(nm)',
                  justify='left').grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        self.frm_para_setting_btn.grid(row=1, sticky=tk.W)
        ttk.Button(self.frm_para_setting_btn,
                   text='SAVE',
                   command=self.para_setting_save).grid(row=0, column=0, padx=5, pady=10)
        ttk.Button(self.frm_para_setting_btn,
                   text='CANCEL',
                   command=self.para_setting_cancel).grid(row=0, column=1, padx=5, pady=10)
        ttk.Button(self.frm_para_setting_btn,
                   text='RESET',
                   command=self.para_setting_reset).grid(row=0, column=2, padx=5, pady=10)

    def set_values(self):
        # 从参数设置中导入参数
        self.tv_area_cm2.set(pas.area_cm2)
        self.tv_power_mw.set(pas.power_mw)
        self.tv_wavelength_nm.set(pas.wavelength_nm)

    def para_setting_save(self):
        # 保存参数设置
        pas.area_cm2 = float(self.tv_area_cm2.get()) if self.tv_area_cm2.get() else 0.0706858
        pas.power_mw = float(self.tv_power_mw.get()) if self.tv_power_mw.get() else 1
        pas.wavelength_nm = float(self.tv_wavelength_nm.get()) if self.tv_wavelength_nm.get() else 970
        self.destroy()

    def para_setting_cancel(self):
        # 取消参数设置
        self.destroy()

    def para_setting_reset(self):
        # 重置参数设置
        global pas
        pas = ParaSettings()
        self.set_values()


class PlotSettingWindow(tk.Toplevel):
    """作图设置窗口类"""

    def __init__(self):
        # 构造函数，创建作图设置窗口，初始化窗口控件
        super().__init__()
        self.frm = ttk.Frame(master=self)
        self.frm_line_setting = ttk.Frame(master=self.frm)
        self.frm_log_setting = ttk.Frame(master=self.frm)
        self.frm_plot_setting_btn = ttk.Frame(master=self.frm)
        self.tv_line_x_label = tk.StringVar(value=pls.line_x_label)
        self.tv_line_y_label = tk.StringVar(value=pls.line_y_label)
        self.tv_line_x_min = tk.StringVar(value=pls.line_x_min)
        self.tv_line_x_max = tk.StringVar(value=pls.line_x_max)
        self.tv_line_y_min = tk.StringVar(value=pls.line_y_min)
        self.tv_line_y_max = tk.StringVar(value=pls.line_y_max)
        self.tv_log_x_label = tk.StringVar(value=pls.log_x_label)
        self.tv_log_y_label = tk.StringVar(value=pls.log_y_label)
        self.tv_log_x_min = tk.StringVar(value=pls.log_x_min)
        self.tv_log_x_max = tk.StringVar(value=pls.log_x_max)
        self.tv_log_y_min = tk.StringVar(value=pls.log_y_min)
        self.tv_log_y_max = tk.StringVar(value=pls.log_y_max)
        self.create_window()

    def create_window(self):
        # 创建作图设置窗口
        self.title('作图设置 Plot Settings')
        self.focus_set()
        self.frm.grid(sticky=tk.W)
        self.frm_line_setting.grid(row=0, sticky=tk.W)
        ttk.Label(master=self.frm_line_setting,
                  text='线性曲线 Line Curve',
                  font=('Arial', 10, 'bold'),
                  justify='left').grid(row=0, column=0, columnspan=5, sticky=tk.W)
        ttk.Label(self.frm_line_setting,
                  text='x轴标签 Label X',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master=self.frm_line_setting,
                  textvariable=self.tv_line_x_label,
                  justify='right',
                  width=22).grid(row=1, column=1, columnspan=4, pady=5, sticky=tk.W)
        ttk.Label(self.frm_line_setting,
                  text='y轴标签 Label Y',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master=self.frm_line_setting,
                  textvariable=self.tv_line_y_label,
                  justify='right',
                  width=22).grid(row=2, column=1, columnspan=4, pady=5, sticky=tk.W)
        ttk.Label(self.frm_line_setting,
                  text='x轴坐标范围 Range X',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master=self.frm_line_setting,
                  textvariable=self.tv_line_x_min,
                  justify='right',
                  width=10).grid(row=3, column=1)
        ttk.Label(self.frm_line_setting,
                  text='-',
                  font=('Arial', 9, '')).grid(row=3, column=2, pady=5)
        ttk.Entry(master=self.frm_line_setting,
                  textvariable=self.tv_line_x_max,
                  justify='right',
                  width=10).grid(row=3, column=3)
        ttk.Label(self.frm_line_setting,
                  text='(V)',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=3, column=4)
        ttk.Label(self.frm_line_setting,
                  text='y轴坐标范围 Range Y',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master=self.frm_line_setting,
                  textvariable=self.tv_line_y_min,
                  justify='right',
                  width=10).grid(row=4, column=1)
        ttk.Label(self.frm_line_setting,
                  text='-',
                  font=('Arial', 9, '')).grid(row=4, column=2, pady=5)
        ttk.Entry(master=self.frm_line_setting,
                  textvariable=self.tv_line_y_max,
                  justify='right',
                  width=10).grid(row=4, column=3)
        ttk.Label(self.frm_line_setting,
                  text='(mA/cm2)',
                  justify='left').grid(row=4, column=4, padx=5, pady=5)
        self.frm_log_setting.grid(row=1, sticky=tk.W)
        ttk.Label(self.frm_log_setting,
                  text='对数曲线 Log Curve',
                  font=('Arial', 10, 'bold'),
                  justify='left').grid(row=0, column=0, columnspan=5, sticky=tk.W)
        ttk.Label(self.frm_log_setting,
                  text='x轴标签 Label X',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master=self.frm_log_setting,
                  textvariable=self.tv_log_x_label,
                  justify='right',
                  width=22).grid(row=1, column=1, columnspan=4, pady=5, sticky=tk.W)
        ttk.Label(self.frm_log_setting,
                  text='y轴标签 Label Y',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master=self.frm_log_setting,
                  textvariable=self.tv_log_y_label,
                  justify='right',
                  width=22).grid(row=2, column=1, columnspan=4, pady=5, sticky=tk.W)
        ttk.Label(self.frm_log_setting,
                  text='x轴坐标范围 Range X',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master=self.frm_log_setting,
                  textvariable=self.tv_log_x_min,
                  justify='right',
                  width=10).grid(row=3, column=1)
        ttk.Label(self.frm_log_setting,
                  text='-',
                  font=('Arial', 9, '')).grid(row=3, column=2, pady=5)
        ttk.Entry(master=self.frm_log_setting,
                  textvariable=self.tv_log_x_max,
                  justify='right',
                  width=10).grid(row=3, column=3)
        ttk.Label(self.frm_log_setting,
                  text='(V)',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=3, column=4)
        ttk.Label(self.frm_log_setting,
                  text='y轴坐标范围 Range Y',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master=self.frm_log_setting,
                  textvariable=self.tv_log_y_min,
                  justify='right',
                  width=10).grid(row=4, column=1)
        ttk.Label(self.frm_log_setting,
                  text='-',
                  font=('Arial', 9, '')).grid(row=4, column=2, pady=5)
        ttk.Entry(master=self.frm_log_setting,
                  textvariable=self.tv_log_y_max,
                  justify='right',
                  width=10).grid(row=4, column=3)
        ttk.Label(self.frm_log_setting,
                  text='(mA/cm2)',
                  justify='left').grid(row=4, column=4, padx=5, pady=5)
        self.frm_plot_setting_btn.grid(row=2, padx=40, sticky=tk.W)
        ttk.Button(self.frm_plot_setting_btn,
                   text='SAVE',
                   command=self.plot_setting_save).grid(row=0, column=0, padx=5, pady=10)
        ttk.Button(self.frm_plot_setting_btn,
                   text='CANCEL',
                   command=self.plot_setting_cancel).grid(row=0, column=1, padx=5, pady=10)
        ttk.Button(self.frm_plot_setting_btn,
                   text='RESET',
                   command=self.plot_setting_reset).grid(row=0, column=2, padx=5, pady=10)

    def set_values(self):
        # 从作图设置中导入参数
        self.tv_line_x_label.set(pls.line_x_label)
        self.tv_line_y_label.set(pls.line_y_label)
        self.tv_line_x_min.set(pls.line_x_min)
        self.tv_line_x_max.set(pls.line_x_max)
        self.tv_line_y_min.set(pls.line_y_min)
        self.tv_line_y_max.set(pls.line_y_max)
        self.tv_log_x_label.set(pls.log_x_label)
        self.tv_log_y_label.set(pls.log_y_label)
        self.tv_log_x_min.set(pls.log_x_min)
        self.tv_log_x_max.set(pls.log_x_max)
        self.tv_log_y_min.set(pls.log_y_min)
        self.tv_log_y_max.set(pls.log_y_max)

    def plot_setting_save(self):
        # 保存作图设置
        pls.line_x_label = self.tv_line_x_label.get()
        pls.line_y_label = self.tv_line_y_label.get()
        pls.line_x_min = float(self.tv_line_x_min.get()) if self.tv_line_x_min.get() else ''
        pls.line_x_max = float(self.tv_line_x_max.get()) if self.tv_line_x_max.get() else ''
        pls.line_y_min = float(self.tv_line_y_min.get()) if self.tv_line_y_min.get() else ''
        pls.line_y_max = float(self.tv_line_y_max.get()) if self.tv_line_y_max.get() else ''
        pls.log_x_label = self.tv_log_x_label.get()
        pls.log_y_label = self.tv_log_y_label.get()
        pls.log_x_min = float(self.tv_log_x_min.get()) if self.tv_log_x_min.get() else ''
        pls.log_x_max = float(self.tv_log_x_max.get()) if self.tv_log_x_max.get() else ''
        pls.log_y_min = float(self.tv_log_y_min.get()) if self.tv_log_y_min.get() else ''
        pls.log_y_max = float(self.tv_log_y_max.get()) if self.tv_log_y_max.get() else ''
        self.destroy()

    def plot_setting_cancel(self):
        # 取消作图设置
        self.destroy()

    def plot_setting_reset(self):
        # 重置作图设置
        global pls
        pls = PlotSettings()
        self.set_values()


class AppMenu(object):
    """菜单类"""

    def __init__(self, root, menu_dict):
        # 初始化菜单
        self.root = root
        self.menu_bar = tk.Menu(self.root)  # 创建菜单栏
        self.menu_dict = menu_dict
        for key, value in self.menu_dict.items():
            # 循环创建菜单
            menu_var = tk.Menu(self.menu_bar, tearoff=0)
            for index, item in enumerate(value['Item']):
                # 循环创建菜单项
                menu_var.add_command(label=item, command=getattr(self, value['Command'][index]))
            # 判断菜单项不可用情况
            if not device_list and key in ('文件', 'File'):
                for i in range(2, 4):
                    menu_var.entryconfig(i, state=tk.DISABLED)
            if not device_list and key in ('器件', 'Device'):
                for i in range(1, 3):
                    menu_var.entryconfig(i, state=tk.DISABLED)
            if not device_list and key in ('作图', 'Plot'):
                for i in range(0, 6):
                    menu_var.entryconfig(i, state=tk.DISABLED)
            if key == '窗口':
                menu_var.entryconfig(0, state=tk.DISABLED)
            if key == 'Window':
                menu_var.entryconfig(1, state=tk.DISABLED)
            # 添加菜单到菜单栏
            self.menu_bar.add_cascade(label=key, menu=menu_var)
            # 判断菜单不可用情况
            if not device_list and (key in ('器件', 'Device', '作图', 'Plot')):
                self.menu_bar.entryconfig(key, state=tk.DISABLED)
        # 添加菜单栏到窗口
        self.root.config(menu=self.menu_bar)

    def select_device_data(self):
        # 选择器件数据
        global device_list
        paths = filedialog.askopenfilenames(filetypes=[('Text Files', '*.txt*')])
        if paths:
            device = Device(paths, pas.area_cm2, pas.power_mw, pas.wavelength_nm)
            device_list.append(device)
            legend_setting = LegendSettingWindow()
            self.root.wait_window(legend_setting)
            if legend_setting.legend:
                legend_list.append(legend_setting.legend)
            else:
                legend_list.append(device.id)
        self.root.add_menu(AppMenu, self.menu_dict)

    def select_silicon_device_data(self):
        # 选择硅片器件数据
        global device_list
        paths = filedialog.askopenfilenames(filetypes=[('Text Files', '*.txt*')])
        if paths:
            silicon_device = SiliconDevice(paths, pas.area_cm2, pas.power_mw, pas.wavelength_nm)
            device_list.append(silicon_device)
            legend_setting = LegendSettingWindow()
            self.root.wait_window(legend_setting)
            if legend_setting.legend:
                legend_list.append(legend_setting.legend)
            else:
                legend_list.append(silicon_device.id)
        self.root.add_menu(AppMenu, self.menu_dict)

    @staticmethod
    def export_excel():
        # 导出excel
        pass

    @staticmethod
    def save_as_txt():
        # 保存txt
        pass

    @staticmethod
    def exit_program():
        # 退出
        sys.exit()

    def add_device(self):
        # 添加器件
        global device_index
        if len(device_list) > device_index:
            device_index = device_index + 1
        self.root.add_menu(AppMenu, self.menu_dict)

    def delete_last_device(self):
        # 删除上一个器件
        global device_index
        if device_list:
            device_list.pop()
            legend_list.pop()
            device_index = len(device_list)
        self.root.add_menu(AppMenu, self.menu_dict)

    def clear_devices(self):
        # 清空器件
        global device_list, device_index, legend_list
        device_list = []
        legend_list = []
        device_index = 0
        self.root.add_menu(AppMenu, self.menu_dict)

    @staticmethod
    def plot_dark_line_curves():
        # 作暗态线性曲线
        if device_list:
            Plot.plot_line_curves('Dark Line Curves',
                                  'dark',
                                  pls.line_x_label,
                                  pls.line_y_label,
                                  pls.line_x_min,
                                  pls.line_x_max,
                                  pls.line_y_min,
                                  pls.line_y_max,
                                  device_list,
                                  legend_list)

    @staticmethod
    def plot_light_line_curves():
        # 作光态线性曲线
        if device_list:
            Plot.plot_line_curves('Light Line Curves',
                                  'light',
                                  pls.line_x_label,
                                  pls.line_y_label,
                                  pls.line_x_min,
                                  pls.line_x_max,
                                  pls.line_y_min,
                                  pls.line_y_max,
                                  device_list,
                                  legend_list)

    @staticmethod
    def plot_device_line_curves():
        # 作器件线性曲线
        if device_list:
            Plot.plot_line_curves('Device Line Curves',
                                  'all',
                                  pls.line_x_label,
                                  pls.line_y_label,
                                  pls.line_x_min,
                                  pls.line_x_max,
                                  pls.line_y_min,
                                  pls.line_y_max,
                                  device_list,
                                  legend_list)

    @staticmethod
    def plot_dark_log_curves():
        # 作暗态对数曲线
        if device_list:
            Plot.plot_log_curves('Dark Log Curves',
                                 'dark',
                                 pls.log_x_label,
                                 pls.log_y_label,
                                 pls.log_x_min,
                                 pls.log_x_max,
                                 pls.log_y_min,
                                 pls.log_y_max,
                                 device_list,
                                 legend_list)

    @staticmethod
    def plot_light_log_curves():
        # 作光态对数曲线
        if device_list:
            Plot.plot_log_curves('Light Log Curves',
                                 'light',
                                 pls.log_x_label,
                                 pls.log_y_label,
                                 pls.log_x_min,
                                 pls.log_x_max,
                                 pls.log_y_min,
                                 pls.log_y_max,
                                 device_list,
                                 legend_list)

    @staticmethod
    def plot_device_log_curves():
        # 作光态对数曲线
        if device_list:
            Plot.plot_log_curves('Light Log Curves',
                                 'all',
                                 pls.log_x_label,
                                 pls.log_y_label,
                                 pls.log_x_min,
                                 pls.log_x_max,
                                 pls.log_y_min,
                                 pls.log_y_max,
                                 device_list,
                                 legend_list)

    @staticmethod
    def parameters_settings():
        # 参数设置
        ParaSettingWindow()

    @staticmethod
    def plot_settings():
        # 作图设置
        PlotSettingWindow()

    def language_simple_chinese(self):
        # 语言-简体中文
        self.root.add_menu(AppMenu, CN_MENU_DICT)

    def language_english(self):
        # 语言-英文
        self.root.add_menu(AppMenu, EN_MENU_DICT)


if __name__ == '__main__':
    app = Application()
    app.add_menu(AppMenu, CN_MENU_DICT)
    app.mainloop()
