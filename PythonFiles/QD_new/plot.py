import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator


class Plot(object):
    """作图类"""

    @staticmethod
    def plot_line_curves(title, state, x_label, y_label, x_min, x_max, y_min, y_max, devices: list, labels: list):
        # 作线性曲线
        colors = ['navy', 'orange', 'forestgreen', 'red', 'gray', 'purple', 'royalblue', 'brown', 'teal', 'olive']
        if devices:
            plt.figure(title)
            ax = plt.gca()
            for index, device in enumerate(devices):
                getattr(device, 'add_' + state + '_line_curves')(ax, labels[index], colors[:len(device.points)])
                for i in range(len(device.points)):
                    del colors[0]
            ax.axhline(y=0, color='k', linewidth=1)
            ax.axvline(x=0, color='k', linewidth=1)
            ax.xaxis.set_label_text(x_label)
            ax.yaxis.set_label_text(y_label)
            if x_min and x_max:
                ax.set_xlim(x_min, x_max)
            if y_min and y_max:
                ax.set_ylim(y_min, y_max)
            ax.legend(loc='lower right', frameon=False)
            plt.show()

    @staticmethod
    def plot_log_curves(title, state, x_label, y_label, x_min, x_max, y_min, y_max, devices: list, labels: list):
        # 作线性曲线
        colors = ['navy', 'orange', 'forestgreen', 'red', 'gray', 'purple', 'royalblue', 'brown', 'teal', 'olive']
        if devices:
            plt.figure(title)
            ax = plt.gca()
            for index, device in enumerate(devices):
                getattr(device, 'add_' + state + '_log_curves')(ax, labels[index], colors[:len(device.points)])
                for i in range(len(device.points)):
                    del colors[0]
            ax.axhline(y=0, color='k', linewidth=1)
            ax.axvline(x=0, color='k', linewidth=1)
            ax.set_yscale('log')
            ax.xaxis.set_minor_locator(LogLocator(10))
            ax.xaxis.set_label_text(x_label)
            ax.yaxis.set_label_text(y_label)
            if x_min and x_max:
                ax.set_xlim(x_min, x_max)
            if y_min and y_max:
                ax.set_ylim(y_min, y_max)
            ax.legend(loc='lower right', frameon=False)
            plt.show()
