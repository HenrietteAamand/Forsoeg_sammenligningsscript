import csv, os.path, json

class filereader_class:
    def __init__(self, path, filename = "") -> None:
        self.path = path
        self.filename = filename
        
    def read_HRMpro(self, testpersonnummer: int):
        """Metoden læser data fra den logfil, der genereres når man bruger SimulANT+ til at læse data der sendes fra en Garmin(R) ANT+ sensor. 
           Der indlæses en liste, hvor hver plads i listen indeholder en linje fra logfilen på formen '81809171 : Rx: [04][00][88][6B][EC][6F][A3][39]', svarende til datapage 4

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
        """Metoden læser data fra den logfil, der genereres når man bruger SimulANT+ til at læse data der sendes fra en Garmin(R) ANT+ sensor. 
           Der indlæses en liste, hvor hver plads i listen indeholder en linjje fra logfilen på formen '81722734 : Rx: [00][FF][FF][FF][86][02][9F][38]'

        Args:
            testpersonnummer (int): nummer på testpersonnumer fra forøget. Bruges til at åbne den rigtige fil tilhørende den rigtige person. 

        Returns:
            lines_from_logfile (list<string>): Returnerer en liste med strings svarende til hver linje i logfilen
        """
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
        faser = ["Baseline","Stilhed", "Statisk", "Dynamisk"]

        for i in range(len(faser)):
            #maxrefdes_path = self.path + "/Testperson" + str(testpersonnummer) + "/Raaobservationer/Testperson_" + str(testpersonnummer) + "_Fase_" + str(fasenummer) + "_" + faser[i] + "_observationer.csv"
            maxrefdes_path = self.path + "/Raaobservationer/Testperson_" + str(testpersonnummer) + "_Fase_" + str(fasenummer) + "_" + faser[i] + "_observationer.csv"
            if(os.path.exists(maxrefdes_path)):
                i = 3
                csv_file_original =  open(maxrefdes_path, mode='r')
                #print(maxrefdes_path)
                lines_as_dict = csv.DictReader(csv_file_original, delimiter = ',')
                lines_as_dict = list(lines_as_dict)
                csv_file_original.close()
                return lines_as_dict


    def read_sensorcount(self):
        path = self.path + "/sensorcount.csv"
        csv_file_original =  open(path, mode='r')
        lines_as_dict = csv.DictReader(csv_file_original, delimiter = ';')
        lines_as_dict = list(lines_as_dict)
        csv_file_original.close()
        return lines_as_dict

    # def save_hr_data(self, data):
    #     output_file = open('C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/resluts_example.csv', 'w+', newline='')
    #     keys = data[1].keys()
    #     dict_writer = csv.DictWriter(output_file, keys)
    #     dict_writer.writeheader()
    #     i=1
    #     while i <= len(data):
    #         dict_writer.writerows(data[i])
            

    def save_hr_data(self, data):
        full_path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/resluts_example.csv'
        data_file = open(full_path, 'w+', newline='') #w+ fordi så laves filen hvis ikke den allerede eksisterer
        csv_writer = csv.writer(data_file, delimiter=';')
        string = json.dumps(data[1], default=lambda o: o.__dict__, sort_keys=False, indent=4)
        json_obj = json.loads(string)
        header = json_obj.keys()
        csv_writer.writerow(header)
        data_file.close()
        data_file = open(full_path, 'a', newline='')
        csv_writer = csv.writer(data_file, delimiter=';')
        
        # Writing data of CSV file
        i=1
        while i <= len(data):
            string = json.dumps(data[i], default=lambda o: o.__dict__, sort_keys=False, indent=4)
            json_obj = json.loads(string)
            csv_writer.writerow(json_obj.values())
            i+=1
        data_file.close()
        
    def read_hr_data(self):
        full_path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/resluts_example.csv'
        csv_file_original =  open(full_path, mode='r')
        lines_as_dict = csv.DictReader(csv_file_original, delimiter = ';')
        i = 1
        dict_data = {}
        for line in lines_as_dict:
            dict_data[i] = line
            i+=1
        csv_file_original.close()
        i = 1
        return_dict = {}
        for key in dict_data:
            for dataset_key in  dict_data[key]:
                string = dict_data[key][dataset_key]
                dict_data[key][dataset_key] = json.loads(string)
            i+=1
        return dict_data

    def save_results(self, list_to_save: list):
        keys = list_to_save[0].keys()
        output_file = open('C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Data/resluts.csv', 'w+', newline='')
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_to_save)

    def read_fase_to_intervention_file(self):
        full_path = 'C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Data/testperson_fase_intervention.csv'
        csv_file_original =  open(full_path, mode='r')
        lines_as_dict = csv.DictReader(csv_file_original, delimiter = ';')
        lines_as_list = list(lines_as_dict)
        csv_file_original.close()
        return lines_as_list


        

    