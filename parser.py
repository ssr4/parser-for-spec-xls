from __future__ import unicode_literals
import pandas as pd
import csv

try:
  with open('3.csv') as file_obj: 
    reader_obj = csv.reader(file_obj) 
    for row in reader_obj: 
        for r in row:
          print(r.encode().decode().replace(';', ' '))
except Exception as e:
  print(e)