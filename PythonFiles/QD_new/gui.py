import sys
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from device import Device, SiliconDevice
from plot import Plot
from settings import ParaSettings, PlotSettings

# 全局变量
device_list = []
legend_list = []
frame_list = []
device_num = 0
delete_buttons = []
pls = PlotSettings()
pas = ParaSettings()
# 菜单字典
CN_MENU_DICT = {'文件': {'Item': ['选择器件数据 (D)',
                                '选择硅片器件数据 (S)',
                                '导出excel文件 (E)',
                                '退出'],
                       'Command': ['select_device_data',
                                   'select_silicon_device_data',
                                   'export_excel',
                                   'exit_program']
                       },
                '器件': {'Item': ['修改图例 (M)',
                                '添加器件 (A)',
                                '删除上一个器件 (Back)',
                                '清空器件 (C)'],
                       'Command': ['modify_legend',
                                   'add_device',
                                   'delete_last_device',
                                   'clear_devices']
                       },
                '作图': {'Item': ['暗态线性曲线 (1)',
                                '光态线性曲线 (2)',
                                '器件线性曲线 (3)',
                                '暗态对数曲线 (4)',
                                '光态对数曲线 (5)',
                                '器件对数曲线 (Space)'],
                       'Command': ['plot_dark_line_curves',
                                   'plot_light_line_curves',
                                   'plot_device_line_curves',
                                   'plot_dark_log_curves',
                                   'plot_light_log_curves',
                                   'plot_device_log_curves']
                       },
                '设置': {'Item': ['参数设置 (O)',
                                '作图设置 (P)'],
                       'Command': ['parameters_settings',
                                   'plot_settings']
                       },
                '窗口': {'Item': ['语言-简体中文',
                                '语言-英语'],
                       'Command': ['language_simple_chinese',
                                   'language_english']
                       }
                }
EN_MENU_DICT = {'File': {'Item': ['Select Device Data (D)',
                                  'Select Silicon Device Data (S)',
                                  'Export Excel File (E)',
                                  'Exit'],
                         'Command': ['select_device_data',
                                     'select_silicon_device_data',
                                     'export_excel',
                                     'exit_program']},
                'Device': {'Item': ['Modify Legend (M)',
                                    'Add Device (A)',
                                    'Delete Last Device (Back)',
                                    'Clear Devices (C)'],
                           'Command': ['modify_legend',
                                       'add_device',
                                       'delete_last_device',
                                       'clear_devices']},
                'Plot': {'Item': ['Plot Dark Line Curves (1)',
                                  'Plot Light Line Curves (2)',
                                  'Plot Device Line Curves (3)',
                                  'Plot Dark Log Curves (4)',
                                  'Plot Light Log Curves (5)',
                                  'Plot Device Log Curves (Space)'],
                         'Command': ['plot_dark_line_curves',
                                     'plot_light_line_curves',
                                     'plot_device_line_curves',
                                     'plot_dark_log_curves',
                                     'plot_light_log_curves',
                                     'plot_device_log_curves']
                         },
                'Settings': {'Item': ['Parameters Settings (O)',
                                      'Plot Settings (P)'],
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
        self.create_window()

    def create_window(self):
        # 创建主窗口
        self.title('QDPD Processor')
        self.frm.grid(sticky=tk.W)
        self.frm_welcome.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(master=self.frm_welcome,
                  textvariable=self.tv_welcome,
                  justify='left',
                  font=('Comic Sans MS', 14, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.frm_result.grid(row=1, column=0, padx=10, sticky=tk.W)

    def add_menu(self, menu_class_name, menu_dict):
        # 添加菜单
        menu_class_name(self, self.frm_result, menu_dict)


class LegendSettingWindow(tk.Toplevel):
    """图例设置窗口类"""
    def __init__(self):
        # 构造函数
        super().__init__()
        self.frm = ttk.Frame(master=self)
        self.tv_legend = tk.StringVar()
        self.create_window()

    def create_window(self):
        # 创建图例设置窗口
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
        self.bind("<Return>", self.legend_setting_save)

    def legend_setting_save(self, event=None):
        # 保存图例设置
        global legend_list
        if len(legend_list) > device_num:
            legend_list[device_num] = self.tv_legend.get()
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
        self.bind("<Return>", self.para_setting_save)
        self.bind("<Escape>", self.para_setting_cancel)
        self.bind("<r>", self.para_setting_reset)
        self.bind("<R>", self.para_setting_reset)

    def set_values(self):
        # 从参数设置中导入参数
        self.tv_area_cm2.set(pas.area_cm2)
        self.tv_power_mw.set(pas.power_mw)
        self.tv_wavelength_nm.set(pas.wavelength_nm)

    def para_setting_save(self, event=None):
        # 保存参数设置
        pas.area_cm2 = float(self.tv_area_cm2.get()) if self.tv_area_cm2.get() else 0.0706858
        pas.power_mw = float(self.tv_power_mw.get()) if self.tv_power_mw.get() else 1
        pas.wavelength_nm = float(self.tv_wavelength_nm.get()) if self.tv_wavelength_nm.get() else 970
        self.destroy()

    def para_setting_cancel(self, event=None):
        # 取消参数设置
        self.destroy()

    def para_setting_reset(self, event=None):
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
        self.bind("<Return>", self.plot_setting_save)
        self.bind("<Escape>", self.plot_setting_cancel)
        self.bind("<r>", self.plot_setting_reset)
        self.bind("<R>", self.plot_setting_reset)

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

    def plot_setting_save(self, event=None):
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

    def plot_setting_cancel(self, event=None):
        # 取消作图设置
        self.destroy()

    def plot_setting_reset(self, event=None):
        # 重置作图设置
        global pls
        pls = PlotSettings()
        self.set_values()


class AppMenu(object):
    """菜单类"""

    def __init__(self, root, frm_result, menu_dict):
        # 初始化菜单
        self.root = root
        self.frm_result = frm_result
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
                menu_var.entryconfig(2, state=tk.DISABLED)
            if not device_list and key in ('器件', 'Device'):
                for i in range(0, 4):
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
        # 快捷键
        self.root.bind("<d>", self.select_device_data)
        self.root.bind("<D>", self.select_device_data)
        self.root.bind("<s>", self.select_silicon_device_data)
        self.root.bind("<S>", self.select_silicon_device_data)
        self.root.bind("<e>", self.export_excel)
        self.root.bind("<E>", self.export_excel)
        self.root.bind("<m>", self.modify_legend)
        self.root.bind("<M>", self.modify_legend)
        self.root.bind("<BackSpace>", self.delete_last_device)
        self.root.bind("<c>", self.clear_devices)
        self.root.bind("<C>", self.clear_devices)
        self.root.bind("<1>", self.plot_dark_line_curves)
        self.root.bind("<2>", self.plot_light_line_curves)
        self.root.bind("<3>", self.plot_device_line_curves)
        self.root.bind("<4>", self.plot_dark_log_curves)
        self.root.bind("<5>", self.plot_light_log_curves)
        self.root.bind("<6>", self.plot_device_log_curves)
        self.root.bind("<space>", self.plot_device_log_curves)
        self.root.bind("<a>", self.add_device)
        self.root.bind("<A>", self.add_device)
        self.root.bind("<Return>", self.add_device)
        self.root.bind("<o>", self.parameters_settings)
        self.root.bind("<O>", self.parameters_settings)
        self.root.bind("<p>", self.plot_settings)
        self.root.bind("<P>", self.plot_settings)
        # 添加菜单栏到窗口
        self.root.config(menu=self.menu_bar)

    def append_device(self, device):
        # 添加器件到列表
        global device_list, legend_list, frame_list, delete_buttons
        if len(device_list) == device_num:
            device_list.append(device)
            legend_list.append(device.id)
            frame_list.append(ttk.Frame(master=self.frm_result))
        else:
            device_list[device_num] = device
            legend_list[device_num] = device.id
            frame_list[device_num].destroy()
            delete_buttons = []
            frame_list[device_num] = ttk.Frame(master=self.frm_result)

    def delete_point(self, point_index):
        # 删除工作点
        global device_num
        device = device_list[device_num].delete_point(point_index)
        if device is not None:
            self.append_device(device)
            self.show_results(device)
        else:
            device_list.pop()
            legend_list.pop()
            frame_list[-1].destroy()
            frame_list.pop()
            device_num = len(device_list)
        self.root.add_menu(AppMenu, self.menu_dict)

    def show_results(self, device):
        # 显示器件结果
        frame = frame_list[device_num]
        frame.grid(row=device_num, pady=5, sticky=tk.W)
        ttk.Label(master=frame,
                  text='Device: ' + device.id,
                  justify='left',
                  font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=5, sticky=tk.W)
        for column, label in enumerate(device.results.columns):
            ttk.Label(master=frame,
                      text=label,
                      justify='center',
                      font=('Arial', 11, '')).grid(row=1, column=column, padx=5, pady=1)
            for index, value in enumerate(device.results[label]):
                if label == 'ID':
                    ttk.Label(master=frame,
                              text=str(value),
                              justify='center',
                              font=('Arial', 11, '')).grid(row=index+2, column=column, padx=2, pady=1)
                else:
                    ttk.Label(master=frame,
                              text='{:.3f}'.format(value),
                              justify='center',
                              font=('Arial', 11, '')).grid(row=index + 2, column=column, padx=2, pady=1)
        for index in range(device.results.shape[0]):
            butt_delete = ttk.Button(master=frame,
                                     text='×',
                                     width=5,
                                     command=lambda point_index=index: self.delete_point(point_index))
            butt_delete.grid(row=index + 2, column=device.results.columns.size, padx=10, pady=1)
            delete_buttons.append(butt_delete)

    def select_device_data(self, event=None):
        # 选择器件数据
        global device_list
        paths = list(filedialog.askopenfilenames(filetypes=[('Text Files', '*.txt*')]))
        if paths:
            device = Device(paths, pas.area_cm2, pas.power_mw, pas.wavelength_nm)
            self.append_device(device)
            self.show_results(device)
        self.root.add_menu(AppMenu, self.menu_dict)

    def select_silicon_device_data(self, event=None):
        # 选择硅片器件数据
        global device_list
        paths = list(filedialog.askopenfilenames(filetypes=[('Text Files', '*.txt*')]))
        if paths:
            silicon_device = SiliconDevice(paths, pas.area_cm2, pas.power_mw, pas.wavelength_nm)
            self.append_device(silicon_device)
            self.show_results(silicon_device)
        self.root.add_menu(AppMenu, self.menu_dict)

    @staticmethod
    def export_excel(event=None):
        # 导出excel
        if device_list:
            excel_path = filedialog.asksaveasfilename(filetypes=[('Excel Files', '*.xlsx')])
            if excel_path:
                if not excel_path.endswith('.xlsx'):
                    excel_path = excel_path + '.xlsx'
                writer = pd.ExcelWriter(excel_path)
                for device in device_list:
                    device.results.to_excel(writer, device.id)
                writer.save()

    @staticmethod
    def exit_program(event=None):
        # 退出
        sys.exit()

    @staticmethod
    def modify_legend(event=None):
        # 修改图例
        LegendSettingWindow()

    def add_device(self, event=None):
        # 添加器件
        global device_num, delete_buttons
        if len(device_list) > device_num:
            device_num = device_num + 1
            for button in delete_buttons:
                button.destroy()
            delete_buttons = []
        self.root.add_menu(AppMenu, self.menu_dict)

    def delete_last_device(self, event=None):
        # 删除上一个器件
        global device_num
        if device_list:
            device_list.pop()
            legend_list.pop()
            frame_list[-1].destroy()
            frame_list.pop()
            device_num = len(device_list)
        self.root.add_menu(AppMenu, self.menu_dict)

    def clear_devices(self, event=None):
        # 清空器件
        global device_list, device_num, legend_list, frame_list
        device_list = []
        legend_list = []
        for frame in frame_list:
            frame.destroy()
        frame_list = []
        device_num = 0
        self.root.add_menu(AppMenu, self.menu_dict)

    @staticmethod
    def plot_dark_line_curves(event=None):
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
    def plot_light_line_curves(event=None):
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
    def plot_device_line_curves(event=None):
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
    def plot_dark_log_curves(event=None):
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
    def plot_light_log_curves(event=None):
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
    def plot_device_log_curves(event=None):
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
    def parameters_settings(event=None):
        # 参数设置
        ParaSettingWindow()

    @staticmethod
    def plot_settings(event=None):
        # 作图设置
        PlotSettingWindow()

    def language_simple_chinese(self, event=None):
        # 语言-简体中文
        self.root.add_menu(AppMenu, CN_MENU_DICT)

    def language_english(self, event=None):
        # 语言-英文
        self.root.add_menu(AppMenu, EN_MENU_DICT)


if __name__ == '__main__':
    app = Application()
    app.add_menu(AppMenu, CN_MENU_DICT)
    app.mainloop()
