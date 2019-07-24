import abc
import numpy as np
import pandas as pd


class Point(metaclass=abc.ABCMeta):
    """工作点抽象类"""

    def __init__(self, path, point_id, area_cm2, power_mw, wavelength_nm):
        # 构造函数
        self.path = path
        self.id = point_id
        self.area_cm2 = area_cm2
        self.power_mw = power_mw
        self.wavelength_nm = wavelength_nm
        self.dark_df, self.light_df = self.get_df()

    @abc.abstractmethod
    def get_df(self):
        # 抽象方法，获取数据，返回dataframe
        return None, None

    def get_certain_dark_current_density(self, voltage_v):
        # 获取特定电压下暗电流密度
        if self.dark_df is not None:
            dark_diff_df = (self.dark_df['voltage_v'] - voltage_v).abs()
            return self.dark_df.loc[dark_diff_df == dark_diff_df.min(), 'current density_na/cm2'].iloc[0]

    def get_certain_external_quantum_efficiency(self, voltage_v):
        # 获取特定电压下外量子效率
        if self.light_df is not None:
            dark_diff_df = (self.dark_df['voltage_v'] - voltage_v).abs()
            light_diff_df = (self.light_df['voltage_v'] - voltage_v).abs()
            dark_current_a = self.dark_df.loc[dark_diff_df == dark_diff_df.min(), 'current_a'].iloc[0]
            light_current_a = self.light_df.loc[light_diff_df == light_diff_df.min(), 'current_a'].iloc[0]
            return (light_current_a - dark_current_a) * 1240 / \
                   (self.area_cm2 * 1e-3 * self.power_mw * self.wavelength_nm)

    def get_result_df(self):
        # 获取结果，返回dataframe
        result = [{
            'id': self.id,
            '-0.5V jdark': self.get_certain_dark_current_density(-0.5),
            '-0.5V eqe': self.get_certain_external_quantum_efficiency(-0.5),
            '-2V jdark': self.get_certain_dark_current_density(-2.0),
            '-2V eqe': self.get_certain_external_quantum_efficiency(-2.0)
        }]
        return pd.DataFrame(result, columns=['id', '-0.5V jdark', '-0.5V eqe', '-2V jdark', '-2V eqe'])


class AgilentPoint(Point):
    """安捷伦测试工作点类"""

    def get_df(self):
        # 获取安捷伦数据
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
    print(ap.get_result_df())
