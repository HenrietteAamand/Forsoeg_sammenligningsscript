import matplotlib.pyplot as plt
import numpy as np


class plotter_class():
    def __init__(self) -> None:
        pass

    def plot_hr(self, maxrefdes = [], fs_maxrefdes = 25, hrm_pro = [], forerunner = [], fs_garmin = 4, empatica = [], fs_empatica = 1, fasenummer = 0, testpersonnummer = 0, show_bool = True):
        """Metoden plotter alle HR signaler i samme plot. Der laves en tidsakse ud fra den angivede samplerate. Samperate er pr default sat til til hhv 25, 4 og 1 for Maxrefdes103, Garmn og sidst empatica. 

        Args:
            maxrefdes (list, optional): Liste med hr værdier Defaults to [].
            fs_maxrefdes (int, optional): [description]. Defaults to 25.
            hrm_pro (list, optional): Liste med hr værdier. Defaults to [].
            forerunner (list, optional): Liste med hr værdier. Defaults to [].
            fs_garmin (int, optional): Samplefrekvens for garmminprodukterne. Defaults to 4.
            empatica (list, optional): Liste med hr værdier. Defaults to [].
            fs_empatica (int, optional): Sampelfrekvens for empatica. Defaults to 1.
            fasenummer (int, optional): Fasenummer er nummeret på fasen, og Bruges til en titel. Defaults to 0.
            testpersonnummer (int, optional): Testpersonnummer er nummeret på testpersonen, hvis data der plottes. Defaults to 0.
            show_bool (bool, optional): Styrer om plottet vises eller ej. Defaults to True.
        """
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
        plt.title("Hr-values for 4 sensors")
    
        plt.show(block = show_bool)
        #plt.close(1)


    def plot_rr(self, maxrefdes = [], hrm_pro = [], forerunner = [], empatica = [], fasenummer = 0, testpersonnummer = 0, show_bool = True):
        """Metoden plotter de givne RR-værdier

        Args:
            maxrefdes (list, optional): Liste med RR-værdier for maxrefdes. Defaults to [].
            hrm_pro (list, optional): Liste med RR-værdier for HRM-Pro. Defaults to [].
            forerunner (list, optional): Liste med RR-værdier for Forerunner 45. Defaults to [].
            empatica (list, optional): Liste med RR værdier for Empatica. Defaults to [].
            fasenummer (int, optional): Fasenummer er nummeret på fasen, og Bruges til en titel. Defaults to 0.
            testpersonnummer (int, optional): Testpersonnummer er nummeret på testpersonen, hvis data der plottes. Defaults to 0.
            show_bool (bool, optional): Styrer om plottet vises eller ej. Defaults to True.
        """
        plt.figure(1)
        plt.plot(maxrefdes, label = 'MAXREFDES103')
        plt.plot(empatica, label = 'empatica')
        plt.plot(hrm_pro, label = 'HRM-Pro')
        plt.plot(forerunner, label = 'Forerunner 45')
        plt.legend(loc = 'upper right')
        plt.title("RR-values for 4 sensors")
    
        plt.show(block = show_bool)
        pass