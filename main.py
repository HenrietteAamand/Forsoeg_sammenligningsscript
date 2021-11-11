from csv import DictReader
from extract_forerunner import extract_forerunner_class
import filereader, extract_hrmpro, extract_maxrefdes103, tidskorrigering, extract_empatica, datetime
from plotter import plotter_class

path = "C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Data"
fr = filereader.filereader_class(path=path)
tk = tidskorrigering.tidskorrigering_class(1635761570409,63780218)
hrm_pro = extract_hrmpro.extract_hrmpro_class(fr,tk)
forerunner = extract_forerunner_class(fr,tk)
maxrefdes103 = extract_maxrefdes103.extract_maxrefdes103_class(fr)
empatica = extract_empatica.extract_empatica_class(fr, tk)
plotter = plotter_class()

counter = 1
fasenummer = 0
antal_testpersoner = 14

Dict_with_obs = { }
Dict_with_obs[counter] = {}
while(counter <=antal_testpersoner):
    testpersonnummer = counter
    maxrefdes103.extract(testpersonnummer,fasenummer)
    timelim_begin = maxrefdes103.get_first_timestamp()
    #my_datetime = datetime.datetime.fromtimestamp(timelim_begin/1000).strftime('%d/%m/%y %H:%M:%S.%f')
    #print("Maxrefdes103: " + my_datetime)
    timelim_end = maxrefdes103.get_last_timestamp()
    hrm_pro.extract(testpersonnummer,timelim_begin=timelim_begin, timelim_end=timelim_end)
    empatica.extract(testpersonnummer,timelim_begin, timelim_end)
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
    print("Length forerun hr = " + str(len(Dict_with_obs[counter]["RR_Forerunner_" + str(fasenummer)])) + "\nLength hrm-pro hr = " + str(len(Dict_with_obs[counter]["RR_Hrmpro_" + str(fasenummer)])))

    # Dictionary_with_all_observations[str(counter)]["Hr_forerunner_" + str(fasenummer)] = maxrefdes103.get_hr()
    fasenummer += 1
    if(fasenummer > 3):
        counter += 1
        fasenummer = 0
        Dict_with_obs[counter] = {}
        hrm_pro.set_read_from_file_bool(True)
        empatica.set_read_from_file_bool(True)
        
        #Forerunner

counter = 1
while counter <= antal_testpersoner:
    plotter.plot_hr_subplot(Dict_all_data=Dict_with_obs, counter=counter)
    counter += 1


# while(counter <= antal_testpersoner):
#     plotter.plot_hr(maxrefdes= Dict_with_obs[counter]['Hr_Maxrefdes103_1'], hrm_pro=Dict_with_obs[counter]['Hr_Hrmpro_1'], empatica=Dict_with_obs[counter]['Hr_Empatica_1'], forerunner=Dict_with_obs[counter]['Hr_Forerunner_1'])
#     plotter.plot_hr(maxrefdes= Dict_with_obs[counter]['Hr_Maxrefdes103_2'], hrm_pro=Dict_with_obs[counter]['Hr_Hrmpro_2'], empatica=Dict_with_obs[counter]['Hr_Empatica_2'], forerunner=Dict_with_obs[counter]['Hr_Forerunner_2'])
#     plotter.plot_hr(maxrefdes= Dict_with_obs[counter]['Hr_Maxrefdes103_3'], hrm_pro=Dict_with_obs[counter]['Hr_Hrmpro_3'], empatica=Dict_with_obs[counter]['Hr_Empatica_3'], forerunner=Dict_with_obs[counter]['Hr_Forerunner_3'])
#     plotter.plot_rr(maxrefdes= Dict_with_obs[counter]['RR_Maxrefdes103_1'], hrm_pro=Dict_with_obs[counter]['RR_Hrmpro_1'], empatica=Dict_with_obs[counter]['RR_Empatica_1'], forerunner=Dict_with_obs[counter]['RR_Forerunner_1'])
#     plotter.plot_rr(maxrefdes= Dict_with_obs[counter]['RR_Maxrefdes103_2'], hrm_pro=Dict_with_obs[counter]['RR_Hrmpro_2'], empatica=Dict_with_obs[counter]['RR_Empatica_2'], forerunner=Dict_with_obs[counter]['RR_Forerunner_2'])
#     plotter.plot_rr(maxrefdes= Dict_with_obs[counter]['RR_Maxrefdes103_3'], hrm_pro=Dict_with_obs[counter]['RR_Hrmpro_3'], empatica=Dict_with_obs[counter]['RR_Empatica_3'], forerunner=Dict_with_obs[counter]['RR_Forerunner_3'])
#     counter += 1


