#!/usre/bin/python3

import csv
region_names = ['Моск', 'С.-Петер', 'СПБ-В', 'Волх', 'Петр', 'Мурм']
NUMBER_OF_INDICATORS = 6
NUMBER_OF_FIELDS_IN_INDICATORS = 6
# +2 потому что пропускаем первые два поля
SHIFT_IN_INDICATORS = NUMBER_OF_INDICATORS * NUMBER_OF_FIELDS_IN_INDICATORS + 2
try:
  with open('example4.csv') as file_obj: 
    reader_obj = csv.reader(file_obj) 
    for row_in_csv in reader_obj: 
        row_in_csv = [row for index, row in enumerate(row_in_csv) if row and index >SHIFT_IN_INDICATORS]
        if(len(row_in_csv)):
          for region in region_names:
            # print(row_in_csv, '\n')
            if(region in row_in_csv):
              print(row_in_csv, '\n')
            
        # for r in row:
        #   row_in_csv = r.encode().decode().replace(';', ' ')
        #   if row_in_csv:
        #     # print("\n" in row_in_csv, row_in_csv == "")
        #     print(row_in_csv)
except Exception as e:
  print(e)