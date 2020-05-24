import csv
import os
from state_abbrevs import us_state_abbrev

class Data_Handler:
    file_types = ("csv")

    def __init__(self, file_name, school_name_column, school_city_column, school_state_column, school_level_column, min_grade_size, grade_columns, good_levels, convert_state = False):
        if not file_name.endswith(self.file_types):
            raise ValueError(f"File must be of types: {self.file_types}")
        
        if not self.file_exists(file_name):
            raise ValueError("That file does not exist")

        self.fn = file_name

        self.name = school_name_column
        self.city = school_city_column
        self.state = school_state_column
        self.level = school_level_column
        self.min_grade_size = min_grade_size
        self.grade_columns = grade_columns
        self.good_levels = good_levels
        self.convert_state = convert_state

    
    def file_exists(self, file_name):
        return os.path.isfile(file_name)


    def get_school_names(self):
        school_data = []

        with open(self.fn, errors='ignore') as f:
            reader = csv.reader(f, delimiter=',')
            begin = True

            columns = [
                self.name,
                self.city,
                self.state,
                self.level,
            ]

            # if there is no grade limiting set, do not add to column list
            if self.grade_columns != None:
                columns.extend([self.grade_columns[0],
                                self.grade_columns[1],])

            column_indexes = []

            for row in reader:
                if begin:
                    # if column name not found in sheet, raise error
                    for x in range(len(columns)):
                        col = columns[x]

                        index = row.index(col)
                        
                        # index not found
                        if index == -1:
                            raise ValueError(f"{col} in spreadsheet not valid")
                            break
                            
                        # store index of column name
                        column_indexes.append(index)

                    begin = False
                else:
                    min_grade, max_grade = None, None

                    if self.grade_columns != None:
                        min_grade = self.convert_grade(row[column_indexes[4]])
                        max_grade = self.convert_grade(row[column_indexes[5]])

                    if self.check_school(row[column_indexes[3]], min_grade, max_grade):
                        school_name = row[column_indexes[0]]
                        school_city = row[column_indexes[1]]
                        if self.convert_state:
                            school_state = self.convert_to_full_state(row[column_indexes[2]])
                        else:
                            school_state = row[column_indexes[2]]

                        school_data.append([school_name, school_city, school_state])

        return school_data

    # checks if school is valid:
    #   - valid level
    #   - valid grade range
    def check_school(self, level, min_grade = None, max_grade = None):
        if level not in self.good_levels:
            return False
        if min_grade != None:
            min_grade = self.convert_grade(min_grade)
            max_grade = self.convert_grade(max_grade)

            if max_grade - min_grade < self.min_grade_size:
                return False

        return True


    # converts grade into integer equivalent
    def convert_grade(self, grade):
        # checks if grade has string version in object
        if grade in list(self.grade_columns[2].keys()):
            grade = self.grade_columns[2][grade]
        else:
            try:
                grade = int(grade)
            except ValueError:
                raise ValueError(f"{grade} cannot be converted to integer")
        return grade


    def get_school_city(self, row):
        city_index = 1

    
    # converts abbreviation of state to full name
    def convert_to_full_state(self, abb):
        return us_state_abbrev[abb]