import datetime, time
from typing import List
class tidskorrigering_class:
    def __init__(self, absolute_time, sensor_count_at_absolute_time ) -> None:
        self.birthtime_sensor = absolute_time-sensor_count_at_absolute_time

    def hrm_pro(self, list_of_data: list, timelim_begin: int, timelim_end: int):
        list_splitted_data = []
        timecorrected_list = []
        i = -3
        for line in list_of_data:
            if(i >= 0):
                list_splitted_data.append(line.split(':'))
                list_splitted_data[i][0] = self.get_timestamp_garmin(int(list_splitted_data[i][0]))
                if(list_splitted_data[i][0] >= timelim_begin and list_splitted_data[i][0] <= timelim_end):
                    timecorrected_list.append(list_splitted_data[i]) # Jeg er lidt i tvivl om dette rent faktisk tiæføjer hele linjen
            i += 1
        return timecorrected_list

    def forerunner(self):
        pass

    def empatica(self):
        pass

    def get_timestamp_garmin(self, current_count):
        current_absolute_time = self.birthtime_sensor+current_count
        tid_forkert_dato = str(datetime.datetime.now().date().strftime("%d/%m/%y")) + " " + str(datetime.datetime.fromtimestamp(current_absolute_time/1000).strftime('%H:%M:%S.%f'))
        my_datetime = datetime.datetime.strptime(tid_forkert_dato, '%d/%m/%y %H:%M:%S.%f')
        absolute_time = int((time.mktime(my_datetime.timetuple())*1000))
        return absolute_time