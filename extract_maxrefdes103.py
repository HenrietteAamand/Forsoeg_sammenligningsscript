from IExtract import IExtract
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

        #Vi gemmer kun data fra index 1500 fordi det svarer til at fjerne det første minut, hvor data er utilregnelige, og også før interventionsperioden
        index_to_save_from = 1500
        self.first_time = str(datetime.datetime.now().date().strftime("%d/%m/%y")) + " " + data_list_of_dict[index_to_save_from]['timestmp'] 
        self.last_time = str(datetime.datetime.now().date().strftime("%d/%m/%y")) + " " + data_list_of_dict[len(data_list_of_dict)-1]['timestmp']
        
        self.hr_list = []
        self.rr_list = []
        self.timestamp_list = []

        i = 0
        for row in data_list_of_dict:
            if i >= index_to_save_from:
                self.hr_list.append(int(round(float(row["hr"]))))   #Gemmer alle hr værdier en af gangen
                self.timestamp_list.append(row["timestmp"])         # Gemmer alle timestamps en af gangen
                if row["rr"] != "0.0":                              # Gemmer kun RR-værdierne når der er beregnet en ny. 
                    rr_korr = float("{:.1f}".format(0.96*float(row["rr"]))) #korrigerer med den faktor vi fandt i excel
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
        """Metoen returnerer et timestamp, der er korrigeret til dags dato, men med det korrekte tidspunkt fra timestampet

        Returns:
            int: Timestamp returneres som unix time, altså af typen int
        """
        first_datetime = datetime.datetime.strptime(self.first_time, '%d/%m/%y %H:%M:%S.%f')
        absolute_time = int((time.mktime(first_datetime.timetuple())*1000))
        return absolute_time

    def get_last_timestamp(self):
        """Metoen returnerer et timestamp, der er korrigeret til dags dato, men med det korrekte tidspunkt

        Returns:
            int: Timestamp returneres som unix time, altså af typen int
        """
        last_datetime = datetime.datetime.strptime(self.last_time, '%d/%m/%y %H:%M:%S.%f')
        absolute_time = int("{:.0f}".format(time.mktime(last_datetime.timetuple())*1000))
        return absolute_time

    def get_fs(self):
        """Metoden returnerer samplefrekvensen for maxrefdes103

        Returns:
            int: samplefrekvensen
        """
        return 25