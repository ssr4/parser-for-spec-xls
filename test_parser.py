#!/usre/bin/python3

import csv
import re
from collections import OrderedDict
from datetime import datetime


REGION_NAMES = ['Моск', 'СПБ-В', 'С.-Петер', 'Петр', 'Мурм', 'Волх']

NUMBER_OF_INDICATORS = 6
NUMBER_OF_FIELDS_IN_INDICATORS = 6
# +2 потому что пропускаем первые два поля
SHIFT_IN_INDICATORS = NUMBER_OF_INDICATORS * NUMBER_OF_FIELDS_IN_INDICATORS + 2
DATES_OF_REQUEST = []
MONTH_VALUES = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
}

# костыль
STATION_CODES = {

}


def convert_date(date_str):
    for month, day in MONTH_VALUES.items():
        date_str = date_str.replace(month, str(MONTH_VALUES[month]))
        print(date_str)


def convert_number_of_region(region_str):
    region_str[0] = REGION_NAMES.index(region_str[0]) + 1
    # for month, day in MONTH_VALUES.items():
    #     date_str = date_str.replace(month, str(MONTH_VALUES[month]))
    #     print(date_str)


try:
    with open('example5.csv') as file_obj:
        reader_obj = csv.reader(file_obj)
        # regexp = re.compile(r'[A-Za-z]')
        regexp = re.compile(r'\d+/\d')
        mas_of_dates = []
        for row_in_csv in reader_obj:
            # row_in_csv = [row for index, row in enumerate(row_in_csv) if (
            #     row and index > SHIFT_IN_INDICATORS) or (index < SHIFT_IN_INDICATORS and row)]
            if (len(row_in_csv)):
                mas_of_dates_unsorted = list(
                    filter(regexp.match, row_in_csv))
                if (len(mas_of_dates_unsorted) > 2):
                    mas_of_dates.extend(
                        list(OrderedDict.fromkeys(mas_of_dates_unsorted)))
                for region in REGION_NAMES:
                    if (region in row_in_csv):
                        convert_number_of_region(row_in_csv)
                        print(row_in_csv)

     # if (len(new_row_in_csv_with_date)):
                #     if (len(DATES_OF_REQUEST) == 0):
                #         for date in new_row_in_csv_with_date:
                #             DATES_OF_REQUEST.append(
                #                 date)
    # for date_str in DATES_OF_REQUEST:
    #     # Day + Month
    #     date = re.findall(r'\d+.[A-Za-z]+', date_str)
    #     year_search = re.findall(r'\d{4}', date_str)
    #     if (len(year_search)):
    #         year = year_search.pop()
    #         print(year)
    #     convert_date(date.pop())
    print(mas_of_dates)
except Exception as e:
    print(e)

 # for r in row:
    #   row_in_csv = r.encode().decode().replace(';', ' ')
    #   if row_in_csv:
    #     # print("\n" in row_in_csv, row_in_csv == "")
    #     print(row_in_csv)
