from tkinter import *
import tkinter.filedialog as tkf
from TextFile import *


def select_file():
    global text_file
    text_path = tkf.askopenfilename(filetypes=[('Text Files', '*.txt*')])
    if text_path != '':
        text_file = PointIVTxt(text_path,
                               float(ent_power.get()),
                               float(ent_area.get()),
                               float(ent_wavelength.get()))
        headline.set('It\'s a txt file：' + text_file.name)
    else:
        headline.set('Please select one file')


def select_files():
    global text_file
    text_paths = tkf.askopenfilenames(filetypes=[('Text Files', '*.txt*'), ('Asc Files', '*.asc*')])
    if text_paths:
        text_file = [PointIVTxt(text_path,
                                float(ent_power.get()),
                                float(ent_area.get()),
                                float(ent_wavelength.get())) for text_path in text_paths]
        headline.set('They are text files')
    else:
        headline.set('Please select one file')


def process():
    global text_file
    ent0.delete(0, END)
    ent1.delete(0, END)
    ent2.delete(0, END)
    ent3.delete(0, END)
    ent_r.delete(0, END)
    try:
        if text_file and not isinstance(text_file, list):
            text_file.write_excel_data()
            result = text_file.get_show_data()
            if result:
                ent0.insert(0, result['-0.5V']['J (nA/cm2)'])
                ent1.insert(0, result['-0.5V']['EQE'])
                ent2.insert(0, result['-2V']['J (nA/cm2)'])
                ent3.insert(0, result['-2V']['EQE'])
                ent_r.insert(0, result['Rs'])
    except ProcessException:
        pass


def plot():
    global text_file
    if text_file and not isinstance(text_file, list):
        text_file.plot_curves()


def dict_to_list(dic, lis):
    for value in dic.values():
        if isinstance(value, dict):
            dict_to_list(value, lis)
        else:
            lis.append(value)


def rebuild_frame_device():
    global can, frm_device, frm_point, frm_add_button
    can.destroy()
    frm_device.destroy()
    can = Canvas(frm_whole, width=0, height=310, bg='Snow')
    frm_device = Frame(frm_whole, bg='Snow')
    frm_point = Frame(frm_device, bg='Snow')
    frm_add_button = Frame(frm_device, bg='Snow')


def add(point_obj):

    def clear():
        device_id.clear()
        point_objs.clear()
        rebuild_frame_device()
        # root.geometry('590x325+300+150')

    def delete(event):
        del point_objs[int(event.widget['text'][-1])]
        rebuild_frame_device()
        add(None)

    def average():
        for num, value in enumerate(device_obj.get_average_data()):
            average_data[num].set(value)

    def plot_dark():
        device_obj.plot_dark()

    def plot_light():
        device_obj.plot_light()

    def plot_all():
        device_obj.plot_all()

    def export():
        try:
            device_obj.write_excel_data()
            export_info.set('SUCCESS')
        except ProcessException:
            export_info.set('ERROR')
        except PermissionError:
            export_info.set('ERROR')

    if point_obj:
        if isinstance(point_obj, list):
            for obj in point_obj:
                if obj.path not in [obj.path for obj in point_objs]:
                    device_id.add(obj.device_id)
                    point_objs.append(obj)
        else:
            if point_obj.path not in [obj.path for obj in point_objs]:
                device_id.add(point_obj.device_id)
                point_objs.append(point_obj)
    if point_objs:
        device_obj = PointIVTxts(point_objs)

        # root.geometry('1010x325+300+150')
        rebuild_frame_device()
        can.grid(row=0, column=1)

        frm_device.grid(row=0, column=2, padx=10, sticky=N, pady=5)

        Label(frm_device,
              text='Device ID:' + ','.join(device_id),
              font=('Arial', 13, ''),
              bg='Snow').grid(row=0, column=0, sticky=W)
        butt_clear = Button(frm_device,
                            text='CLEAR',
                            font=('System', 9, 'bold'),
                            fg='Red',
                            command=clear)
        butt_clear.grid(row=0, column=1, sticky=E)
        Label(frm_point,
              text='No.',
              font=('Arial', 12, ''),
              bg='Snow').grid(row=0, column=0, rowspan=2, padx=5)
        Label(frm_point,
              text='Bias: -0.5V',
              font=('Arial', 10, ''),
              bg='Snow').grid(row=0, column=1, columnspan=2)
        Label(frm_point,
              text='Bias: -2V',
              font=('Arial', 10, ''),
              bg='Snow').grid(row=0, column=3, columnspan=2)
        Label(frm_point,
              text='Jdark (nA/cm2)',
              font=('Arial', 10, ''),
              bg='Snow').grid(row=1, column=1, padx=5)
        Label(frm_point,
              text='EQE',
              font=('Arial', 10, ''),
              bg='Snow').grid(row=1, column=2, padx=5)
        Label(frm_point,
              text='Jdark (nA/cm2)',
              font=('Arial', 10, ''),
              bg='Snow').grid(row=1, column=3, padx=10)
        Label(frm_point,
              text='EQE',
              font=('Arial', 10, ''),
              bg='Snow').grid(row=1, column=4, padx=5)
        Label(frm_point,
              text='Rs',
              font=('Arial', 10, ''),
              bg='Snow').grid(row=1, column=5, padx=5)
        label_text = [[]]
        for row in range(8):
            for column in range(6):
                label_text[row].append(StringVar())
                Label(frm_point,
                      textvariable=label_text[row][column],
                      font=('Arial', 12, ''),
                      bg='Snow').grid(row=row+2, column=column)
            label_text.append([])
        average_data = []
        for column in range(6):
            average_data.append((StringVar()))
            Label(frm_point,
                  textvariable=average_data[column],
                  font=('Arial', 12, ''),
                  bg='Snow',
                  fg='Navy').grid(row=11, column=column)
        try:
            for index, point_data in enumerate(device_obj.get_show_data()):
                for key, data in enumerate(point_data):
                    label_text[index][key].set(data)
                butt_delete = Button(frm_point, text='×'+str(index), font=('', 10, ''), fg='Red')
                butt_delete.bind("<Button-1>", delete)
                butt_delete.grid(row=index+2, column=len(point_data), padx=10)
        except IndexError:
            headline.set('Sorry. We cannot process more than 8 files!')
            clear()
        frm_point.grid(row=2, column=0, columnspan=2, sticky=W)

        butt_average = Button(frm_add_button,
                              text='AVERAGE',
                              font=('System', 10, 'bold'),
                              bg='LightCyan',
                              command=average)
        butt_average.grid(row=0, column=0)
        butt_plot_dark = Button(frm_add_button,
                                text='PLOT DARK',
                                font=('System', 10, 'bold'),
                                bg='LightCyan',
                                command=plot_dark)
        butt_plot_dark.grid(row=0, column=1)
        butt_plot_light = Button(frm_add_button,
                                 text='PLOT LIGHT',
                                 font=('System', 10, 'bold'),
                                 bg='LightCyan',
                                 command=plot_light)
        butt_plot_light.grid(row=0, column=2)
        butt_plot_all = Button(frm_add_button,
                               text='PLOT ALL',
                               font=('System', 10, 'bold'),
                               bg='LightCyan',
                               command=plot_all)
        butt_plot_all.grid(row=0, column=3)
        export_info = StringVar(value='EXPORT')
        butt_export = Button(frm_add_button,
                             textvariable=export_info,
                             font=('System', 10, 'bold'),
                             bg='LightCyan',
                             command=export)
        butt_export.grid(row=0, column=4)
        frm_add_button.grid(row=3, column=0, columnspan=2)
    else:
        clear()


text_file = None
device_id = set()
point_objs = []

root = Tk()
# root.geometry('590x325+300+150')
root.title('Huawei Processor')

frm_whole = Frame(root, bg='Snow')

frm_main = Frame(frm_whole, bg='Snow')
headline = StringVar(value='Thanks for using! Please select text/asc files')
Label(frm_main,
      textvariable=headline,
      font=('Comic Sans MS', 17, ''),
      bg='Snow').grid(row=0, pady=15)

frm_button = Frame(frm_main, bg='Snow')
butt_select_file = Button(frm_button,
                          text=' SELECT FILE',
                          font=('System', 15, 'bold'),
                          bg='AliceBlue',
                          command=select_file)
butt_select_file.grid(row=0, column=0, padx=10, pady=3)
butt_select_files = Button(frm_button,
                           text=' SELECT FILES',
                           font=('System', 15, 'bold'),
                           bg='AliceBlue',
                           command=select_files)
butt_select_files.grid(row=0, column=1, padx=10, pady=3)
butt_process = Button(frm_button,
                      text='PROCESS',
                      font=('System', 15, 'bold'),
                      bg='AliceBlue',
                      command=process)
butt_process.grid(row=0, column=2, padx=10,  pady=3)
butt_plot = Button(frm_button,
                   text='PLOT',
                   font=('System', 15, 'bold'),
                   bg='AliceBlue',
                   command=plot)
butt_plot.grid(row=0, column=3, padx=10, pady=3)
butt_test = Button(frm_button,
                   text='ADD',
                   font=('System', 15, 'bold'),
                   bg='AliceBlue',
                   command=lambda: add(text_file))
butt_test.grid(row=0, column=4, padx=10, pady=3)
frm_button.grid(row=1, column=0)

frm_parameter = Frame(frm_main, bg='Snow')
Label(frm_parameter,
      text='Optical power (mW)',
      font=('Arial', 13, ''),
      bg='Snow').grid(row=0, column=0, pady=5)
Label(frm_parameter,
      text='Electrode area (cm2)',
      font=('Arial', 13, ''),
      bg='Snow').grid(row=0, column=1, pady=5)
Label(frm_parameter,
      text='Wavelength (nm)',
      font=('Arial', 13, ''),
      bg='Snow').grid(row=0, column=2, pady=5)
ent_power = Entry(frm_parameter)
ent_power.grid(row=1, column=0)
ent_power.insert(0, 1)
ent_area = Entry(frm_parameter)
ent_area.grid(row=1, column=1, padx=5)
ent_area.insert(0, 0.0706858)
ent_wavelength = Entry(frm_parameter)
ent_wavelength.grid(row=1, column=2)
ent_wavelength.insert(0, 970)
frm_parameter.grid(row=2, column=0, pady=15)

Label(frm_main,
      text='IV Process Result',
      font=('Arial', 16, ''),
      bg='Snow').grid(row=3, column=0, sticky=W, pady=10)

frm_data = Frame(frm_main, bg='Snow')
Label(frm_data,
      text='Bias: -0.5V',
      font=('Arial', 13, ''),
      bg='Snow').grid(row=0, column=0, columnspan=2)
Label(frm_data,
      text='Bias: -2V',
      font=('Arial', 13, ''),
      bg='Snow').grid(row=0, column=2, columnspan=2)
Label(frm_data,
      text='Jdark (nA/cm2)',
      font=('Arial', 13, ''),
      bg='Snow').grid(row=1, column=0)
Label(frm_data,
      text='EQE',
      font=('Arial', 13, ''),
      bg='Snow').grid(row=1, column=1)
Label(frm_data,
      text='Jdark (nA/cm2)',
      font=('Arial', 13, ''),
      bg='Snow').grid(row=1, column=2)
Label(frm_data,
      text='EQE',
      font=('Arial', 13, ''),
      bg='Snow').grid(row=1, column=3)
Label(frm_data,
      text='Rs',
      font=('Arial', 13, ''),
      bg='Snow').grid(row=1, column=4)
ent0 = Entry(frm_data)
ent0.grid(row=2, column=0)
ent1 = Entry(frm_data)
ent1.grid(row=2, column=1)
ent2 = Entry(frm_data)
ent2.grid(row=2, column=2)
ent3 = Entry(frm_data)
ent3.grid(row=2, column=3)
ent_r = Entry(frm_data)
ent_r.grid(row=2, column=4, sticky=W)
frm_data.grid(row=4, column=0, sticky=W, padx=6, pady=5)
frm_main.grid(row=0, column=0, sticky=N)

can = Canvas(frm_whole, width=4, height=250, bg='Snow')

frm_device = Frame(frm_whole, bg='Snow')
frm_point = Frame(frm_device, bg='Snow')
frm_add_button = Frame(frm_device, bg='Snow')

frm_whole.grid(sticky=N+W)

root.mainloop()
