from data_handler import Data_Handler
from csv_writer import CSV_Writer

# how many grades a high school must have to be added
# for example, a high school with only freshman may not be suitable
min_grade_size = 3

file_data = {
    "public": {
        "file_name": "files/Public_Universe_Survey.csv",
        "name_column": "SCH_NAME",
        "city_column": "MCITY",
        "state_column": "STATENAME",
        "level_column": "LEVEL",
        "good_levels": [
            "High",
        ],
        # lowest grade offered,
        # highest grade offered,
        # object of string grades and their integer representation
        "grade_columns": [
            "GSLO",
            "GSHI",
            {
                "KG": 0,
                "PK": -1,
                "N": 0,
                # missing
                "M": 0,
                # ungraded
                "UG": 0,
                # adult education
                "AE": 0,
            }
        ],
        "convert_state": False,
    },
    "private": {
        "file_name": "files/Private_Universe_Survey.csv",
        "name_column": "pinst",
        "city_column": "pcity",
        "state_column": "pstabb",
        "level_column": "level",
        "good_levels": [
            "2",
        ],
        "grade_columns": None,
        "convert_state": True,
    }
}

write_files = {
    "name": "files/All_High_Schools.csv"
}

if __name__ == "__main__":
    csvw = CSV_Writer(write_files["name"])

    for key in list(file_data.keys()):
        dh = Data_Handler(file_data[key]["file_name"], file_data[key]["name_column"], file_data[key]["city_column"], file_data[key]["state_column"], file_data[key]["level_column"], min_grade_size, file_data[key]["grade_columns"], file_data[key]["good_levels"], convert_state=file_data[key]["convert_state"])
        schools = dh.get_school_names()
        csvw.add_schools(schools)