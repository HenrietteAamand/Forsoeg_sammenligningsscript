from stabelisation import stabelisation_class
from scipy.stats import norm
import scipy
import numpy as np
from sklearn.linear_model import LinearRegression

from stabelisation import *
class results_class():
    def __init__(self, fase_intervention_testperson_sammenhaeng) -> None:
        self.intervention = fase_intervention_testperson_sammenhaeng
        self.list_dict_results = []
        self.stabel = stabelisation_class()
        self.id_2_dot_0 = 1
        


    def procces_results(self, Dict_all_data: dict, counter: int):
        testperson_nr = counter
        i = 1
        fs = 0
        list_hr_avg = []
        self.list_mean_std = [] # Bruges til at tegne histogrammet med fordelingerne indtegnet
        index_list = []         # Gemmer de indexer, der er fundet som stabiliseringstidspunktet. 
        self.coef_list = []     # Gemmer hældningskoefficienten sat skæringen med y-aksen

        # Dette gøres 4 gange svarende til de 4 faser. Ved baseline ønskes der ikke at gøre noge. 
        while i < 4: #denne tæller faser, jeg skal ikke forholde mig til antal personer
            if (i == 0):
                pass
            else:
                if(testperson_nr == 1): # hvis vi er i gang med testperson 1, svarende til at vi bruger maxrefdes data
                    signal_original = Dict_all_data[testperson_nr]['Hr_Maxrefdes103_' + str(i)]
                    signal_name="Hr_Maxrefdes103_"
                    fs = 25
                else: #Alle de andre gange bruger vi HRM-Pro
                    signal_original = Dict_all_data[testperson_nr]['Hr_Hrmpro_' + str(i)]
                    signal_name = "Hr_Hrmpro_"
                    fs = 4

                # Bestemmer ved hvilket index signalet er stabilt med gmm-metoden
                N = fs*10
                signal_original = Dict_all_data[testperson_nr][signal_name + str(i)]
                hr_avg = self.__get_filtered_signal(signal_original, N)
                list_hr_avg.append(hr_avg)
                index_gmm = self.stabel.gmm(hr_avg)
                index_soren = self.stabel.soren(signal_original, N)
                dict_index = {}
                dict_index['soren'] = index_soren
                dict_index['gmm'] = index_gmm
                index_list.append(dict_index)
                delta_tid_garmin = 1/fs

                # Gemmer resultaterne af gmm()
                std_low, std_high = self.stabel.get_stds()
                mean_low, mean_high = self.stabel.get_means()
                dict_mean_std = {}
                dict_mean_std["std_low"] = std_low
                dict_mean_std["std_high"] = std_high
                dict_mean_std["mean_low"] = mean_low
                dict_mean_std["mean_high"] = mean_high
                self.list_mean_std.append(dict_mean_std)

                # gemmer de resultater der skal laves statistik af, så de senere lan gemmes i en fil
                tid1 = index_gmm*delta_tid_garmin
                maximum_hr = max(hr_avg)
                hastighed = self.linear_regression(hr_avg,fs, index_gmm)[0][0]     # Der er to metoder til at finde hastigheden, her bruges lineær regression
                # hastighed = (mean_low-maximum_hr)/(tid1)
                stabiliseringsniveau, denhoje = self.stabel.get_means()
                
                # Jeg vil gerne gemm hvilken intervention der hører til dette datasæt. Derfor skal jeg ind i interventionslisten og finde den intervention, hvor fasenumrene og testpersonnummmeret matcher
                n=0
                while(n < 3):
                    index2 = testperson_nr*3+n-3 # Jeg trækker 3 fra, fordi jeg hver gang ganger med 3, og dermed lander 1c person for langt fremme
                    fasenummer = self.intervention[index2]['fase']
                    if(fasenummer == str(i)):
                        intervention = self.intervention[index2]['intervention']
                        break
                    n+=1
                dict_results = {}
                dict_results['ID 2.0'] = self.id_2_dot_0
                dict_results['ID 1.0'] = testperson_nr
                dict_results['Mean'] = stabiliseringsniveau
                dict_results['Condition'] = intervention
                dict_results['Time'] = tid1
                dict_results['Max'] = maximum_hr
                dict_results['Velocity (bpm/s)'] = hastighed

                self.list_dict_results.append(dict_results)
                i+=1

        self.id_2_dot_0 += 1
        self.plot_hist_and_gaussian(list_hr_data=list_hr_avg, list_mean_std = self.list_mean_std, counter=testperson_nr)
        return index_list
        

    def __get_filtered_signal(self, raw_signal, average_value):
        N = average_value
        if(N%2 == 0):
            N+=1
        hr_avg = np.convolve(raw_signal, np.ones(N)/N, mode='same')
        hr_return = hr_avg[N:len(hr_avg)-N]
        return hr_return

    def Get_results_as_list(self):
        new_returnlist = []
        raekkefoelge = ['Silent', 'Static', 'Dynamic']
        i = 0
        while( i < len(self.list_dict_results)):
            for n in range(3):
                for j in range(3):
                    condition = self.list_dict_results[i+j]['Condition'] 
                    raekkefoelge_index = raekkefoelge[n]
                    if(condition == raekkefoelge_index):
                        new_returnlist.append(self.list_dict_results[i+j])
                        break

            i +=3


        return new_returnlist


    def Empty_dict(self):
        self.list_dict_results.clear()


    def plot_hist_and_gaussian(self, list_hr_data, list_mean_std, counter = 0):
        fig, axs = plt.subplots(2,2)
        fig.suptitle("Hr for testperson " + str(counter) + " efter endt stresstest")
        list_koordinates = [(0,1), (1,0), (1,1), (0,0)]


        for n in range(len(list_koordinates)-1):
            bins = int(round(max(list_hr_data[n])-min(list_hr_data[n])))
            std_low = round(list_mean_std[n]["std_low"],2)
            std_high = round(list_mean_std[n]["std_high"],2)
            mean_low = round(list_mean_std[n]["mean_low"],2)
            mean_high = round(list_mean_std[n]["mean_high"],2)
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

    def get_mean_and_std_list(self):
        # std_low = round(self.list_mean_std[n]["std_low"],2)
        # mean_low = round(self.list_mean_std[n]["mean_low"],2)
        return self.list_mean_std

    def __get_time(self, signal_avg, fs):
        delta_tid = 1/fs
        tid_avg = len(signal_avg)/fs
        tidsakse_avg = np.arange(0,tid_avg, delta_tid)
        return tidsakse_avg

    def linear_regression(self, signal_avg = [], fs = 4, index = 0):
        y = signal_avg[:index] # Vil kun lave lineær regression på data indtil det index hvor vi har fundet stabiliseringstiden
        X = self.__get_time(y, fs).reshape(-1,1)
        y = y.reshape(-1,1)
        reg = LinearRegression(copy_X=True).fit(X, y)
        reg.score(X, y)
        coef = reg.coef_
        dict_coefficients = {}
        dict_coefficients['coef'] = round(coef[0][0],3)
        dict_coefficients['intercept'] = round(reg.intercept_[0],3)
        self.coef_list.append(dict_coefficients)
        return coef

    def get_coefs(self):
        return self.coef_list