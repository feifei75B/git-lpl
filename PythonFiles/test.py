import numpy as np
file = 'E:\\硕士\\QDPD\\data\\IV测试\\20190710\\I283\\1.txt'
with open(file, 'r') as fp:
    data = fp.readlines()
data_list = [list(map(float, [value.strip() for value in line.split('\t')][1:])) for line in data[1:]]
data_array = np.array(data_list)
[voltage, current] = np.hsplit(data_array, 2)
v = voltage.flatten()
i = current.flatten()
gd = np.gradient(i) / np.gradient(v)
i_gd = i / gd
[slope, intercept] = np.polyfit(i, i_gd, 1)
print(slope)
