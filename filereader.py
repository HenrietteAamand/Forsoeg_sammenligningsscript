import csv, os.path

class filereader_class:
    def __init__(self, path, filename = "") -> None:
        self.path = path
        self.filename = filename
        
    def read_HRMpro(self, testpersonnummer: int):
        """Metoden læser data fra den logfil, der genereres når man bruger SimulANT+ til at læse data der sendes fra en Garmin(R) ANT+ sensor. 
           Der indlæses en liste, hvor hver plads i listen indeholder en linjje fra logfilen på formen '81722734 : Rx: [00][FF][FF][FF][86][02][9F][38]'

        Args:
            testpersonnummer (int): nummer på testpersonnumer fra forøget. Bruges til at åbne den rigtige fil tilhørende den rigtige person. 

        Returns:
            lines_from_logfile (list<string>): Returnerer en liste med strings svarende til hver linje i logfilen
        """
        hrmpro_path = self.path + "/Testperson_" + str(testpersonnummer) + "/SimulANT+ Logs - HRM-Pro/"
        filename = "Heart Rate Display ANT Messages.txt"
        fullpath = hrmpro_path + filename
        #print(fullpath)
        file = open(fullpath, 'r')
        lines_From_Logfile = file.readlines()
        return lines_From_Logfile

    def read_forerunner(self, testpersonnummer: int):
        forerunner_path = self.path + "/Testperson_" + str(testpersonnummer) + "/SimulANT+ Logs - forerunner/"
        filename = "Heart Rate Display ANT Messages.txt"
        fullpath = forerunner_path + filename
        file = open(fullpath, 'r')
        lines_From_Logfile = file.readlines()
        return lines_From_Logfile

    def read_empatica(self, testpersonnummer: int,datatype: str):
        """Metoden indlæser data fra den ønskede empatica logfil.

        Args:
            testpersonnummer (int): Nummeret på testpersonen
            datatype (str): Initialerne for det data der skal indlæses. Muligheder: ACC, BVP, EDA, HR, IBI, tags og TEMP

        Returns:
            lines_from_logfile (list<string>): Returnerer en liste med strings svarende til hver linje i logfilen
        """
        empatica_path = self.path + "/Testperson_" + str(testpersonnummer) + "/Empatica/" + datatype + ".csv"
        file =  open(empatica_path, mode='r', newline='')
        lines_from_logfile = list(csv.reader(file)) #file.readlines()
        file.close()
        return lines_from_logfile
    

    def read_maxrefdes_Raa_observationer(self, testpersonnummer: int, fasenummer: int):
        """Metoden læser data ind fra de rå onservationer, hvor der kan udtrækkes både RR, hr, timestamps m.v. Data indlæses som en .csv fil, og indlses inds i et dictionary

        Args:
            testpersonnummer (int): nummer på testpersonnumer fra forøget. Bruges til at åbne den rigtige fil tilhørende den rigtige person. 
            fasenummer (int): nummer på fasen, der bruges til at åbne den rigtige fil

        Returns:
            list<Dict>: Der returneres en liste med dictionaries. Der er følgende entries i dictionariet: timestmp,smpleCnt,grnCnt,led2,led3,grn2Cnt,irCnt,redCnt,accelX,accelY,accelZ,hr,rr,rrsecure,spo2. Timestamp angives som et klokkeslet uden dato 
        """
        i = 0
        faser = ["Stilhed", "Statisk", "Dynamisk"]

        while(i<3):
            maxrefdes_path = self.path + "/Testperson" + str(testpersonnummer) + "/Raaobservationer/Testperson_" + str(testpersonnummer) + "_Fase_" + str(fasenummer) + "_" + faser[i] + "_observationer.csv"
            if(os.path.exists(maxrefdes_path)):
                i = 3
                csv_file_original =  open(maxrefdes_path, mode='r')
                #print(maxrefdes_path)
                lines_as_dict = csv.DictReader(csv_file_original, delimiter = ',')
                lines_as_dict = list(lines_as_dict)
                csv_file_original.close()
                return lines_as_dict
            i+= 1
    