import csv
from datetime import datetime
import os


class Logger:
    def __init__(self):
        self.data_dict = {}

    def collect_data(self, source, data):
        """collect data and assign to class variable"""
        self.data_dict[source] = data

    def print_data(self, source):
        """print selected data in nicely formatted string"""
        print("-" * 120)
        print("{0:%Y-%m-%d, %H:%M:%S}".format(self.data_dict[source]))

    def log_data(self):
        """log data into csv file"""

        for file, data in self.data_dict.items():
            path = "data/" + datetime.now().strftime('%Y_%m_%d') + file + ".csv"
            self.file_exist(file, path)
            with open(path, 'a+', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data.keys())
                writer.writerow(data)

    def file_exist(self, source, path):
        if not os.path.isfile(path):
            with open(path, 'a+', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.data_dict[source].keys())
                writer.writeheader()