class filereader_class:
    def __init__(self, path, filename) -> None:
        self.path = path
        self.filename = filename
        pass    
        
    def read_HRMpro(self, testpersonnummer):
        hrmpro_path = self.path + "/Testperson_" + str(testpersonnummer) + "/SimulANT+ Logs - HRM-Pro/"
        filename = "Heart Rate Display ANT Messages.txt"
        fullpath = hrmpro_path + filename
        
        file = open(fullpath, 'r')
        lines_From_Logfile = file.readlines()
        return lines_From_Logfile

    def read_forerunner(self, testpersonnummer: int):
        forerunner_path = self.path + "/Testperson_" + str(testpersonnummer) + "/SimulANT+ Logs - HRM-Pro/"
        filename = "Heart Rate Display ANT Messages.txt"
        fullpath = forerunner_path + filename
        file = open(fullpath, 'r')
        lines_From_Logfile = file.readlines()
        return lines_From_Logfile

    def read_empatica(self, timestamp_begin, timestamp_end):
        pass
    
    def read_maxrefdes(self):
        pass