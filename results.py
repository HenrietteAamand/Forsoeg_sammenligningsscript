from stabelisation import stabelisation_class


from stabelisation import *
class results_class():
    def __init__(self, fase_intervention_testperson_sammenhaeng) -> None:
        self.intervention = fase_intervention_testperson_sammenhaeng
        self.list_dict_results = []
        self.stabel = stabelisation_class()


    def procces_results(self, Dict_all_data: dict, counter: int):
        i = 1
        fs_garmin = 4
        while i < 4: #denne tæller faser, jeg skal ikke forholde mig til antal personer. Måske skal jeg gemme i en global liste? Så kan jeg hente denne liste til sidst, og gemme den fra main? Ja det giver en løsere kobling. 
            hr_hrm_pro = Dict_all_data[counter]['Hr_Hrmpro_' + str(i)]
            hr_avg = self.__get_filtered_signal(hr_hrm_pro, 51)
            index = self.stabel.gmm(hr_avg)
            delta_tid_garmin = 1/fs_garmin

            tid = index*delta_tid_garmin
            maximum_hr = max(hr_avg)
            hastighed = maximum_hr/(tid)
            stabiliseringsniveau = self.stabel.get_mean()
            n=0
            while(n < 3):
                index2 = counter*3+n-3
                fasenummer = self.intervention[index2]['fase']
                if(fasenummer == str(i)):
                    intervention = self.intervention[index2]['intervention']
                n+=1
            dict_results = {}
            dict_results['ID'] = counter
            dict_results['Mean'] = stabiliseringsniveau
            dict_results['Condition'] = intervention
            dict_results['Time'] = tid
            dict_results['Max'] = maximum_hr
            dict_results['Velocity (bpm/s)'] = hastighed

            self.list_dict_results.append(dict_results)
            i+=1


    def __get_filtered_signal(self, raw_signal, average_value):
        N = average_value
        if(N%2 == 0):
            N+=1
        hr_avg = np.convolve(raw_signal, np.ones(N)/N, mode='same')
        return hr_avg

    def Get_results_as_list(self):
        return self.list_dict_results