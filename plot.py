
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

def setup_plotting(num_plots):
    ax_lst = []
    for i in range(num_plots):
        fig = plt.figure(i + 1,figsize=(8,3)) # (width, height)
        ax_lst.append(fig.add_subplot(111))
        fig.set_tight_layout(True)

    return ax_lst

def format_plots(ax_lst,metric_details):
    for i, ax in enumerate(ax_lst):
        metric_name = list(metric_details.keys())[i]
        metric_detail = list(metric_details.values())[i]
        if 'voltage' == metric_name:
            add_ele = 'bus'
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.4f'))

        else:
            add_ele = 'branch'
        ax.legend(loc="upper right")
        ax.set_xlabel(add_ele + ' of network')
        ax.set_ylabel(add_ele + ' ' + metric_detail)
        ax.set_title('Adding branch based on ' + metric_detail)