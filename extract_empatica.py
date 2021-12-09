from IExtract import IExtract
from filereader import filereader_class
from tidskorrigering import tidskorrigering_class
import datetime, time

class extract_empatica_class(IExtract):
    def __init__(self,filereader: filereader_class, tidskorrigering: tidskorrigering_class) -> None:
        self.filereader = filereader
        self.tidkorr = tidskorrigering
        self.read_from_file = True
        self.hr_full_timeperiod = []
        self.rr_full_timeperiod = []

    def extract(self, testpersonnummer: int, timelim_begin: int, timelim_end : int):
        """Metoden udtrækker HR og IBI. Det er også via denne metode der tidskorrigeres, så tidsintervallerne kan sammenlignes på tværs af sensorer

        Args:
            testpersonnummer (int): nummeret på den testperson man er ved at udtrække data fra. Bruges i filereader
            timelim_begin (int): Tidspunktet hvorfra der skal gemmes data. Dette er det første tidspunkt i Maxrefdes103 data grundet forsøgets opsætning.
            timelim_end (int): Tidspunktet, hvor man ikke længere skal bruge data
        """
        # Data indlæses kun en gang pr person, men gennemløbes 4 gange svarende til de 4 faser.  
        if(self.read_from_file):
            data_list_hr = self.filereader.read_empatica(testpersonnummer, "HR").copy()
            data_list_rr = self.filereader.read_empatica(testpersonnummer, "IBI").copy()
            data_list_acc = self.filereader.read_empatica(testpersonnummer, "ACC").copy()
            self.read_from_file = False
        
            absolute_hr = self.correct_absolute(data_list_hr[0][0])  # ændre dato for Hr data til dags dato
            step_hr = float(data_list_hr[1][0]) # finder tiden mellem hvert datapunkt
            absolute_rr = self.correct_absolute(data_list_rr[0][0]) # ændre dato for RR data til dags dato
            absolute_acc = self.correct_absolute(data_list_acc[0][0])
            fs_acc = float(data_list_acc[1][0]) #Finder sampelfrekvensen


            # Laver timestamp til hr data
            self.hr_full_timeperiod = [] #liste der indeholder hr data efter de har fået et timestamp.  
            i = 2
            k = 0
            while( i < len(data_list_hr)-1):
                self.dict_hr_and_time = { }
                self.dict_hr_and_time["hr"] = float(data_list_hr[i][0])
                self.dict_hr_and_time["time"] = (float(absolute_hr)+(step_hr*k))*1000 #tilføjer et timestamp til hver hr data
                self.hr_full_timeperiod.append(self.dict_hr_and_time)
                k+=1
                i+=1
            
            # Laver timestamp til RR data
            n = 1
            i = 1
            self.rr_full_timeperiod = []
            self.dict_rr_and_time = { }
            while(i<len(data_list_rr)-1):
                self.dict_rr_and_time = { }
                data = data_list_rr[n]
                self.dict_rr_and_time["rr"] = float(data[1])*1000
                self.dict_rr_and_time["time"] = (absolute_rr + (float(data[0])))*1000 #tilføjer et timestamp, men denne gang på en lidt anden mådem fordi tiden er angivet på en anden måde for IBI: '36.406250,0.765625' hvor 36.406 (data[0]) er tiden siden absolute_rr og 0.7 er IBI 
                self.rr_full_timeperiod.append(self.dict_rr_and_time)
                n += 1
                i += 1
            # Udtrækker accelerometerdata, men neddeler med en faktor 8, svarende til at fs = 4
            self.accelerometerX = []
            self.accelerometerY = []
            self.accelerometerZ = []
            self.time_accel_full_timeperiod = []
            accel_limit = 1
            to_g = 1/64
            for i in range(len(data_list_acc)-1):
                if(accel_limit >= 8): #Gemmer kun hver 5. datapunkt
                    dict_accel = {}
                    self.time_accel = {}
                    # self.accelerometerX.append(float(data_list_acc[i][0])*to_g)
                    # self.accelerometerY.append(float(data_list_acc[i][1])*to_g)
                    # self.accelerometerZ.append(float(data_list_acc[i][2])*to_g)
                    dict_accel['x'] = float(data_list_acc[i][0])*to_g
                    dict_accel['y'] = float(data_list_acc[i][1])*to_g
                    dict_accel['z'] = float(data_list_acc[i][2])*to_g
                    self.time_accel["time"] = (absolute_acc + i*(1/fs_acc))*1000
                    self.time_accel["accel"] = dict_accel
                    self.time_accel_full_timeperiod.append(self.time_accel)
                    accel_limit = 0
                accel_limit +=1


        # Data tidskorrigeres i henhold til timelim_begin og timelim_end, der er givet af Maxrefdes103
        self.hr_list, self.time_hr = self.tidkorr.empatica(self.hr_full_timeperiod, timelim_begin, timelim_end, "hr")
        self.rr_list, self.time_rr = self.tidkorr.empatica(self.rr_full_timeperiod, timelim_begin, timelim_end, "rr")
        self.accel_list, self.time_accel = self.tidkorr.empatica(self.time_accel_full_timeperiod, timelim_begin, timelim_end, "accel")
    def get_accelerometerdata(self):
        self.accelerometerX = []
        self.accelerometerY = []
        self.accelerometerZ = []
        for accel_datapoint in self.accel_list:
            self.accelerometerX.append(accel_datapoint['x'])
            self.accelerometerY.append(accel_datapoint['y'])
            self.accelerometerZ.append(accel_datapoint['z'])
        return self.accelerometerX, self.accelerometerY, self.accelerometerZ

    def get_hr(self):
        """En standard get-metode der returnerer hr

        Returns:
            list<float>: Hr returneres som en liste med floats
        """
        return self.hr_list
        
    def get_rr(self):
        """En standard get-metode der returnerer rr

        Returns:
            list<float>: Rr returneres som et dictionary med både RR-værdi samt tidsstamp. Tidsstampet er i Unix epoch timestamp
        """
        
        return self.rr_list
        
    def get_time_rr(self):
        return self.time_rr


    def set_read_from_file_bool(self, value : bool):
        """ Denne bool bruges til at fortælle extract_empatic metoden, at nu skal der indlæses data fra en ny testperson. 
            Dette er implementeret for at data kun indlæses en gang pr. testperson, og ikke 3 gange svarende til de 3 faser
        
        Args:
            value (bool): True hvis vi skal i gang med en ny testperson, False hvis vi er i gang med samme testperson, men bare fase 2 og 3
        """
        self.read_from_file = value

    def correct_absolute(self, absolute : str):
        """Metoden ændre timestamp på ematica data. Alle timestamps omregnes til dags dato. 

        Args:
            absolute (str): Tidspunktet for den første måling. Dette er givet som det første i logfilerne fra empatica

        Returns:
            int: Der returneres en tid med dags dato, men hvor klokkeslettet er bevaret. Tiden returneres som UNIX tid
        """
        absolute_int = int(round(float(absolute)))
        # omregner absolute_int til dato og timestamp
        my_datetime = datetime.datetime.fromtimestamp(absolute_int).strftime('%d/%m/%y %H:%M:%S.%f')
        
        # Laver nyt timestamp med dato fra idag og tidspunktet fra absolute_int
        tid_forkert_dato = str(datetime.datetime.now().date().strftime("%d/%m/%y")) + " " + str(datetime.datetime.fromtimestamp(absolute_int).strftime('%H:%M:%S.%f'))

        #konverterer tilbage til datetime obj
        my_datetime = datetime.datetime.strptime(tid_forkert_dato, '%d/%m/%y %H:%M:%S.%f')

        #koverterer tilbage til Unix Epoch timestamp
        absolute_time = int((time.mktime(my_datetime.timetuple())))

        return absolute_time