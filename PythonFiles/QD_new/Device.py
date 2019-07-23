class Device(object):

    def __init__(self, paths: list, area_cm2, power_mw, wavelength_nm):
        self.paths = paths
        self.area_cm2 = area_cm2
        self.power_mw = power_mw
        self.wavelength_nm = wavelength_nm
