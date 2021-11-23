from stabelisation import stabelisation_class
from scipy.stats import norm
import scipy


from stabelisation import *
class results_class():
    def __init__(self, fase_intervention_testperson_sammenhaeng) -> None:
        self.intervention = fase_intervention_testperson_sammenhaeng
        self.list_dict_results = []
        self.stabel = stabelisation_class()
        self.id_2_dot_0 = 1
        


    def procces_results(self, Dict_all_data: dict, counter: int):
        i = 1
        fs = 0
        list_hr_avg = []
        list_mean_std = []
        while i < 4: #denne tæller faser, jeg skal ikke forholde mig til antal personer
            if(counter == 1):
                signal_original = Dict_all_data[counter]['Hr_Maxrefdes103_' + str(i)]
                signal_name="Hr_Maxrefdes103_"
                fs = 25
            else:
                signal_original = Dict_all_data[counter]['Hr_Hrmpro_' + str(i)]
                signal_name = "Hr_Hrmpro_"
                fs = 4
            signal_original = Dict_all_data[counter][signal_name + str(i)]
            hr_avg = self.__get_filtered_signal(signal_original, fs*12+1)
            list_hr_avg.append(hr_avg)
            index = self.stabel.gmm(hr_avg)
            delta_tid_garmin = 1/fs

            tid = index*delta_tid_garmin
            maximum_hr = max(hr_avg)
            hastighed = maximum_hr/(tid)
            stabiliseringsniveau, denanden = self.stabel.get_means()
            n=0
            while(n < 3):
                index2 = counter*3+n-3
                fasenummer = self.intervention[index2]['fase']
                if(fasenummer == str(i)):
                    intervention = self.intervention[index2]['intervention']
                n+=1
            dict_results = {}
            dict_results['ID 2.0'] = self.id_2_dot_0
            dict_results['ID 1.0'] = counter
            dict_results['Mean'] = stabiliseringsniveau
            dict_results['Condition'] = intervention
            dict_results['Time'] = tid
            dict_results['Max'] = maximum_hr
            dict_results['Velocity (bpm/s)'] = hastighed

            self.list_dict_results.append(dict_results)
            std_low, std_high = self.stabel.get_stds()
            mean_low, mean_high = self.stabel.get_means()
            dict_mean_std = {}
            dict_mean_std["std_low"] = std_low
            dict_mean_std["std_high"] = std_high
            dict_mean_std["mean_low"] = mean_low
            dict_mean_std["mean_high"] = mean_high
            list_mean_std.append(dict_mean_std)
            i+=1

        self.id_2_dot_0 += 1
        self.plot_hist_and_gaussian(list_hr_data=list_hr_avg, list_mean_std = list_mean_std, counter=counter)
        


    def __get_filtered_signal(self, raw_signal, average_value):
        N = average_value
        if(N%2 == 0):
            N+=1
        hr_avg = np.convolve(raw_signal, np.ones(N)/N, mode='same')
        hr_return = hr_avg[N:len(hr_avg)-N]
        return hr_return

    def Get_results_as_list(self):
        return self.list_dict_results

    def Empty_dict(self):
        self.list_dict_results.clear()


    def plot_hist_and_gaussian(self, list_hr_data, list_mean_std, counter = 0):
        fig, axs = plt.subplots(2,2)
        fig.suptitle("Hr for testperson " + str(counter) + " efter endt stresstest")
        list_koordinates = [(0,0), (0,1), (1,0), (1,1)]


        for n in range(len(list_koordinates)-1):
            bins = int(round(max(list_hr_data[n])-min(list_hr_data[n])))
            std_low = list_mean_std[n]["std_low"]
            std_high = list_mean_std[n]["std_high"]
            mean_low = list_mean_std[n]["mean_low"]
            mean_high = list_mean_std[n]["mean_high"]
            x_low = np.linspace(mean_low - 3* std_low, mean_low + 3*std_low, 100)
            x_high = np.linspace(mean_high - 3* std_high, mean_high + 3*std_high, 100)
            axs[list_koordinates[n]].plot(x_low, scipy.stats.norm.pdf(x_low, mean_low, std_low), label = 'Mean = ' + str(mean_low) + ' std = ' + str(std_low))
            axs[list_koordinates[n]].plot(x_high, scipy.stats.norm.pdf(x_high, mean_high, std_high), label = 'Mean = ' + str(mean_high) + ' std = ' + str(std_high))
            axs[list_koordinates[n]].hist(list_hr_data[n], bins, facecolor = 'green', alpha= 0.5, density=True)
            axs[list_koordinates[n]].legend(loc = 'upper right')
            axs[list_koordinates[n]].set_xlabel('HR [Bpm]')
            axs[list_koordinates[n]].set_ylabel('Density of heart rate')
            axs[list_koordinates[n]].set_title('Fase ' + str(n))


        fig.set_size_inches(20,10)
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.97, top=0.92, wspace=None, hspace=None)
        path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Figurer/Histogrammer/'
        title = 'Gaussian distributions, Testperson ' + str(counter)
        fig.savefig(path + " " + title) #, dpi = 200)

    