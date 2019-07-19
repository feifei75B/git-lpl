import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from Device import Device
from Settings import PlotSettings, DeviceSettings
from Result import Result


# 全局变量
device = None
result_path = ''
data_path = ''
device_list = []
label_list = []
ps = PlotSettings()
ds = DeviceSettings()
# 菜单字典
CN_MENU_DICT = {'文件': {'Item': ['打开结果txt文件',
                                '打开IV txt文件',
                                '导出excel文件',
                                '保存txt文件',
                                '退出'],
                       'Command': ['open_result_txt',
                                   'open_data_txt',
                                   'export_excel',
                                   'save_as_txt',
                                   'exit_program']
                       },
                '计算': {'Item': ['显示器件结果'],
                       'Command': ['show_device_result']
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


# 全局函数
def get_device():
    """创建器件对象"""
    global device
    if data_path != '' and result_path != '':
        device = Device(ds.area_cm2, ds.label, data_path, result_path)
        return True
    else:
        return False


class Application(tk.Tk):
    """应用程序类"""

    def __init__(self):
        """构造函数，创建主窗口，初始化窗口控件"""
        super().__init__()
        # 主框架
        self.frm = ttk.Frame(master=self)
        # 消息框架
        self.frm_info = ttk.Frame(master=self.frm)
        self.tv_info = tk.StringVar(value='Thanks for using! Please select text files')
        # 设置框架
        self.frm_setting = ttk.Frame(master=self.frm)
        # 器件设置输入框架
        self.frm_device_setting = ttk.Frame(master=self.frm_setting)
        self.tv_device_id = tk.StringVar(value=ds.id)
        self.tv_device_label = tk.StringVar(value=ds.label)
        self.tv_device_area_cm2 = tk.StringVar(value=ds.area_cm2)
        # 器件设置按钮框架
        self.frm_device_setting_btn = ttk.Frame(master=self.frm_setting)
        # 结果框架
        self.frm_result = ttk.Frame(master=self.frm)
        # 最大值框架
        self.frm_max = ttk.Frame(master=self.frm_result)
        self.tv_max_v_oc = tk.StringVar()
        self.tv_max_j_sc = tk.StringVar()
        self.tv_max_ff = tk.StringVar()
        self.tv_max_eff = tk.StringVar()
        # 整流比框架
        self.frm_rr = ttk.Frame(master=self.frm_result)
        self.tv_v_rr = tk.StringVar(value=0.8)
        self.tv_rr = tk.StringVar()
        # 器件全结果框架
        self.frm_all_result = ttk.Frame(master=self.frm)
        # 器件工作点框架
        self.frm_points = ttk.Frame(master=self.frm_all_result)
        self.frm_points_list = ttk.Frame(master=self.frm_points)
        # 器件最大效率点框架
        self.frm_max_eff_result = ttk.Frame(master=self.frm_all_result)
        # 器件平均值框架
        self.frm_ave_result = ttk.Frame(master=self.frm_all_result)
        # 器件变异系数框架
        self.frm_cv_result = ttk.Frame(master=self.frm_all_result)
        self.create_window()

    def create_window(self):
        """创建主窗口"""
        self.title('SC Processor')
        # self.geometry('600x650+300+150')
        self.frm.grid(sticky=tk.W)
        self.frm_info.grid(row=0, column=0, padx=15, sticky=tk.W)
        ttk.Label(master=self.frm_info,
                  textvariable=self.tv_info,
                  justify='left',
                  font=('Comic Sans MS', 14, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.frm_setting.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky=tk.W)
        ttk.Label(master=self.frm_setting,
                  text='设置 Settings',
                  justify='left',
                  font=('Arial', 10, 'bold')).grid(row=0, column=0, pady=5, sticky=tk.W)
        self.frm_device_setting.grid(row=1, column=0, sticky=tk.W)
        ttk.Label(master=self.frm_device_setting,
                  text='编号 ID',
                  justify='left',
                  font=('Arial', 10, '')).grid(row=0, column=0, padx=5, sticky=tk.W)
        ttk.Entry(master=self.frm_device_setting,
                  textvariable=self.tv_device_id,
                  justify='right',
                  width=8).grid(row=0, column=1, padx=5)
        ttk.Label(master=self.frm_device_setting,
                  text='图例 Label',
                  justify='left',
                  font=('Arial', 10, '')).grid(row=1, column=0, padx=5, sticky=tk.W)
        ttk.Entry(master=self.frm_device_setting,
                  textvariable=self.tv_device_label,
                  justify='right',
                  width=8).grid(row=1, column=1, padx=5)
        ttk.Label(master=self.frm_device_setting,
                  text='面积 Area',
                  justify='left',
                  font=('Arial', 10, '')).grid(row=2, column=0, padx=5, sticky=tk.W)
        ttk.Entry(master=self.frm_device_setting,
                  textvariable=self.tv_device_area_cm2,
                  justify='right',
                  width=8).grid(row=2, column=1, padx=5)
        self.frm_device_setting_btn.grid(row=2, column=0, padx=20, pady=5)
        ttk.Button(master=self.frm_device_setting_btn,
                   text='SAVE',
                   command=self.device_setting_save,
                   width=5).grid(row=0, column=0, padx=5)
        ttk.Button(master=self.frm_device_setting_btn,
                   text='RESET',
                   command=self.device_setting_reset,
                   width=5).grid(row=0, column=1, padx=5)
        self.frm_result.grid(row=1, column=0, padx=10, sticky=tk.W)
        self.frm_max.grid(row=0, column=0, sticky=tk.W)
        ttk.Label(master=self.frm_max,
                  text='最大值 Max',
                  justify='left',
                  font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(master=self.frm_max,
                   text='GET',
                   command=self.get_max,
                   width=5).grid(row=0, column=1)
        ttk.Label(master=self.frm_max,
                  text='Voc (V)',
                  justify='left',
                  font=('Arial', 10, '')).grid(row=1, column=0, padx=5, sticky=tk.W)
        ttk.Entry(master=self.frm_max,
                  textvariable=self.tv_max_v_oc,
                  justify='right',
                  width=8).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(master=self.frm_max,
                  text='FF',
                  justify='left',
                  font=('Arial', 10, '')).grid(row=1, column=2, padx=5, sticky=tk.W)
        ttk.Entry(master=self.frm_max,
                  textvariable=self.tv_max_ff,
                  justify='right',
                  width=8).grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
        ttk.Label(master=self.frm_max,
                  text='Jsc (mA/cm2)',
                  justify='left',
                  font=('Arial', 10, '')).grid(row=2, column=0, padx=5, sticky=tk.W)
        ttk.Entry(master=self.frm_max,
                  textvariable=self.tv_max_j_sc,
                  justify='right',
                  width=8).grid(row=2, column=1, padx=5, sticky=tk.W)
        ttk.Label(master=self.frm_max,
                  text='η',
                  justify='left',
                  font=('Arial', 10, '')).grid(row=2, column=2, padx=5, sticky=tk.W)
        ttk.Entry(master=self.frm_max,
                  textvariable=self.tv_max_eff,
                  justify='right',
                  width=8).grid(row=2, column=3, padx=5, sticky=tk.W)
        self.frm_rr.grid(row=0, column=1, sticky=tk.W)
        ttk.Label(master=self.frm_rr,
                  text='整流比 RR',
                  justify='left',
                  font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(master=self.frm_rr,
                   text='GET',
                   command=self.get_rr,
                   width=5).grid(row=0, column=1)
        ttk.Label(master=self.frm_rr,
                  text='电压 V (V)',
                  justify='left',
                  font=('Arial', 10, '')).grid(row=1, column=0, padx=5, sticky=tk.W)
        ttk.Entry(master=self.frm_rr,
                  textvariable=self.tv_v_rr,
                  justify='right',
                  width=8).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(master=self.frm_rr,
                  text='整流比 RR',
                  justify='left',
                  font=('Arial', 10, '')).grid(row=2, column=0, padx=5, sticky=tk.W)
        ttk.Entry(master=self.frm_rr,
                  textvariable=self.tv_rr,
                  justify='right',
                  width=8).grid(row=2, column=1, padx=5)
        self.frm_all_result.grid(row=2, column=0, columnspan=2, padx=10, sticky=tk.W)
        self.frm_points.grid(row=0, column=0, sticky=tk.W)
        ttk.Label(master=self.frm_points,
                  text='器件结果 Points Result',
                  justify='left',
                  font=('Arial', 10, 'bold')).grid(row=0, column=0, pady=5, sticky=tk.W)
        ttk.Button(master=self.frm_points,
                   text='GET',
                   command=self.get_points_result,
                   width=5).grid(row=0, column=1, padx=5, sticky=tk.W)
        self.frm_max_eff_result.grid(row=1, column=0, pady=5, sticky=tk.W)
        ttk.Label(master=self.frm_max_eff_result,
                  text='最大效率 Max Efficiency',
                  justify='left',
                  font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=3, sticky=tk.W)
        ttk.Button(master=self.frm_max_eff_result,
                   text='GET',
                   command=self.get_max_eff_result,
                   width=5).grid(row=0, column=3, padx=5, sticky=tk.W)
        self.frm_ave_result.grid(row=2, column=0, pady=5, sticky=tk.W)
        ttk.Label(master=self.frm_ave_result,
                  text='平均值 Average',
                  justify='left',
                  font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=3, sticky=tk.W)
        ttk.Button(master=self.frm_ave_result,
                   text='GET',
                   command=self.get_ave_result,
                   width=5).grid(row=0, column=3, padx=5, sticky=tk.W)
        self.frm_cv_result.grid(row=3, column=0, pady=5, sticky=tk.W)
        ttk.Label(master=self.frm_cv_result,
                  text='变异系数 CV%',
                  justify='left',
                  font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=3, sticky=tk.W)
        ttk.Button(master=self.frm_cv_result,
                   text='GET',
                   command=self.get_cv_result,
                   width=5).grid(row=0, column=3, padx=5, sticky=tk.W)

    def add_menu(self, menu_class_name, menu_dict):
        """添加菜单"""
        menu_class_name(self, menu_dict)

    def set_values(self):
        """从器件设置中导入参数"""
        self.tv_device_id.set(ds.id)
        self.tv_device_label.set(ds.label)
        self.tv_device_area_cm2.set(ds.area_cm2)

    def device_setting_save(self):
        """保存器件设置"""
        ds.id = self.tv_device_id.get()
        ds.label = self.tv_device_label.get()
        ds.area_cm2 = float(self.tv_device_area_cm2.get())

    def device_setting_reset(self):
        """重置器件设置"""
        global ds
        ds = DeviceSettings()
        self.set_values()

    def get_max(self):
        """获取最大值指令"""
        if get_device():
            max_v_oc, max_j_sc, max_ff, max_eff = device.get_max_list()
            self.tv_max_v_oc.set('{:.3f}'.format(max_v_oc))
            self.tv_max_j_sc.set('{:.3f}'.format(max_j_sc))
            self.tv_max_ff.set('{:.3f}'.format(max_ff))
            self.tv_max_eff.set('{:.3f}'.format(max_eff))

    def get_rr(self):
        """获取整流比指令"""
        # if get_device():
        #     v_rr = float(self.tv_v_rr.get())
        #     rr = device.get_rectification_ratio(v_rr)
        #     self.tv_rr.set('{:.3f}'.format(rr))
        pass

    def get_points_result(self):
        """获取器件结果指令"""
        if get_device():
            self.frm_points_list.destroy()
            self.frm_points_list = ttk.Frame(master=self.frm_points)
            self.frm_points_list.grid(row=1, column=0, columnspan=2, sticky=tk.W)
            for index, title in enumerate(Result.get_title_list()):
                ttk.Label(master=self.frm_points_list,
                          text=title + '\t',
                          font=('Arial', 10, 'bold')).grid(row=0, column=index + 1)
            for point in device.points:
                ttk.Label(master=self.frm_points_list,
                          text=str(point.id) + '\t',
                          font=('Arial', 10, 'bold')).grid(row=point.id, column=0)
                for index, result in enumerate(point.result.get_show_list()):
                    if index == 5 and result >= 10000.0:
                        ttk.Label(master=self.frm_points_list,
                                  text='\t{:.3f}\t'.format(result),
                                  font=('Arial', 12, '')).grid(row=point.id, column=index + 1)
                    else:
                        ttk.Label(master=self.frm_points_list,
                                  text='{:.3f}\t'.format(result),
                                  font=('Arial', 12, '')).grid(row=point.id, column=index + 1)

    def get_max_eff_result(self):
        """获取最大效率指令"""
        if get_device():
            for index, title in enumerate(Result.get_title_list()):
                ttk.Label(master=self.frm_max_eff_result,
                          text=title + '\t',
                          font=('Arial', 10, 'bold')).grid(row=1, column=index + 1)
            ttk.Label(master=self.frm_max_eff_result,
                      text=str(device.max_efficiency_point.id) + '\t',
                      font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W)
            for index, result in enumerate(device.max_efficiency_point.result.get_show_list()):
                ttk.Label(master=self.frm_max_eff_result,
                          text='{:.3f}\t'.format(result),
                          font=('Arial', 12, '')).grid(row=2, column=index + 1)

    def get_ave_result(self):
        """获取平均值"""
        if get_device():
            for index, title in enumerate(Result.get_title_list()):
                ttk.Label(master=self.frm_ave_result,
                          text=title + '\t',
                          font=('Arial', 10, 'bold')).grid(row=1, column=index + 1)
            ttk.Label(master=self.frm_ave_result,
                      text='Ave.\t',
                      font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W)
            for index, result in enumerate(device.mean_result.get_show_list()):
                ttk.Label(master=self.frm_ave_result,
                          text='{:.3f}\t'.format(result),
                          font=('Arial', 12, '')).grid(row=2, column=index + 1)

    def get_cv_result(self):
        """获取变异系数"""
        if get_device():
            for index, title in enumerate(Result.get_title_list()):
                ttk.Label(master=self.frm_cv_result,
                          text=title + '\t',
                          font=('Arial', 10, 'bold')).grid(row=1, column=index + 1)
            ttk.Label(master=self.frm_cv_result,
                      text='CV%.\t',
                      font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W)
            for index, result in enumerate(device.cv_result.get_show_list()):
                ttk.Label(master=self.frm_cv_result,
                          text='{:.3f}\t'.format(result),
                          font=('Arial', 12, '')).grid(row=2, column=index + 1)


class PlotSettingWindow(tk.Toplevel):
    """作图设置窗口类"""

    def __init__(self):
        """构造函数，创建作图设置窗口，初始化窗口控件"""
        super().__init__()
        self.frm = ttk.Frame(master=self)
        self.frm_log_setting = ttk.Frame(master=self.frm)
        self.frm_line_setting = ttk.Frame(master=self.frm)
        self.frm_plot_setting_btn = ttk.Frame(master=self.frm)
        self.tv_log_x_label = tk.StringVar(value=ps.log_x_label)
        self.tv_log_y_label = tk.StringVar(value=ps.log_y_label)
        self.tv_line_x_label = tk.StringVar(value=ps.line_x_label)
        self.tv_line_y_label = tk.StringVar(value=ps.line_y_label)
        self.tv_line_x_min = tk.StringVar(value=ps.line_x_min)
        self.tv_line_x_max = tk.StringVar(value=ps.line_x_max)
        self.tv_line_y_min = tk.StringVar(value=ps.line_y_min)
        self.tv_line_y_max = tk.StringVar(value=ps.line_y_max)
        self.create_window()

    def create_window(self):
        """创建作图设置窗口"""
        self.title('作图设置 Plot Settings')
        self.geometry('360x270+400+200')
        self.focus_set()
        self.frm.grid(sticky=tk.W)
        self.frm_log_setting.grid(row=0, sticky=tk.W)
        ttk.Label(master=self.frm_log_setting,
                  text='对数曲线 Log Curve',
                  font=('Arial', 10, 'bold'),
                  justify='left').grid(row=0, column=0, columnspan=2, sticky=tk.W)
        ttk.Label(self.frm_log_setting,
                  text='x轴标签 Label X',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master=self.frm_log_setting,
                  textvariable=self.tv_log_x_label,
                  justify='right',
                  width=22).grid(row=1, column=1)
        ttk.Label(self.frm_log_setting,
                  text='y轴标签 Label Y',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master=self.frm_log_setting,
                  textvariable=self.tv_log_y_label,
                  justify='right',
                  width=22).grid(row=2, column=1)
        self.frm_line_setting.grid(row=1, sticky=tk.W)
        ttk.Label(self.frm_line_setting,
                  text='线性曲线 Line Curve',
                  font=('Arial', 10, 'bold'),
                  justify='left').grid(row=0, column=0, columnspan=5, sticky=tk.W)
        ttk.Label(self.frm_line_setting,
                  text='x轴标签 Label X',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=1, column=0)
        ttk.Entry(master=self.frm_line_setting,
                  textvariable=self.tv_line_x_label,
                  justify='right',
                  width=22).grid(row=1, column=1, columnspan=4, pady=5, sticky=tk.W)
        ttk.Label(self.frm_line_setting,
                  text='y轴标签 Label Y',
                  font=('Arial', 9, ''),
                  justify='left').grid(row=2, column=0)
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
                  font=('Arial', 9, '')).grid(row=3, pady=5, column=2)
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
                  font=('Arial', 9, '')).grid(row=4, pady=5, column=2)
        ttk.Entry(master=self.frm_line_setting,
                  textvariable=self.tv_line_y_max,
                  justify='right',
                  width=10).grid(row=4, column=3)
        ttk.Label(self.frm_line_setting,
                  text='(mA/cm2)',
                  justify='left').grid(row=4, padx=5, pady=5, column=4)
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
        """从作图设置中导入参数"""
        self.tv_log_x_label.set(ps.log_x_label)
        self.tv_log_y_label.set(ps.log_y_label)
        self.tv_line_x_label.set(ps.line_x_label)
        self.tv_line_y_label.set(ps.line_y_label)
        self.tv_line_x_min.set(ps.line_x_min)
        self.tv_line_x_max.set(ps.line_x_max)
        self.tv_line_y_min.set(ps.line_y_min)
        self.tv_line_y_max.set(ps.line_y_max)

    def plot_setting_save(self):
        """保存作图设置"""
        ps.log_x_label = self.tv_log_x_label.get()
        ps.log_y_label = self.tv_log_y_label.get()
        ps.line_x_label = self.tv_line_x_label.get()
        ps.line_y_label = self.tv_line_y_label.get()
        ps.line_x_min = float(self.tv_line_x_min.get())
        ps.line_x_max = float(self.tv_line_x_max.get())
        ps.line_y_min = float(self.tv_line_y_min.get())
        ps.line_y_max = float(self.tv_line_y_max.get())
        self.destroy()

    def plot_setting_cancel(self):
        """取消作图设置"""
        self.destroy()

    def plot_setting_reset(self):
        """重置作图设置"""
        global ps
        ps = PlotSettings()
        self.set_values()


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

    def open_data_txt(self):
        """打开数据文件指令"""
        global data_path
        data_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt*')])
        self.root.add_menu(AppMenu, self.menu_dict)

    def open_result_txt(self):
        """打开结果文件指令"""
        global result_path
        result_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt*')])
        self.root.add_menu(AppMenu, self.menu_dict)

    @staticmethod
    def export_excel():
        """导出excel指令"""
        if get_device():
            excel_dir = filedialog.askdirectory()
            device.export_excel(excel_dir)

    @staticmethod
    def save_as_txt():
        """保存txt指令"""
        if get_device():
            txt_dir = filedialog.askdirectory()
            device.save_as_txt(txt_dir)

    @staticmethod
    def exit_program():
        """退出指令"""
        sys.exit()

    def show_device_result(self):
        """显示器件结果指令"""
        if get_device():
            self.root.get_points_result()
            self.root.get_max()
            self.root.get_max_eff_result()
            self.root.get_ave_result()
            self.root.get_cv_result()
            self.root.get_rr()

    def add_device(self):
        """添加器件指令"""
        if get_device():
            if device.data_path not in [dev.data_path for dev in device_list]:
                device_list.append(device)
                label_list.append(device.label)
            self.root.add_menu(AppMenu, self.menu_dict)

    def delete_last_device(self):
        """删除上一个器件指令"""
        if device_list:
            device_list.pop()
        self.root.add_menu(AppMenu, self.menu_dict)

    def clear_devices(self):
        """清空器件指令"""
        global device_list
        device_list = []
        self.root.add_menu(AppMenu, self.menu_dict)

    @staticmethod
    def plot_dark_log_curve():
        """作暗态对数曲线指令"""
        # if get_device():
        #     Device.plot_log_curves(device.id,
        #                            ps.log_x_label,
        #                            ps.log_y_label,
        #                            [device.dark_point],
        #                            [device.label + ' dark'])
        pass

    @staticmethod
    def plot_light_line_curve():
        """作光态线性曲线指令"""
        if get_device():
            Device.plot_line_curves(device.id,
                                    ps.line_x_label,
                                    ps.line_y_label,
                                    ps.line_x_min,
                                    ps.line_x_max,
                                    ps.line_y_min,
                                    ps.line_y_max,
                                    [device.max_efficiency_point],
                                    [device.label])

    @staticmethod
    def plot_device_line_curves():
        """作器件线性曲线指令"""
        # if get_device():
        #     Device.plot_devices_line_curves(device.id,
        #                                     ps.line_x_label,
        #                                     ps.line_y_label,
        #                                     ps.line_x_min,
        #                                     ps.line_x_max,
        #                                     ps.line_y_min,
        #                                     ps.line_y_max,
        #                                     [device])
        pass

    @staticmethod
    def plot_dark_contrast_curves():
        """作暗态对比曲线指令"""
        # Device.plot_log_curves(device.id,
        #                        ps.log_x_label,
        #                        ps.log_y_label,
        #                        [dev.dark_point for dev in device_list],
        #                        [dev.label for dev in device_list])
        pass

    @staticmethod
    def plot_light_contrast_curves():
        """作光态对比曲线指令"""
        Device.plot_line_curves(device.id,
                                ps.line_x_label,
                                ps.line_y_label,
                                ps.line_x_min,
                                ps.line_x_max,
                                ps.line_y_min,
                                ps.line_y_max,
                                [dev.max_efficiency_point for dev in device_list],
                                [dev.label for dev in device_list])

    @staticmethod
    def plot_device_contrast_curves():
        """作器件对比曲线指令"""
        # Device.plot_devices_line_curves(device.id,
        #                                 ps.line_x_label,
        #                                 ps.line_y_label,
        #                                 ps.line_x_min,
        #                                 ps.line_x_max,
        #                                 ps.line_y_min,
        #                                 ps.line_y_max,
        #                                 device_list)
        pass

    @staticmethod
    def plot_settings():
        """作图设置指令"""
        PlotSettingWindow()

    def language_simple_chinese(self):
        """语言-简体中文指令"""
        self.root.add_menu(AppMenu, CN_MENU_DICT)

    def language_english(self):
        """语言-英文指令"""
        self.root.add_menu(AppMenu, EN_MENU_DICT)


if __name__ == '__main__':
    app = Application()
    app.add_menu(AppMenu, CN_MENU_DICT)
    app.mainloop()
