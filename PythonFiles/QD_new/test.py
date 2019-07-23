import numpy as np
import pandas as pd
path = r'E:\硕士\QDPD\data\IV测试\20190718 390\I273\1-iv-l.txt'
df = pd.read_csv(path, sep='\t', header=0, names=['index', 'voltage', 'current'])
df.drop(columns=['index'], inplace=True)
dark = df.loc[0:200]
light = df.loc[201:401]
print(dark, type(light))
dark.loc[0, 'current'] = 0
print(df)
