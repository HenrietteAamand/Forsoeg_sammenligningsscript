from filereader import filereader_class
from tidskorrigering import tidskorrigering_class
from Calculate_RR_class import *

class extract_forerunner_class():
    def __init__(self, filereader: filereader_class, tidskorrigering: tidskorrigering_class) -> None:
        self.filereader = filereader
        self.tidkorr = tidskorrigering
        self.rr_calculator = Caculate_rr_class()
        self.read_from_file = True
        self.lines_splitted = []

    def extract(self, testpersonnummer : int, timelim_begin: int, timelim_end : int):
        """Metoden udtrækker HR og RR. Det er også via denne metode der tidskorrigeres, så tidsintervallerne kan sammenlignes på tværs af sensorer
           RR-værdierne er dog usikre, og har nogle sære store peaks. Dette kan skyldes, at nogle gange fejler en pakke (82286937 : Rx fail)

        Args:
            testpersonnummer (int): nummeret på den testperson man er ved at udtrække data fra. Bruges i filereader
            timelim_begin (int): Tidspunktet hvorfra der skal gemmes data. Dette er det første tidspunkt i Maxrefdes103 data grundet forsøgets opsætning.
            timelim_end (int): Tidspunktet, hvor man ikke længere skal bruge data
        """
        if(self.read_from_file):
            lines_from_file = self.filereader.read_forerunner(testpersonnummer)
            self.lines_splitted = self.tidkorr.forerunner(lines_from_file, timelim_begin, timelim_end)
            self.read_from_file = False
        self.hr_list = []
        oldtogglebit = 0
        # I den hexadecimale streng udtrækkes hver byte og gemmes i et dictionary sammen med den udregnede tid
        self.New_list_with_logged_values_as_dictionay = []
        for sensordata in self.lines_splitted:
            dictionary_with_hex ={} 
            if len(sensordata) == 3:
                if 'Rx' in sensordata[1]:
                    temporary_List = sensordata[2][1:-2].split('][')
                    self.hr_list.append(temporary_List[7])
                    if(oldtogglebit != temporary_List[6] and temporary_List[0][2] == '0'): #Yderligere gemmes kun data, når der har været et nyt 'heart-beat-event svarende til at hr_count er blevet en større
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
        self.list_of_rr_and_time = self.rr_calculator.rr_0(self.New_list_with_logged_values_as_dictionay)
        return self.list_of_rr_and_time

    def get_rr(self): 
        """ Metoden returnerer en liste med rr-værdier.

        Returns:
            List<float>: Rr returneres som en liste med floats
        """
        # Modificerer rr-værdierne ved at udtrække rr værdier uden tiden.
        rr_list = []
        if len(self.list_of_rr_and_time) > 0:
            for dict in self.list_of_rr_and_time:
                rr_list.append(dict['rr'])
        else:
            #print("please extract rr data with the extract_rr_values-method before getting the rr-values in a separate list")
            pass
        return rr_list
    
    def get_hr(self):
        """ Metoden returnerer en liste med Hr-værdier.

        Returns:
            List<float>: Hr returneres som en liste med floats
        """
        hr_list = []
        for hr in self.hr_list: #self.New_list_with_logged_values_as_dictionay:
            hr_list.append(int(hr,16))
        return(hr_list)

    def set_read_from_file_bool(self, value : bool):
        """ Denne bool bruges til at fortælle extract_empatic metoden, at nu skal der indlæses data fra en ny testperson. 
            Dette er implementeret for at data kun indlæses en gang pr. testperson, og ikke 3 gange svarende til de 3 faser
        
        Args:
            value (bool): True hvis vi skal i gang med en ny testperson, False hvis vi er i gang med samme testperson, men bare fase 2 og 3
        """
        self.read_from_file = value
        
    