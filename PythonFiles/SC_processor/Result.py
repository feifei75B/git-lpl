class Result(object):
    """结果类"""
    def __init__(self, result_array):
        self.oc_voltage_v = result_array[0]
        self.sc_current_a = result_array[1]
        self.sc_current_density_ma_cm2 = result_array[2]
        self.max_current_a = result_array[3]
        self.max_voltage_v = result_array[4]
        self.max_power_mw = result_array[5]
        self.fill_factor = result_array[6]
        self.efficiency = result_array[7]
        self.s_resistance_ohms = result_array[8]
        self.sh_resistance_ohms = result_array[9]

    def get_show_list(self):
        return [self.oc_voltage_v,
                self.sc_current_density_ma_cm2,
                self.fill_factor,
                self.efficiency,
                self.s_resistance_ohms,
                self.sh_resistance_ohms]

    @staticmethod
    def get_title_list():
        return ['Voc (V)', 'Jsc (mA/cm2)', 'FF', 'η (%)', 'Rs (Ω)', 'Rsh (Ω)']
