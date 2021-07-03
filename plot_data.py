from logging import Handler
import os
from posixpath import split
from numpy.lib.function_base import append
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import re
from pandas.io.formats import printing
from scipy.misc import derivative

def dydx(y, x):
    ret = []
    for i in range(len(y)):
        if i == 0:
            ret.append((y[i]-y[i+1])/(x[i]-x[i+1]))

        elif i < len(y)-1:
            ret.append((y[i-1]-y[i+1])/(x[i-1]-x[i+1]))
        elif i == len(y)-1:
            ret.append((y[i]-y[i-1])/(x[i]-x[i-1]))

    
    # ret.append('')
    return ret

    

def plot_xy(x, y, x_label, y_label, title, plot_switch=1, y_is_log=0):
    if plot_switch == 1:
        plt.rcParams['font.sans-serif'] = ['Times New Roman']
        plt.rcParams['font.serif'] = ['Times New Roman']
        fig = plt.figure()
        ax = fig.add_subplot(111)



        lns1 = ax.plot(x, y, 'g-', label=y_label)
        ax.set_xlabel(x_label, fontdict={'family': 'Times New Roman', 'size': 20})
        ax.set_ylabel(y_label, color='g', fontdict={'family': 'Times New Roman', 'size': 20})
        if y_is_log == 1:
            ax.set_yscale("log")
        ax.set_title(title, fontdict={'family': 'Times New Roman', 'size': 20})

        lns = lns1
        labs = [l.get_label() for l in lns]

        ax.legend(lns, labs, loc=0)
        plt.show()


def plot_xyy(x, y1, y2, x_label, y1_label, y2_label, title, plot_switch=1, y1_is_log=0, y2_is_log=0, save_switch=1):
    
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['font.serif'] = ['Times New Roman']
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax2 = ax.twinx()

    lns1 = ax.plot(x, y1, 'g-', label=y1_label)
    ax.set_xlabel(x_label, fontdict={'family': 'Times New Roman', 'size': 20})
    ax.set_ylabel(y1_label, color='g', fontdict={'family': 'Times New Roman', 'size': 20})
    if y1_is_log == 1:
        ax.set_yscale("log")
    if y2_is_log == 1:
        ax2.set_yscale("log")
    ax.set_title(title, fontdict={'family': 'Times New Roman', 'size': 20})
    lns2 = ax2.plot(x, y2, 'r-', label=y2_label)
    ax2.set_ylabel(y2_label, color='r', fontdict={'family': 'Times New Roman', 'size': 20})
    

    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]

    ax.legend(lns, labs, loc=0)
    if plot_switch == 1:
        plt.show()
    elif save_switch == 1:
        print(title)
        plt.savefig(os.path.normpath(os.path.dirname(__file__)+f'/{title}.jpg'))



def plot_xyy_breakdown(x, y1, y2, x_label, y1_label, y2_label, title, plot_switch=1, y1_is_log=0, y2_is_log=0):
    if plot_switch == 1:
        plt.rcParams['font.sans-serif'] = ['Times New Roman']
        plt.rcParams['font.serif'] = ['Times New Roman']
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax2 = ax.twinx()

        lns1 = ax.plot(x, y1, 'g-', label=y1_label)
        ax.set_xlabel(x_label, fontdict={'family': 'Times New Roman', 'size': 20})
        ax.set_ylabel(y1_label, color='g', fontdict={'family': 'Times New Roman', 'size': 20})

        if y1_is_log == 1:
            ax.set_yscale("log")
        if y2_is_log == 1:
            ax2.set_yscale("log")
        ax.set_title(title, fontdict={'family': 'Times New Roman', 'size': 20})
        lns2 = ax2.plot(x, y2, 'r-', label=y2_label)
        ax2.set_ylabel(y2_label, color='r', fontdict={'family': 'Times New Roman', 'size': 20})
        ax.set_ylim(1e-5, 1e1)
        ax2.set_ylim(1e-5, 1e1)

        lns = lns1 + lns2
        labs = [l.get_label() for l in lns]

        ax.legend(lns, labs, loc=0)
        plt.show()


def transfer_plot(address, header, instrument, true_gate_width, plot_switch=1, save_switch=1):
    

    if instrument == '1500':
        ret = re.search('Trans', address)
        if ret is None:
            return None
        filename = address.split('\\')[-1].split('.')[0]
        title = filename[filename.find('HGJ'):filename.rfind('(')]
        try :
            pd_reader = pd.read_csv(address, sep=',',header=header-2).drop(columns=['DataName'])
        except :
            return

        df1 = pd.DataFrame()
        df1 = pd_reader
        list1 = pd_reader.columns.tolist()
        for x in list1:
            if x in [' Vgate', ' Vdrian', ' IDRAIN', ' ISOURCE', ' IGATE', ' Idrain', ' Isource', ' Igate',' gm']:
                continue
            df1 = df1.drop(columns=[x])
        # print(df1)
        df1['NId'] = df1[' IDRAIN'] * 1e6 / true_gate_width

        # 计算跨导
        # list1 = dydx(y=df1[' IDRAIN'], x=df1[' Vgate'])
        # list1 = np.diff(df1[' IDRAIN'])
        # list1 = np.append(list1, 'NaN')
        df1['Ngm'] = dydx(y=df1[' IDRAIN'], x=df1[' Vgate'])
        # df1['Ngm'] = pd.to_numeric(df1['Ngm'], errors='coerce')
        df1['Ngm'] = df1['Ngm'] * 1e6 / true_gate_width
        # print(df1)
        # df1['Ngm'] = derivative(df1[' IDRAIN'], df1[' Vgate'])

        plot_xyy(x=df1[' Vgate'],y1=df1['NId'],y2=df1['Ngm'],x_label="Gate Voltage (V)",y1_label="Drain Current (mA/mm)",y2_label='Transconductance (mS/mm)',title=title,plot_switch=plot_switch,save_switch=save_switch)

    elif instrument  == '4200':
        ret = re.search('Trans', address)
        if ret is None:
            return None
        # debug
        # address.split('\\')[-1]
        # address.split('\\')[-2]
        # address.split('\\')[-3]
        # address.split('\\')[-4]
        title = ' '.join(address.split('\\')[-4:-1]) + ' ' + address.split('\\')[-1].split('.')[0]
        # .split('.')[0]
        # title = filename[filename.find('HGJ'):filename.rfind('(')]

        pd_reader = pd.read_excel(address,sheet_name=0,header=header)
        df1 = pd.DataFrame()
        df1 = pd_reader
        # 读取列名，并抛弃不需要的数据
        list1 = pd_reader.columns.tolist()
        for x in list1:
            if x in ['DrainI', 'DrainV', 'GateI', 'GateV', 'GM']:
                continue
            df1 = df1.drop(columns=[x])
        # 设置字符串为NaN
        df1['GM'] = pd.to_numeric(df1['GM'], errors='coerce')
        # print(df1['GM'])
        df1['NId'] = df1['DrainI'] * 1e6 / true_gate_width
        df1['NIg'] = np.abs(df1['GateI'] * 1e6 / true_gate_width)
        df1['Ngm'] = df1['GM'] * 1e6 / true_gate_width
        # print(df1)
        plot_xyy(x=df1['GateV'],y1=df1['NId'],y2=df1['Ngm'],x_label="Gate Voltage (V)",y1_label="Drain Current (mA/mm)",y2_label='Transconductance (mS/mm)',title=title,plot_switch=plot_switch,save_switch=save_switch)
        

def output_plot(address, header, instrument, true_gate_width, plot_switch=1 ):
    

    if instrument == '1500':
        ret = re.search('Output', address)
        if ret is None:
            return None
        filename = address.split('\\')[-1].split('.')[0]
        title = filename[filename.find('HGJ'):filename.rfind('(')]

        pd_reader = pd.read_csv(address, sep=',',header=header-2).drop(columns=['DataName'])
        df1 = pd.DataFrame()
        df1 = pd_reader
        list1 = pd_reader.columns.tolist()
        for x in list1:
            if x in [' Vdrain', ' Vgate', ' Vdrian', ' IDRAIN', ' ISOURCE', ' IGATE']:
                continue
            df1 = df1.drop(columns=[x])
        df1['NId'] = df1[' IDRAIN'] * 1e6 / true_gate_width

        print(df1)
        plot_xy(x=df1[' Vdrain'],y=df1['NId'],x_label="Gate Voltage (V)",y_label="Drain Current (mA/mm)",title=title,plot_switch=plot_switch)
    # TO DO 
    elif instrument  == '4200':
        ret = re.search('Output', address)
        if ret is None:
            return None

        title = ' '.join(address.split('\\')[-4:-1]) + ' ' + address.split('\\')[-1].split('.')[0]
        # .split('.')[0]
        # title = filename[filename.find('HGJ'):filename.rfind('(')]

        pd_reader = pd.read_excel(address,sheet_name=0,header=header)
        df1 = pd.DataFrame()
        df1 = pd_reader
        # 读取列名，并抛弃不需要的数据
        list1 = pd_reader.columns.tolist()
        for x in list1:
            if x in ['DrainI', 'DrainV', 'GateI', 'GateV', 'GM']:
                continue
            df1 = df1.drop(columns=[x])
        # 设置字符串为NaN
        df1['GM'] = pd.to_numeric(df1['GM'], errors='coerce')
        # print(df1['GM'])
        df1['NId'] = df1['DrainI'] * 1e6 / true_gate_width
        df1['NIg'] = np.abs(df1['GateI'] * 1e6 / true_gate_width)
        df1['Ngm'] = df1['GM'] * 1e6 / true_gate_width
        # print(df1)
        plot_xyy(x=df1['GateV'],y1=df1['NId'],y2=df1['Ngm'],x_label="Gate Voltage (V)",y1_label="Drain Current (mA/mm)",y2_label='Transconductance (mS/mm)',title=title,plot_switch=plot_switch)

def Schottky_plot(address, header, instrument, true_gate_width, plot_switch=1 ):
    
  
    if instrument == '1500':
        ret = re.search('Schottky', address)
        if ret is None:
            return None
        filename = address.split('\\')[-1].split('.')[0]
        title = filename[filename.find('HGJ'):filename.rfind('(')]
        
        pd_reader = pd.read_csv(address, sep=',',header=header-2).drop(columns=['DataName'])
        df1 = pd.DataFrame()
        df1 = pd_reader
        list1 = pd_reader.columns.tolist()
        for x in list1:
            if x in [' Vdrain', ' Vgate', ' Vdrian', ' IDRAIN', ' ISOURCE', ' IGATE']:
                continue
            df1 = df1.drop(columns=[x])
        df1['NIg'] = np.abs(df1[' IGATE'] * 1e6 / true_gate_width)
        # print(df1)
        plot_xy(x=df1[' Vgate'],y=df1['NIg'],x_label="Gate Voltage (V)",y_label="Gate Current (mA/mm)",title=title,plot_switch=plot_switch,y_is_log=1)

    elif instrument  == '4200':
        ret = re.search('Igs', address)
        if ret is None:
            return None

        title = ' '.join(address.split('\\')[-4:-1]) + ' ' + address.split('\\')[-1].split('.')[0]
        # .split('.')[0]
        # title = filename[filename.find('HGJ'):filename.rfind('(')]

        pd_reader = pd.read_excel(address,sheet_name=0,header=header)
        df1 = pd.DataFrame()
        df1 = pd_reader
        # 读取列名，并抛弃不需要的数据
        list1 = pd_reader.columns.tolist()
        for x in list1:
            if x in ['GateI', 'GateV']:
                continue
            df1 = df1.drop(columns=[x])
        df1['NIg'] = np.abs(df1['GateI'] * 1e6 / true_gate_width)
        print(df1)
        plot_xy(x=df1['GateV'],y=df1['NIg'],x_label="Gate Voltage (V)",y_label="Gate Current (mA/mm)",title=title,plot_switch=plot_switch,y_is_log=1)


def breakdown_plot(address, header, instrument, true_gate_width, plot_switch=1 ):
    

    if instrument == '1500':
        ret = re.search('Breakdown', address)
        if ret is None:
            return None
        filename = address.split('\\')[-1].split('.')[0]
        title = filename[filename.find('HGJ'):filename.rfind('(')]
    
        pd_reader = pd.read_csv(address, sep=',',header=header-2).drop(columns=['DataName'])
        df1 = pd.DataFrame()
        df1 = pd_reader
        list1 = pd_reader.columns.tolist()
        for x in list1:
            if x in [' Vdrian', ' IDRAIN', ' ISOURCE', ' IGATE']:
                continue
            df1 = df1.drop(columns=[x])
        df1['NId'] = df1[' IDRAIN'] * 1e6 / true_gate_width
        df1['NIg'] = np.abs(df1[' IGATE'] * 1e6 / true_gate_width)
        # print(df1)
        plot_xyy_breakdown(x=df1[' Vdrian'],y1=df1['NId'],y2=df1['NIg'],x_label="Drain Voltage (V)",y1_label="Drain Current (mA/mm)",y2_label='Gate Current (mA/mm)',title=title,plot_switch=plot_switch,y1_is_log=1,y2_is_log=1)

    elif instrument  == '4200':
        ret = re.search('BR', address)
        if ret is None:
            return None
        # 设置标题
        title = ' '.join(address.split('\\')[-4:-1]) + ' ' + address.split('\\')[-1].split('.')[0]
        # .split('.')[0]
        # title = filename[filename.find('HGJ'):filename.rfind('(')]

        pd_reader = pd.read_excel(address,sheet_name=0,header=header)
        df1 = pd.DataFrame()
        df1 = pd_reader
        # 读取列名，并抛弃不需要的数据
        list1 = pd_reader.columns.tolist()
        for x in list1:
            if x in ['DrainI', 'DrainV', 'SourceI', 'SourceV', 'GateI', 'GateV']:
                continue
            df1 = df1.drop(columns=[x])
        # 重新计算归一化值
        df1['NId'] = df1['DrainI'] * 1e6 / true_gate_width
        df1['NIg'] = np.abs(df1['GateI'] * 1e6 / true_gate_width)
        # print(df1)
        plot_xyy_breakdown(x=df1['DrainV'],y1=df1['NId'],y2=df1['NIg'],x_label="Drain Voltage (V)",y1_label="Drain Current (mA/mm)",y2_label='Gate Current (mA/mm)',title=title,plot_switch=plot_switch,y1_is_log=1,y2_is_log=1)



    # # output csv extension
    # if write_csv_switch == 1:
    #     preaddress, ext = os.path.splitext(address)
    #     address_output = os.path.normpath(preaddress+".csv")
    #     pd_reader.to_csv(address_output)

# transfer_plot(address=r'C:\Users\rikka\Desktop\Workshop\data\HGJ170_20210329\Trans-Vd=10V-50um [HGJ214-I11-PAI150U(2) ; 3_29_2021 10_24_15 AM].csv', header=265, instrument='1500', true_gate_width=50)