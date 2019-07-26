import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from device import *
from plot import Plot
from settings import *
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
                '作图': {'Item': ['暗态对数曲线',
                                '光态线性曲线',
                                '器件线性曲线',
                                '暗态对比曲线',
                                '光态对比曲线',
                                '器件对比曲线',
                                '作图设置'],
                       'Command': ['plot_dark_log_curve',
                                   'plot_light_line_curve',
                                   'plot_device_line_curves',
                                   'plot_dark_contrast_curves',
                                   'plot_light_contrast_curves',
                                   'plot_device_contrast_curves',
                                   'plot_settings']
                       },
                '窗口': {'Item': ['语言-简体中文',
                                '语言-英语'],
                       'Command': ['language_simple_chinese',
                                   'language_english']}}
EN_MENU_DICT = {'File': {'Item': ['Open Result.txt',
                                  'Open IV.txt',
                                  'Export Excel File',
                                  'Save As Text File',
                                  'Exit'],
                         'Command': ['open_result_txt',
                                     'open_data_txt',
                                     'export_excel',
                                     'save_as_txt',
                                     'exit_program']},
                'Calculate': {'Item': ['Show Device Result'],
                              'Command': ['show_device_result']},
                'Device': {'Item': ['Add Device',
                                    'Delete Last Device',
                                    'Clear Devices'],
                           'Command': ['add_device',
                                       'delete_last_device',
                                       'clear_devices']},
                'Plot': {'Item': ['Plot Dark Log Curve',
                                  'Plot Light Line Curve',
                                  'Plot Device Line Curves',
                                  'Plot Dark Contrast Curves',
                                  'Plot Light Contrast Curves',
                                  'Plot Device Contrast Curves',
                                  'Plot Settings'],
                         'Command': ['plot_dark_log_curve',
                                     'plot_light_line_curve',
                                     'plot_device_line_curves',
                                     'plot_dark_contrast_curves',
                                     'plot_light_contrast_curves',
                                     'plot_device_contrast_curves',
                                     'plot_settings']
                         },
                'Window': {'Item': ['Language-Simple Chinese',
                                    'Language-English'],
                           'Command': ['language_simple_chinese',
                                       'language_english']}}


class Application(tk.Tk):
    """应用程序类"""

    def __init__(self):
        """构造函数，创建主窗口，初始化窗口控件"""
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
        """创建主窗口"""
        self.title('QDPD Processor')
        self.frm.grid(sticky=tk.W)
        self.frm_welcome.grid(row=0, column=0, padx=15, sticky=tk.W)
        ttk.Label(master=self.frm_info,
                  textvariable=self.tv_info,
                  justify='left',
                  font=('Comic Sans MS', 14, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.frm_result.grid(row=1, column=0, padx=10, sticky=tk.W)

    def add_menu(self, menu_class_name, menu_dict):
        """添加菜单"""
        menu_class_name(self, menu_dict)


class AppMenu(object):
    """菜单类"""

    def __init__(self, root, menu_dict):
        """初始化菜单"""

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
            if (data_path == '' or result_path == '') and key in ('文件', 'File'):
                for i in range(2, 4):
                    menu_var.entryconfig(i, state=tk.DISABLED)
            if (data_path == '' or result_path == '') and key in ('作图', 'Plot'):
                for i in range(0, 6):
                    menu_var.entryconfig(i, state=tk.DISABLED)
            if device_list == [] and key in ('器件', 'Device'):
                for i in range(1, 3):
                    menu_var.entryconfig(i, state=tk.DISABLED)
            # if device_list == [] and key in ('作图', 'Plot'):
            #     for i in range(3, 6):
            #         menu_var.entryconfig(i, state=tk.DISABLED)
            if key in ('作图', 'Plot'):
                menu_var.entryconfig(0, state=tk.DISABLED)
                menu_var.entryconfig(2, state=tk.DISABLED)
                menu_var.entryconfig(3, state=tk.DISABLED)
                if device_list == []:
                    menu_var.entryconfig(4, state=tk.DISABLED)
                menu_var.entryconfig(5, state=tk.DISABLED)
            if key == '窗口':
                menu_var.entryconfig(0, state=tk.DISABLED)
            if key == 'Window':
                menu_var.entryconfig(1, state=tk.DISABLED)
            # 添加菜单到菜单栏
            self.menu_bar.add_cascade(label=key, menu=menu_var)
            # 判断菜单不可用情况
            if (data_path == '' or result_path == '') and \
                    (key in ('计算', 'Calculate', '器件', 'Device')):
                self.menu_bar.entryconfig(key, state=tk.DISABLED)
        # 添加菜单栏到窗口
        root.config(menu=self.menu_bar)
