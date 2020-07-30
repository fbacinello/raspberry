import csv
from datetime import datetime
from time import sleep

class Logger:
    def __init__(self):
        self.data_dict = {}

    def collect_data(self, data):
        '''collect data and assign to class variable'''
        self.data_dict['time'] = data
        self.data_dict['temp'] = 22
        pass

    def print_data(self):
        '''print selected data in nicely formatted string'''
        print("-"*120)
        print("{0:%Y-%m-%d, %H:%M:%S}".format(self.data_dict["time"]))
        pass

    def log_data(self):
        '''log data into csv file'''
        for file, data in self.data_dict.items():
            with open('data/' + file + ".csv", 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([data])

def main():
    logger = Logger()
    logger.collect_data(datetime.now())
    logger.log_data()
    logger.print_data()

#main()