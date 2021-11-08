from filereader import*
import datetime, time

class extract_maxrefdes103_class():
    def __init__(self, filereader: filereader_class) -> None:
        self.filereader = filereader

    def extract(self, testpersonnummer: int, fasenummer: int):
        """Metoden udtrækker hr, rr og timestamps for data fra sample 1501, og fjerner dermed det første minut, svarende til at vi har fjernet dette fra forsøget

        Args:
            testpersonnummer (int): nummer på testpersonnumer fra forøget. Bruges til at åbne den rigtige fil tilhørende den rigtige person. 
            fasenummer (int): nummer på fasen, der bruges til at åbne den rigtige fil
        """
        data_list_of_dict = self.filereader.read_maxrefdes_Raa_observationer(testpersonnummer, fasenummer)

        # self.first_time = str(datetime.datetime.now().date().strftime("%d/%m/%y")) + " " + data_list_of_dict[1501]['timestmp'] #Vi tager ved index 1501 fordi det svarer til at fjerne det første minut, hvor data er utilregnelige
        # self.last_time = str(datetime.datetime.now().date().strftime("%d/%m/%y")) + " " + data_list_of_dict[len(data_list_of_dict)-1]['timestmp']
        
        self.hr_list = []
        self.rr_list = []
        self.timestamp_list = []

        i = 0
        for row in data_list_of_dict:
            if i > 1500:
                self.hr_list.append(int(round(row["hr"])))
                self.timestamp_list.append(row["timestmp"])
                if row["rr5"] != "0.0": #Hvis rr er lig 0, så vil jeg ikke gemme data
                    rr_korr = float("{:.1f}".format(0.96*float(row["rr5"]))) #korrigerer med den faktor vi fandt i excel
                    self.rr_list.append(rr_korr)
            i +=1

    def get_rr(self):
        """Metoden er en standard get-metode, der returnerer alle RR-intervaller

        Returns:
            list<float>: listen med alle RR-intervaller som floatværdier
        """
        return self.rr_list

    def get_hr(self):
        """Metoden returnerer en liste med alle hr-værdierne. Disse er optaget med fs 25 Hz

        Returns:
            List<int>: Listen med alle hr værdierne som intigers
        """
        return self.hr_list

    def get_first_timestamp(self):
        my_datetime = datetime.datetime.strptime(self.timestamp_list[0], '%d/%m/%y %H:%M:%S.%f')
        absolute_time = int((time.mktime(my_datetime.timetuple())*1000))
        return absolute_time

    def get_last_timestamp(self):
        my_datetime = datetime.datetime.strptime(self.timestamp[len(self.timestamp)-1], '%d/%m/%y %H:%M:%S.%f')
        absolute_time = int("{:.0f}".format(time.mktime(my_datetime.timetuple())*1000))
        return absolute_time

    def get_fs(self):
        """Metoden returnerer samplefrekvensen for maxrefdes103

        Returns:
            int: samplefrekvensen
        """
        return 25