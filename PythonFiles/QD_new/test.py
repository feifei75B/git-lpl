# import numpy as np
# import pandas as pd
# path = r'E:\硕士\QDPD\data\IV测试\20190718 390\I273\1-iv-l.txt'
# df = pd.read_csv(path, sep='\t', header=0, names=['index', 'voltage', 'current'])
# df.drop(columns=['index'], inplace=True)
# dark = - df.loc[200:0:-1].reset_index(drop=True)
# light = - df.loc[401:201:-1].reset_index(drop=True)
# print((dark['voltage'] - -0.5).abs().min())
# print(dark.loc[(dark['voltage'] - -0.5).abs() == (dark['voltage'] - -0.5).abs().min(), 'current'].iloc[0])
# print(type(dark['voltage'] - -0.5))
# v = dark['voltage']
# print(type(v))
# print(dark.index)

import tkinter as tk
from tkinter import ttk

def a(event):
    print(event.widget)

root = tk.Tk()
b = ttk.Button(master=root, text='a')
b.bind("<Button-1>", a)
b.pack()
root.mainloop()
