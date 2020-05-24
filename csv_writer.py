import os
import csv

class CSV_Writer:
    file_types = ("csv")

    def __init__(self, file_name):
        if not file_name.endswith(self.file_types):
            raise ValueError(f"File must be of types: {self.file_types}")

        self.fn = file_name

        # sets column names
        with open(self.fn, mode="w") as wf:
            file_writer = csv.writer(wf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(["Name", "City", "State"])

    
    def add_school(self, school_name, school_city, school_state):
        # file mode is append to avoid deletion when adding multiple schools
        with open(self.fn, mode="a") as wf:
            file_writer = csv.writer(wf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow([school_name, school_city, school_state])

    
    def add_schools(self, school_arr):
        with open(self.fn, mode="a") as wf:
            file_writer = csv.writer(wf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerows(school_arr)