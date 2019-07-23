import os
import abc
import numpy as np
import pandas as pd


class Point(metaclass=abc.ABCMeta):
    """工作点抽象类"""

    def __init__(self, path, area_cm2, power_mw, wavelength_nm):
        # 构造函数
        self.path = path
        self.area_cm2 = area_cm2
        self.power_mw = power_mw
        self.wavelength_nm = wavelength_nm
        self.id = self.get_id()
        self.dark_df, self.light_df = self.get_df()

    def get_id(self):
        # 获取id
        basename = os.path.basename(self.path)
        if basename[1].isdigit():
            return basename[0:2]
        else:
            return basename[0]

    @abc.abstractmethod
    def get_df(self):
        # 抽象方法，获取dataframe
        return None, None


class AgilentPoint(Point):

    def get_df(self):
        # 获取dataframe
        df = pd.read_csv(self.path, sep='\t', header=0, names=['index', 'voltage_v', 'current_a'])
        df.drop(columns=['index'], inplace=True)
        df.loc[:, 'current density_na/cm2'] = df.loc[:, 'current_a'] * 1e9 / self.area_cm2
        if df.shape[0] >= 402:
            # 暗态、光态
            return np.negative(df.copy().loc[200:0:-1].reset_index(drop=True)), \
                   np.negative(df.copy().loc[401:201:-1].reset_index(drop=True))
        elif df.shape[0] >= 201:
            # 暗态
            return np.negative(df.copy().loc[200:0:-1].reset_index(drop=True)), None
        else:
            # 无效数据
            return None, None


if __name__ == '__main__':
    """测试用例"""
    ap = AgilentPoint(r'E:\硕士\QDPD\data\IV测试\20190718 390\I273\1-iv-l.txt', 0.0706858, 0.39, 970)
    print(ap.dark_df, ap.light_df)
    print(ap.dark_df['current density_na/cm2'])
