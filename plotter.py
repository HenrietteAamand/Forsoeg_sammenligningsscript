import matplotlib.pyplot as plt
import numpy as np


class plotter_class():
    def __init__(self) -> None:
        pass

    def plot_hr(self, maxrefdes, fs_maxrefdes = 25, hrm_pro = [], forerunner = [], fs_garmin = 4, empatica = [], fs_empatica = 1, fasenummer = 0, testpersonnummer = 0, show_bool = True):
        # Deltatider
        delta_tid_maxrefdes = 1/fs_maxrefdes
        delta_tid_garmin = 1/fs_garmin
        delta_tid_empatica = 1/fs_empatica

        # længde af signal i tid
        tid_maxrefdes = len(maxrefdes)/fs_maxrefdes
        tid_empatica = len(empatica)/fs_empatica
        tid_hrmpro = len(hrm_pro)/fs_garmin
        tid_forerunner = len(forerunner)/fs_garmin

        # kaver tidsakse til de forskellige signaler så de kan plottes i samme figur
        tidsakse_maxrefdes = np.arange(0,tid_maxrefdes,delta_tid_maxrefdes)
        tidsakse_empatica = np.arange(0,tid_empatica, delta_tid_empatica)
        tidsakse_hrmpro = np.arange(0,tid_hrmpro,delta_tid_garmin)
        tidsakse_forerunner = np.arange(0,tid_forerunner, delta_tid_garmin)

        plt.figure(1)
        plt.plot(tidsakse_maxrefdes, maxrefdes, label = 'MAXREFDES103')
        plt.plot(tidsakse_empatica, empatica, label = 'empatica')
        plt.plot(tidsakse_hrmpro, hrm_pro, label = 'HRM-Pro')
        plt.plot(tidsakse_forerunner, forerunner, label = 'Forerunner 45')
        plt.legend(loc = 'upper right')
    
        plt.show(block = show_bool)
        #plt.close(1)


    def plot_rr(self, maxrefdes, hrm_pro = [], forerunner = [], empatica = [], fasenummer = 0, testpersonnummer = 0):
        pass