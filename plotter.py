import matplotlib.pyplot as plt
import numpy as np
from stabelisation import*


class plotter_class():
    def __init__(self) -> None:
        self.stabilityindex = stabelisation_class()
        self.fase_variable = 0
        self.testperson = 1
        self.velocities = []
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

        # Laver tidsakse til de forskellige signaler så de kan plottes i samme figur
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
    
        #plt.show(block = show_bool)
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
    
        #plt.show(block = show_bool)
        pass

    def plot_hr_subplot(self, Dict_all_data: dict, counter: int, show_bool = True):
        list_timeaxes = []
        fs_maxrefdes = 25
        fs_empatica = 1
        fs_garmin = 4
        
        i = 0
        while i < 4:
            maxrefdes = Dict_all_data[counter]['Hr_Maxrefdes103_' + str(i)]
            hrm_pro = Dict_all_data[counter]['Hr_Hrmpro_' + str(i)]
            empatica = Dict_all_data[counter]['Hr_Empatica_' + str(i)]
            forerunner = Dict_all_data[counter]['Hr_Forerunner_' + str(i)]

             # Deltatider
            delta_tid_maxrefdes = 1/fs_maxrefdes
            delta_tid_garmin = 1/fs_garmin
            delta_tid_empatica = 1/fs_empatica

            # længde af signal i tid
            tid_maxrefdes = len(maxrefdes)/fs_maxrefdes
            tid_empatica = len(empatica)/fs_empatica
            tid_hrmpro = len(hrm_pro)/fs_garmin
            tid_forerunner = len(forerunner)/fs_garmin

            # Laver tidsakse til de forskellige signaler så de kan plottes i samme figur
            tidsakse_maxrefdes = np.arange(0,tid_maxrefdes,delta_tid_maxrefdes)
            tidsakse_empatica = np.arange(0,tid_empatica, delta_tid_empatica)
            tidsakse_hrmpro = np.arange(0,tid_hrmpro, delta_tid_garmin)
            tidsakse_forerunner = np.arange(0,tid_forerunner, delta_tid_garmin)

            dict_tidsakse = {}
            dict_tidsakse["Maxrefdes103"] = tidsakse_maxrefdes
            dict_tidsakse["Hrmpro"] = tidsakse_hrmpro
            dict_tidsakse["Empatica"] = tidsakse_empatica
            dict_tidsakse["Forerunner"] = tidsakse_forerunner

            list_timeaxes.append(dict_tidsakse)
            i += 1

        fig, axs = plt.subplots(2,2)
        fig.suptitle("Hr for testperson " + str(counter) + " efter endt stresstest")
        
        list_koordinates = [(0,0), (0,1), (1,0), (1,1)]


        for n in range(len(list_koordinates)):
            axs[list_koordinates[n]].plot(list_timeaxes[n]["Maxrefdes103"], Dict_all_data[counter]['Hr_Maxrefdes103_' + str(n)], label = 'MAXREFDES103')
            axs[list_koordinates[n]].plot(list_timeaxes[n]["Empatica"], Dict_all_data[counter]['Hr_Empatica_' + str(n)], label = 'empatica')
            axs[list_koordinates[n]].plot(list_timeaxes[n]["Hrmpro"],  Dict_all_data[counter]['Hr_Hrmpro_' + str(n)], label = 'HRM-Pro')
            axs[list_koordinates[n]].plot(list_timeaxes[n]["Forerunner"], Dict_all_data[counter]['Hr_Forerunner_' + str(n)], label = 'Forerunner 45')
            axs[list_koordinates[n]].set_xlabel('Tid [sekunder]')
            axs[list_koordinates[n]].set_ylabel('HR [BPM]')
            axs[list_koordinates[n]].legend(loc = 'upper right')
            axs[list_koordinates[n]].set_title('Fase ' + str(n))


        fig.set_size_inches(20,10)
        fig.subplots_adjust(left=0.03, bottom=0.08, right=0.97, top=0.92, wspace=None, hspace=None)
        path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Figurer/Alle_sensorer/'
        title = 'Testperson ' + str(counter)
        fig.savefig(path + " " + title) #, dpi = 200)
        #plt.show()    


        # plotter.plot_hr(maxrefdes= Dict_all_data[counter]['Hr_Maxrefdes103_1'], hrm_pro=Dict_all_data[counter]['Hr_Hrmpro_1'], empatica=Dict_all_data[counter]['Hr_Empatica_1'], forerunner=Dict_all_data[counter]['Hr_Forerunner_1'])
        # plotter.plot_hr(maxrefdes= Dict_all_data[counter]['Hr_Maxrefdes103_2'], hrm_pro=Dict_all_data[counter]['Hr_Hrmpro_2'], empatica=Dict_all_data[counter]['Hr_Empatica_2'], forerunner=Dict_all_data[counter]['Hr_Forerunner_2'])
        # plotter.plot_hr(maxrefdes= Dict_all_data[counter]['Hr_Maxrefdes103_3'], hrm_pro=Dict_all_data[counter]['Hr_Hrmpro_3'], empatica=Dict_all_data[counter]['Hr_Empatica_3'], forerunner=Dict_all_data[counter]['Hr_Forerunner_3'])
        # plotter.plot_rr(maxrefdes= Dict_all_data[counter]['RR_Maxrefdes103_1'], hrm_pro=Dict_all_data[counter]['RR_Hrmpro_1'], empatica=Dict_all_data[counter]['RR_Empatica_1'], forerunner=Dict_all_data[counter]['RR_Forerunner_1'])
        # plotter.plot_rr(maxrefdes= Dict_all_data[counter]['RR_Maxrefdes103_2'], hrm_pro=Dict_all_data[counter]['RR_Hrmpro_2'], empatica=Dict_all_data[counter]['RR_Empatica_2'], forerunner=Dict_all_data[counter]['RR_Forerunner_2'])
        # plotter.plot_rr(maxrefdes= Dict_all_data[counter]['RR_Maxrefdes103_3'], hrm_pro=Dict_all_data[counter]['RR_Hrmpro_3'], empatica=Dict_all_data[counter]['RR_Empatica_3'], forerunner=Dict_all_data[counter]['RR_Forerunner_3'])
        # counter += 1

    def plot_limit_HRM_pro(self, Dict_all_data: dict, counter: int, show_bool = True, index_list = [], list_mean_std = [], hastighed_list = [], fase_intervention_list = [], velocity = []):

        list_timeaxes = []
        list_indexes_time = []
        fs = 4
        list_avg = []
        i = 0
        N = 51
        signal_name=""
        max_and_min_values = []
        list_hastighed = [] 
        tid_two_point_list = []
        hr_two_point_list = []
        while i < 4:
            if(counter == 1):
                signal_original = Dict_all_data[counter]['Hr_Maxrefdes103_' + str(i)]
                signal_name="Hr_Maxrefdes103_"
                fs = 25
            else:
                signal_original = Dict_all_data[counter]['Hr_Hrmpro_' + str(i)]
                signal_name = "Hr_Hrmpro_"
                fs = 4
            
            N = fs*10+1
            
            signal_avg = self.get_filtered_signal(signal_original, N)
            list_avg.append(signal_avg)
            #index = self.stabilityindex.dispertion(hrm_pro_avg)
            dict_tid = {}
            delta_tid_garmin = 1/fs
            if (i > 0):    
                # Deltatider
                time_gmm = index_list[i-1]['gmm']*delta_tid_garmin
                time_soren = index_list[i-1]['soren']*delta_tid_garmin
                dict_tid['gmm'] = time_gmm
                dict_tid['soren'] = time_soren
            elif(i==0):
                dict_tid['gmm'] = 0
                dict_tid['soren'] = 0
            list_indexes_time.append(dict_tid)

            # længde af signal i tid
            tid_signal = len(signal_original[N:len(signal_original)-N])/fs
            tid_avg = len(signal_avg)/fs

            # Laver tidsakse til de forskellige signaler så de kan plottes i samme figur
            tidsakse_signal = np.arange(0,tid_signal, delta_tid_garmin)
            tidsakse_avg = np.arange(0,tid_avg, delta_tid_garmin)

            dict_tidsakse = {}
            dict_tidsakse["Signal"] = tidsakse_signal
            dict_tidsakse["Avg"] = tidsakse_avg
            list_timeaxes.append(dict_tidsakse)
            max_and_min_values.append(max(signal_avg))
            max_and_min_values.append(min(signal_avg))
            if(i>0):    
                list_regression = []
                a = hastighed_list[i-1]['coef']
                b = hastighed_list[i-1]['intercept']
                # Laver den rette linje
                for tid in tidsakse_avg:
                    list_regression.append((a*(tid)+b))
                list_hastighed.append(list_regression)

                #hr_two_point = [signal_avg[0], signal_avg[index_list[i-1]['gmm']]]
                hr_two_point = [list_mean_std[i-1]['mean_high'], list_mean_std[i-1]['mean_low']]
                hr_two_point_list.append(hr_two_point)
                tid_two_point = [0, list_indexes_time[i]['gmm']]
                tid_two_point_list.append(tid_two_point)
                velocity_dict = {}
                velocity_dict['reg'] = a
                velocity_dict['point'] = velocity[i-1]
                velocity_dict['diff'] = a-velocity[i-1]
                self.velocities.append(velocity_dict)
            i += 1

            
        SMALL_SIZE = 12
        MEDIUM_SIZE = 12 #18
        MEDIUM_BIG_SIZE = 12 #22
        BIGGER_SIZE = 24

        plt.rc('font', size=MEDIUM_SIZE)         # controls default text sizes
        plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
        plt.rc('legend', fontsize=MEDIUM_BIG_SIZE)   # legend fontsize
        plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
        # plt.rc('subplot', titlesize=MEDIUM_SIZE)  # fontsize of the figure title

        fig, axs = plt.subplots(2,2)
        fig.suptitle("Hr, testperson " + str(self.testperson) + " after finishing the stresstest", fontweight='bold')
        
        list_koordinates = [(0,0), (0,1), (1,0), (1,1)]

        y_lim_low = min(max_and_min_values)-5
        y_lim_high = max(max_and_min_values)+5
        for n in range(len(list_koordinates)):
            #axs[list_koordinates[n]].plot(list_timeaxes[n]["Signal"],  Dict_all_data[counter][signal_name + str(n)][N:len(Dict_all_data[counter][signal_name + str(n)])-N], label = 'Raw Hr data', color = 'g', linewidth = 0.8)
            axs[list_koordinates[n]].plot(list_timeaxes[n]["Avg"],  list_avg[n], label = 'Averaged Hr data', color = 'g')
           
            if(list_indexes_time[n]['soren']) > 0:
                markerline_mean_soren, stemlines_mean_soren, baseline = axs[list_koordinates[n]].stem(list_indexes_time[n]['soren'],max(Dict_all_data[counter][signal_name + str(n)]),'g', markerfmt='o', linewidth = 0.8,label = 'Time = ' + str(list_indexes_time[n]) + " sec", basefmt=" ")
                plt.setp(markerline_mean_soren, 'color', plt.getp( stemlines_mean_soren,'color'))
            if(n > 0): # alle de ting der skal ske for alle andre end baseline
                mean = list_mean_std[n-1]["mean_low"]
                axs[list_koordinates[n]].axhline(y=mean, color='b', linestyle='-', label = 'Mean of low cluster = ' + str(round(mean,2)), linewidth = 0.8)
                axs[list_koordinates[n]].axhline(y=mean + list_mean_std[n-1]["std_low"], color='k', linestyle='--', linewidth = 0.5, label = 'Mean of low cluster +/- 1*std ')
                axs[list_koordinates[n]].axhline(y=mean - list_mean_std[n-1]["std_low"], color='k', linestyle='--', linewidth = 0.5)
                axs[list_koordinates[n]].plot(list_timeaxes[n]["Avg"], list_hastighed[n-1], color = 'darkgoldenrod', label = 'Stabelization velocity = ' + str(hastighed_list[n-1]['coef']) + " bpm/s")   
                axs[list_koordinates[n]].plot(tid_two_point_list[n-1], hr_two_point_list[n-1], color = 'purple', label = 'Stabelization velocity = ' + str(velocity[n-1]) + " bpm/s")   

                markerline_mean, stemlines_mean, baseline = axs[list_koordinates[n]].stem(list_indexes_time[n]['gmm'],y_lim_high-10,'b', markerfmt='o', label = 'Stabilization time = ' + str(list_indexes_time[n]['gmm']) + " sec", basefmt=" ")
                plt.setp(markerline_mean, 'color', plt.getp( stemlines_mean,'color'))
            axs[list_koordinates[n]].set_ylim([y_lim_low, y_lim_high])
            axs[list_koordinates[n]].set_xlabel('Time [seconds]')
            axs[list_koordinates[n]].set_ylabel('HR [bpm]')
            axs[list_koordinates[n]].legend(loc = 'upper right', facecolor="white")
            axs[list_koordinates[n]].set_facecolor('whitesmoke')
            axs[list_koordinates[n]].grid(color = 'lightgrey')
            axs[list_koordinates[n]].set_title('Phase ' + str(n) + ': ' + str(fase_intervention_list[self.fase_variable]['intervention']) + ' phase', fontsize = MEDIUM_BIG_SIZE, fontweight='bold')
            self.fase_variable += 1


        fig.set_size_inches(20,10)
        fig.set_tight_layout('tight')
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.97, top=0.92, wspace=None, hspace=None)
        path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Figurer/gmm/'
        title = 'Testperson ' + str(self.testperson)
        fig.savefig(path + " " + title) #, dpi = 200)
        self.testperson+= 1
        #plt.show()    

    def get_velocities(self):
        return self.velocities

    def get_filtered_signal(self, raw_signal, average_value):
        N = average_value
        if(N%2 == 0):
            N+=1
        hr_avg = np.convolve(raw_signal, np.ones(N)/N, mode='same')
        hr_return = hr_avg[N:len(hr_avg)-N]
        return hr_return
