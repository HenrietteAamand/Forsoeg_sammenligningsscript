import keyboard
from csv import DictReader
from Sammenligning import sammenligning_class
from extract_forerunner import extract_forerunner_class
import filereader, extract_hrmpro, extract_maxrefdes103, tidskorrigering, extract_empatica, datetime
from results import results_class
from plotter import plotter_class
from Calculate_RR_class import Caculate_rr_class
import numpy as np

class main_class:
    def __init__(self, antal_testpersoner: int, counter: int, filereader : filereader.filereader_class) -> None:
        """initialiseringsklasse. Her kan man sætte startværdierne

        Args:
            counter: Den testperson man ønsker at starte indlæsningen fra. Sættex den til 5 indlæses eks testperson 5 til 'antal_testpersoner'
            antal_testpersoner (int): Antal testpersoner er antallet af testpersoner man ønsker at indlæse. Det kan sættes fra 1 - 14. Antal testpersoner skal være større end counter
            filereader (filereader.filereader_class): Filereader klasse, der er fælles for alle exctract klasser. 
        """
        self.counter = counter
        self.antal_testpersoner = antal_testpersoner
        self.fr = filereader
        
    def extract_data(self):
        """Metoden køres kun, når data skal hentes fra de oprindelie datafiler på ny. Den er sat til at hente data fra samtlige sensorer. Dette kan ændres inden i metoden
        """
        # Opretter de nøvnendige klasser 
        fr = self.fr
        tk = tidskorrigering.tidskorrigering_class()
        RR_calculater = Caculate_rr_class()
        hrm_pro = extract_hrmpro.extract_hrmpro_class(fr,tk, RR_calculater)
        forerunner = extract_forerunner_class(fr,tk, RR_calculater)
        maxrefdes103 = extract_maxrefdes103.extract_maxrefdes103_class(fr)
        empatica = extract_empatica.extract_empatica_class(fr, tk)

        # Henter det sensercount der stemmer overens med et tilhørende unix epoch timestamp 
        dict_sensorcount = fr.read_dict_to_list('/sensorcount.csv')
        
        # sætter birtcount og sensercount for det første gennemløb. Herefter ændres dette i whileloopet. 
        tk.set_birthtime_sensor(dict_sensorcount[0]['Absolute_count'], dict_sensorcount[0]['Sensor_count'])
        
        counter = self.counter  # Nummeret på den første testperson. Ændres dette til eks 5 indlæses fra testperson 5 og fremefter
        fasenummer = 0
        antal_testpersoner = self.antal_testpersoner

        # Dette dictionary med dictionaries bruges til at gemme samtlige data. Key for dict 1 er testpersonnummer, og key for 'under dict' er eks HR_SENSORNAVN_FASENUMMER
        Dict_with_obs = { }
        Dict_with_obs[counter] = {}

        #Dette loop indlæser de ønskede data. Sættes counter til 1 og antal_testpersoner til 14 så indlæses data fra samtlige testpersoner.
        while(counter <= antal_testpersoner):
            testpersonnummer = counter
            maxrefdes103.extract(testpersonnummer,fasenummer)
            timelim_begin = maxrefdes103.get_first_timestamp()
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
        # slutteligt gemmes data i en fil, så man ikke beøver hente og behandle data fra de oprindelige datafiler hver gang scriptet køres. 
        fr.save_hr_data(Dict_with_obs)

# Opsætter programmet
antal_testpersoner = 14 #Indlæser fra alle forsøgspersoner
plotter = plotter_class()
path = "C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Data"
fr = filereader.filereader_class(path=path)
sammenligner = sammenligning_class()
main = main_class(antal_testpersoner, 1, fr)
fase_intervention = fr.read_dict_to_list('/testperson_fase_intervention.csv').copy()# fase_intervention er en list, der sammenkobler fasenummer og intervention for ghver enkelt forsøgsperson. Denne bruges til plotsne. 
to_results = fase_intervention.copy()
resultater = results_class(to_results)

i = 0
n = 0
brugbare_datasaet = [1,5,8,9,11,12,13,14] # Lav ny liste, og tilføj kun de elementer som du skal bruge, altså dem der hører til de brugbare datasæt
fase_intervention_brugbare = []

#Gemmer kun fase-interventyionssammenhæng for de brugbare dataslæt
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

#main.extract_data() #indkommenteres hvis data skal indlæses på ny.
Dict_with_obs_file = fr.read_hr_data() # Bruges i stedet for main.extract_data(), hvor data bare indlæses fra en fil.
counter = 1
antal_testpersoner = 14

l = 0
# Plotter alle hr afhængigt af tiden
for n in range(len(brugbare_datasaet)):
    # sammenligner.plot_differences(Dict_with_obs_file, counter=counter)
    # plotter.plot_hr_subplot(Dict_all_data=Dict_with_obs_file, counter=brugbare_datasaet[n])
    # sammenligner.plot_corellation(Dict_with_obs_file, counter=counter)
    # #sammenligner.plot_normal_distribution(Dict_with_obs_file, counter = counter, type='hist') #type = 'QQ'
    # sammenligner.plot_2_percentage_under(Dict_with_obs_file, counter)
    indexlist = resultater.process_results(Dict_with_obs_file, counter = brugbare_datasaet[n])
    list_mean_std = resultater.get_mean_and_std_list()
    velocity_list_two_point = resultater.get_velocity_two_point()
    velocity_list_lin_reg = resultater.get_coefs()
    plotter.plot_limit_HRM_pro(Dict_with_obs_file, counter = brugbare_datasaet[n], index_list= indexlist, list_mean_std=list_mean_std, hastighed_lin_reg=velocity_list_lin_reg, fase_intervention_list=fase_intervention_brugbare, hastighed_two_points=velocity_list_two_point)

    print(str(n+1) + " new figure(s) created")

# Gemmer resultater til en .csv fil, så de kan analyseres i et statistik program 
fr.save_results(resultater.Get_results_as_list(), 'results.csv')
fr.save_results(plotter.get_velocities(), 'velocities.csv')
resultater.Empty_result_dict()



