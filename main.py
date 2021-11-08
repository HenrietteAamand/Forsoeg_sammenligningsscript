import filereader, extract_hrmpro, extract_maxrefdes103, tidskorrigering, extract_empatica
from plotter import plotter_class

path = "C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Data"
fr = filereader.filereader_class(path=path)
tk = tidskorrigering.tidskorrigering_class(1635761570409,63780218)
hrm_pro = extract_hrmpro.extract_hrmpro_class(fr,tk)
maxrefdes103 = extract_maxrefdes103.extract_maxrefdes103_class(fr)
empatica = extract_empatica.extract_empatica_class(fr, tk)
plotter = plotter_class()

counter = 1
fasenummer = 1
antal_testpersoner = 1

Dict_with_obs = { }
Dict_with_obs[counter] = {}
while(counter <=antal_testpersoner):
    testpersonnummer = counter
    maxrefdes103.extract(testpersonnummer,fasenummer)
    timelim_begin = maxrefdes103.get_first_timestamp()
    timelim_end = maxrefdes103.get_last_timestamp()
    hrm_pro.extract(testpersonnummer,timelim_begin=timelim_begin, timelim_end=timelim_end)
    empatica.extract(testpersonnummer,timelim_begin, timelim_end)

    Dict_with_obs[counter]['Hr_Maxrefdes103_' + str(fasenummer)] = maxrefdes103.get_hr()
    Dict_with_obs[counter]['RR_Maxrefdes103_' + str(fasenummer)] = maxrefdes103.get_rr()
    Dict_with_obs[counter]["Hr_Hrmpro_" + str(fasenummer)] = hrm_pro.get_hr()
    Dict_with_obs[counter]["RR_Hrmpro_" + str(fasenummer)] = hrm_pro.get_rr()
    Dict_with_obs[counter]["Hr_empatica_" + str(fasenummer)] =empatica.get_hr()
    # Dictionary_with_all_observations[str(counter)]["Hr_forerunner_" + str(fasenummer)] = maxrefdes103.get_hr()
    fasenummer += 1
    if(fasenummer > 3):
        counter += 1
        fasenummer = 1
        Dict_with_obs[counter] = {}
        hrm_pro.set_read_from_file_bool(True)
        empatica.set_read_from_file_bool(True)
        
        #Forerunner

counter = 1

plotter.plot_hr(maxrefdes= Dict_with_obs[counter]['Hr_Maxrefdes103_1'], hrm_pro=Dict_with_obs[counter]['Hr_Hrmpro_1'], empatica=Dict_with_obs[counter]['Hr_empatica_1'])


