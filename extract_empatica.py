from filereader import filereader_class
from tidskorrigering import tidskorrigering_class
import datetime, time

class extract_empatica_class():
    def __init__(self,filereader: filereader_class, tidskorrigering: tidskorrigering_class) -> None:
        self.filereader = filereader
        self.tidkorr = tidskorrigering
        self.read_from_file = True
        self.hr_full_timeperiod = []
        self.rr_full_timeperiod = []


    def extract(self, testpersonnummer: int, timelim_begin: int, timelim_end : int):
        if(self.read_from_file):
            data_list_hr = self.filereader.read_empatica(testpersonnummer, "HR").copy()
            data_list_rr = self.filereader.read_empatica(testpersonnummer, "IBI").copy()
            self.read_from_file = False
        
            absolute_hr = self.correct_absolute(data_list_hr[0][0])  #float(data_list_hr[0][0])
            step_hr = float(data_list_hr[1][0])
            absolute_rr = self.correct_absolute(data_list_rr[0][0])

            self.hr_full_timeperiod = []
            i = 2
            k = 0
            while( i< len(data_list_hr)-1):
                self.dict_hr_and_time = { }
                self.dict_hr_and_time["hr"] = float(data_list_hr[i][0])
                self.dict_hr_and_time["time"] = (float(absolute_hr)+(step_hr*k))*1000
                self.hr_full_timeperiod.append(self.dict_hr_and_time)
                k+=1
                i+=1
            
            n = 1
            i = 1
            self.rr_full_timeperiod = []
            self.dict_rr_and_time = { }
            while(i<len(data_list_rr)-1):
                self.dict_rr_and_time = { }
                data = data_list_rr[n]
                self.dict_rr_and_time["rr"] = float(data[1])*1000
                self.dict_rr_and_time["time"] = (absolute_rr + (float(data[0])))*1000
                self.rr_full_timeperiod.append(self.dict_rr_and_time)
                n += 1
                i += 1

        self.hr_list = self.tidkorr.empatica(self.hr_full_timeperiod, timelim_begin, timelim_end, 'hr').copy()
        self.rr_list = self.tidkorr.empatica(self.rr_full_timeperiod, timelim_begin, timelim_end, 'rr').copy()

    def get_hr(self):
        return self.hr_list
        

    def get_rr(self):
        return self.rr_list

    def set_read_from_file_bool(self, value : bool):
        self.read_from_file = value

    def correct_absolute(self, absolute : str):
        absolute_int = int(round(float(absolute)))
        my_datetime = datetime.datetime.fromtimestamp(absolute_int).strftime('%d/%m/%y %H:%M:%S.%f')
        #print("Empatica: " + my_datetime)
        tid_forkert_dato = str(datetime.datetime.now().date().strftime("%d/%m/%y")) + " " + str(datetime.datetime.fromtimestamp(absolute_int).strftime('%H:%M:%S.%f'))
        my_datetime = datetime.datetime.strptime(tid_forkert_dato, '%d/%m/%y %H:%M:%S.%f')
        absolute_time = int((time.mktime(my_datetime.timetuple())))
        return absolute_time