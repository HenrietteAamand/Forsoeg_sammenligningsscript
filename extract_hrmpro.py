

from filereader import filereader_class
from tidskorrigering import tidskorrigering_class
from Calculate_RR_class import *


class extract_hrmpro_class():
    def __init__(self, filereader: filereader_class, tidskorrigering: tidskorrigering_class) -> None:
        self.filereader = filereader
        self.tidkorr = tidskorrigering
        self.rr_calculator = Caculate_rr_class()
        self.read_from_file = True
        self.lines_splitted = []

    def extract(self, testpersonnummer : int, timelim_begin: int, timelim_end : int, ):
        if(self.read_from_file):
            lines_from_file = self.filereader.read_HRMpro(testpersonnummer)
            self.lines_splitted = self.tidkorr.hrm_pro(lines_from_file, timelim_begin, timelim_end)
            self.read_from_file = False

        oldtogglebit = 0
        # I den hexadecimale streng udtrækkes hver byte og gemmes i et dictionary sammen med den udregnede tid
        self.New_list_with_logged_values_as_dictionay = []
        for sensordata in self.lines_splitted:
            dictionary_with_hex ={} 
            if len(sensordata) == 3:
                if 'Rx' in sensordata[1]:
                    temporary_List = sensordata[2][1:-2].split('][')
                    if(oldtogglebit != temporary_List[6]): #Yderligere gemmes kun data, når der har været et nyt 'heart-beat-event svarende til at hr_count er blevet en større
                        dictionary_with_hex["b0"] = temporary_List[0]
                        dictionary_with_hex["b1"] = temporary_List[1]
                        dictionary_with_hex["b2"] = temporary_List[2]
                        dictionary_with_hex["b3"] = temporary_List[3]
                        dictionary_with_hex["LSB"] = temporary_List[4]
                        dictionary_with_hex["MSB"] = temporary_List[5]
                        dictionary_with_hex["hr_count"] = temporary_List[6]
                        dictionary_with_hex["hr"] = temporary_List[7]
                        dictionary_with_hex["time"] = sensordata[0]
                        self.New_list_with_logged_values_as_dictionay.append(dictionary_with_hex)
                    oldtogglebit = temporary_List[6]
        
        #Bruger data page 4 til at omregne til RR-værdier
        self.list_of_rr_and_time = self.rr_calculator.rr_4(self.New_list_with_logged_values_as_dictionay)
        return self.list_of_rr_and_time

    def get_rr(self, given_delay): #given_delay sættes, hvis der ønskes at manipulere med længden af HRM_pro rr værierne
        # Modificerer rr-værdierne ved at udtrække rr værdier uden tiden.
        rr = []
        if len(self.list_of_rr_and_time) > 0:
            for dict in self.list_of_rr_and_time:
                rr.append(dict['rr'])
        else:
            print("please extract rr data with the extract_rr_values-method before getting the rr-values in a separate list")
        return rr
    
    def get_hr(self):
        hr = []
        for measurement in self.New_list_with_logged_values_as_dictionay:
            hr.append(int(measurement["hr"],16))
        return(hr)

    def set_read_from_file_bool(self, value : bool):
        self.read_from_file = value

