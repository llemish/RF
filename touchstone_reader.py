import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.interpolate import interp1d
import re


freq_list = []
s11_Mag = []
s11_Phase = []
s21_Mag = []
s21_Phase = []
s12_Mag = []
s12_Phase = []
s22_Mag = []
s22_Phase = []
with open('s2p_temp.s2p', 'r') as f:
    #print(f.readlines())
    for line in f:
        if line[0] != '!':
            if line[0] == '#':
                line = line.upper()
                print(line)
                freq_unit = re.findall(r'^#\s*(\w{1,3})\s*\w\s*\w{2}\s*\w\s*\d{2}', line)
                print(freq_unit)
                format_unit = re.findall(r'^#\s*\w{1,3}\s*\w\s*(\w{2})\s*\w\s*\d{2}', line)
                if freq_unit[0] == 'HZ':
                    unit = 'Hz'
                if freq_unit[0] == 'KHZ':
                    unit = 'kHz'
                if freq_unit[0] == 'MHZ':
                    unit = 'MHz'
                if freq_unit[0] == 'GHZ':
                    unit = 'GHz'
                if freq_unit[0] == 'THZ':
                    unit = 'THz'
                if freq_unit[0] == 'S':
                    unit = 's'
                if freq_unit[0] == 'MS':
                    unit = 'ms'
                if freq_unit[0] == 'US':
                    unit = 'us'
                if freq_unit[0] == 'PS':
                    unit = 'ps'
                print('unit - ', unit)
                if format_unit[0] == 'DB':
                    form = 'dB'
                if format_unit[0] == 'RI':
                    form = 'RI'
                print('format - ', form)
            else:
                split = line.split()
                freq_list.append(int(split[0]))
                s11_Mag.append(float(split[1]))
                s11_Phase.append(float(split[2]))
                s21_Mag.append(float(split[3]))
                s21_Phase.append(float(split[4]))
                s12_Mag.append(float(split[5]))
                s12_Phase.append(float(split[6]))
                s22_Mag.append(float(split[7]))
                s22_Phase.append(float(split[8]))
    s2p = dict(freq=np.array(freq_list), s11_Mag=np.array(s11_Mag), s11_Phase=np.array(s11_Phase),
               s21_Mag=np.array(s21_Mag), s21_Phase=np.array(s21_Phase), s12_Mag=np.array(s12_Mag),
               s12_Phase=np.array(s12_Phase), s22_Mag=np.array(s22_Mag), s22_Phase=np.array(s22_Phase))
    print(s2p)
