from filereader import filereader_class
from tidskorrigering import tidskorrigering_class

class extract_empatica_class():
    def __init__(self,filereader: filereader_class, tidskorrigering: tidskorrigering_class) -> None:
        self.filereader = filereader
        self.tidkorr = tidskorrigering
        self.read_from_file = True


    def extract(self, testpersonnummer):
        if(self.read_from_file):
            data_list_of_dict = self.filereader.read_maxrefdes_Raa_observationer(testpersonnummer)

        pass

    def get_hr(self):
        pass

    def get_RR(self):
        pass

    def set_read_from_file_bool(self, value : bool):
        self.read_from_file = value