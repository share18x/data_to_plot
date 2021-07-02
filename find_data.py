import os
import time
from numpy import add
import plot_data


def finddata(address, extention):
    files_in_this_dir = []
    address = os.path.normpath(address)
    for root, dirs, files in os.walk(address):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == extention:
                files_in_this_dir.append(os.path.join(root,file))
    return files_in_this_dir

address = os.path.abspath(os.path.dirname(__file__))
files = finddata(address=address, extention=".xls")
for i in files:
    # small_signal_plot.calc_plot(address=files[i], header=5, write_csv_switch=1, plot_switch=1)
    # plot_data.transfer_plot(address=i,header=265,instrument='1500',true_gate_width=50,plot_switch=1)
    # plot_data.output_plot(address=i,header=267,instrument='1500',true_gate_width=50,plot_switch=1)
    # plot_data.Schottky_plot(address=i,header=258,instrument='1500',true_gate_width=50,plot_switch=1)
    # plot_data.breakdown_plot(address=i,header=258,instrument='1500',true_gate_width=50,plot_switch=1)
    
    plot_data.transfer_plot(address=i, header=0, instrument='4200', true_gate_width=50)
    # if input('输入q退出，按回车继续：\n') == 'q':
    #     exit()