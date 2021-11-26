import keyboard
from csv import DictReader
from Sammenligning import sammenligning_class
from extract_forerunner import extract_forerunner_class
import filereader, extract_hrmpro, extract_maxrefdes103, tidskorrigering, extract_empatica, datetime
from results import results_class
from plotter import plotter_class
import numpy as np

class main_class:
    def __init__(self, antal_testpersoner: int, filereader : filereader.filereader_class) -> None:
        self.antal_testpersoner = antal_testpersoner
        self.fr = filereader
        
    def extract_data(self):
        fr = self.fr
        tk = tidskorrigering.tidskorrigering_class()
        hrm_pro = extract_hrmpro.extract_hrmpro_class(fr,tk)
        forerunner = extract_forerunner_class(fr,tk)
        maxrefdes103 = extract_maxrefdes103.extract_maxrefdes103_class(fr)
        empatica = extract_empatica.extract_empatica_class(fr, tk)

        dict_sensorcount = fr.read_sensorcount()
        tk.set_birthtime_sensor(dict_sensorcount[0]['Absolute_count'], dict_sensorcount[0]['Sensor_count'])

        counter = 1
        fasenummer = 0
        antal_testpersoner = self.antal_testpersoner

        Dict_with_obs = { }
        Dict_with_obs[counter] = {}
        while(counter <= antal_testpersoner):
            testpersonnummer = counter
            maxrefdes103.extract(testpersonnummer,fasenummer)
            timelim_begin = maxrefdes103.get_first_timestamp()
            #my_datetime = datetime.datetime.fromtimestamp(timelim_begin/1000).strftime('%d/%m/%y %H:%M:%S.%f')
            #print("Maxrefdes103: " + my_datetime)
            timelim_end = maxrefdes103.get_last_timestamp()
            hrm_pro.extract(testpersonnummer,timelim_begin=timelim_begin, timelim_end=timelim_end)
            empatica.extract(testpersonnummer,timelim_begin= timelim_begin, timelim_end = timelim_end)
            forerunner.extract(testpersonnummer,timelim_begin=timelim_begin, timelim_end=timelim_end)
            Dict_with_obs[counter]['Hr_Maxrefdes103_' + str(fasenummer)] = maxrefdes103.get_hr()
            Dict_with_obs[counter]['RR_Maxrefdes103_' + str(fasenummer)] = maxrefdes103.get_rr()
            Dict_with_obs[counter]["Hr_Hrmpro_" + str(fasenummer)] = hrm_pro.get_hr()
            Dict_with_obs[counter]["RR_Hrmpro_" + str(fasenummer)] = hrm_pro.get_rr()
            Dict_with_obs[counter]["Hr_Forerunner_" + str(fasenummer)] = forerunner.get_hr()
            Dict_with_obs[counter]["RR_Forerunner_" + str(fasenummer)] = forerunner.get_rr()
            Dict_with_obs[counter]["Hr_Empatica_" + str(fasenummer)] =empatica.get_hr()
            Dict_with_obs[counter]["RR_Empatica_" + str(fasenummer)] =empatica.get_rr()
            
            delta_time = timelim_end-timelim_begin
            sum_maxrefdes = sum(Dict_with_obs[counter]['RR_Maxrefdes103_' + str(fasenummer)])
            sum_hrmpro = sum(Dict_with_obs[counter]["RR_Hrmpro_" + str(fasenummer)])
            sum_empatica = sum(Dict_with_obs[counter]["RR_Empatica_" + str(fasenummer)])

            #print("Deltatid = " + str(delta_time) + ", maxrefdes differens = " + str(delta_time - sum_maxrefdes) + ", HRM-Pro differens = " + str(delta_time - sum_hrmpro) + ", Empatica differens = " + str(delta_time - sum_empatica))
            #print("Length forerun hr = " + str(len(Dict_with_obs[counter]["RR_Forerunner_" + str(fasenummer)])) + "\nLength hrm-pro hr = " + str(len(Dict_with_obs[counter]["RR_Hrmpro_" + str(fasenummer)])))

            # Dictionary_with_all_observations[str(counter)]["Hr_forerunner_" + str(fasenummer)] = maxrefdes103.get_hr()
            fasenummer += 1
            if(fasenummer > 3 and counter <= antal_testpersoner):
                counter += 1
                fasenummer = 0
                hrm_pro.set_read_from_file_bool(True)
                empatica.set_read_from_file_bool(True)
                forerunner.set_read_from_file_bool(True)
                if(counter <=antal_testpersoner):
                    tk.set_birthtime_sensor(dict_sensorcount[counter-1]['Absolute_count'], dict_sensorcount[counter-1]['Sensor_count'])
                    Dict_with_obs[counter] = {}
                print(str(counter-1) + " new person extracted")
                #Forerunner
        fr.save_hr_data(Dict_with_obs)


antal_testpersoner = 14
plotter = plotter_class()
path = "C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Data"
fr = filereader.filereader_class(path=path)
sammenligner = sammenligning_class()
main = main_class(antal_testpersoner, fr)
fase_intervention = fr.read_fase_to_intervention_file().copy()
to_results = fase_intervention.copy()
resultater = results_class(to_results)

i = 0
n = 0
brugbare_datasaet = [1,5,8,9,11,12,13,14]# Lav ny liste, og tilføj kun de elementer asom du skal bruge, altså dem der hører til de brugbare datasæt
fase_intervention_brugbare = []

while( i < len(fase_intervention)):
    if(fase_intervention[i]['testperson'] == str(brugbare_datasaet[n])):
        dicht_basline = {}
        dicht_basline['testperson'] = str(brugbare_datasaet[n])
        dicht_basline['fase'] = '0'
        dicht_basline['intervention'] = 'Baseline'
        fase_intervention_brugbare.append(dicht_basline)
        n += 1
        for r in range(3):
            fase_intervention_brugbare.append(fase_intervention[i])
            i+=1
    else:
        i+= 3

#main.extract_data()
Dict_with_obs_file = fr.read_hr_data()
counter = 1
antal_testpersoner = 14
# Plotter alle hr afhængigt af tiden
# while counter <= antal_testpersoner:
#     counter += 1

l = 0
# Plotter alle hr afhængigt af tiden
for n in range(len(brugbare_datasaet)):
    #sammenligner.plot_differences(Dict_with_obs_file, counter=counter)
    plotter.plot_hr_subplot(Dict_all_data=Dict_with_obs_file, counter=brugbare_datasaet[n])
    #sammenligner.plot_corellation(Dict_with_obs_file, counter=counter)
    #sammenligner.plot_normal_distribution(Dict_with_obs_file, counter = counter, type='QQ') #type = 'hist'
    #sammenligner.plot_2_percentage_under(Dict_with_obs_file, counter)
    indexlist = resultater.procces_results(Dict_with_obs_file, counter = brugbare_datasaet[n])
    list_mean_std = resultater.get_mean_and_std_list()
    plotter.plot_limit_HRM_pro(Dict_with_obs_file, counter = brugbare_datasaet[n], index_list= indexlist, list_mean_std=list_mean_std, hastighed_list=resultater.get_coefs(), fase_intervention_list=fase_intervention_brugbare)

    print(str(n+1) + " new figure(s) created")

fr.save_results(resultater.Get_results_as_list())
#input("Press Enter to continue...")
resultater.Empty_dict()

# while(counter <= antal_testpersoner):
#     plotter.plot_hr(maxrefdes= Dict_with_obs_file[counter]['Hr_Maxrefdes103_1'], hrm_pro=Dict_with_obs_file[counter]['Hr_Hrmpro_1'], empatica=Dict_with_obs_file[counter]['Hr_Empatica_1'], forerunner=Dict_with_obs_file[counter]['Hr_Forerunner_1'])
#     plotter.plot_hr(maxrefdes= Dict_with_obs_file[counter]['Hr_Maxrefdes103_2'], hrm_pro=Dict_with_obs_file[counter]['Hr_Hrmpro_2'], empatica=Dict_with_obs_file[counter]['Hr_Empatica_2'], forerunner=Dict_with_obs_file[counter]['Hr_Forerunner_2'])
#     plotter.plot_hr(maxrefdes= Dict_with_obs_file[counter]['Hr_Maxrefdes103_3'], hrm_pro=Dict_with_obs_file[counter]['Hr_Hrmpro_3'], empatica=Dict_with_obs_file[counter]['Hr_Empatica_3'], forerunner=Dict_with_obs_file[counter]['Hr_Forerunner_3'])
#     plotter.plot_rr(maxrefdes= Dict_with_obs_file[counter]['RR_Maxrefdes103_1'], hrm_pro=Dict_with_obs_file[counter]['RR_Hrmpro_1'], empatica=Dict_with_obs_file[counter]['RR_Empatica_1'], forerunner=Dict_with_obs_file[counter]['RR_Forerunner_1'])
#     plotter.plot_rr(maxrefdes= Dict_with_obs_file[counter]['RR_Maxrefdes103_2'], hrm_pro=Dict_with_obs_file[counter]['RR_Hrmpro_2'], empatica=Dict_with_obs_file[counter]['RR_Empatica_2'], forerunner=Dict_with_obs_file[counter]['RR_Forerunner_2'])
#     plotter.plot_rr(maxrefdes= Dict_with_obs_file[counter]['RR_Maxrefdes103_3'], hrm_pro=Dict_with_obs_file[counter]['RR_Hrmpro_3'], empatica=Dict_with_obs_file[counter]['RR_Empatica_3'], forerunner=Dict_with_obs_file[counter]['RR_Forerunner_3'])
#     counter += 1


