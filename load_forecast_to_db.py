#!/usre/bin/python3

import csv
import re
from collections import OrderedDict
from datetime import datetime
import json

import db as database

JSON_FILE_NAME = "weather.json"

REGION_NAMES = ['Моск', 'СПб-В', 'С.-Петер', 'Петр', 'Мурм', 'Волх']

# количество показателей
NUMBER_OF_INDICATORS = 6

# количество наборов показателей
NUMBER_OF_INDICATOR_SETS = 6

# сдвиг в показателях, чтобы пропускать ненужные колонки
# +2 потому что пропускаем первые два поля
SHIFT_IN_INDICATORS = NUMBER_OF_INDICATORS * NUMBER_OF_INDICATOR_SETS + 2

# даты по запросам
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
    "Москва": "06007",
    "Тверь": "06150",
    "Бологое": "05000",
    "Сонково": "05110",
    "Ржев": "06300",
    "Чудово": "04200",
    "Малая Вишера": "04160",
    "Тосно": "03130",
    "Санкт-Петербург": "03000",
    "Мга": "03020",
    "Зеленогорск": "03930",
    "Выборг": "02000",
    "Приозерск": "02300",
    "Дно": "05670",
    "Великие Луки": "06600",
    "Псков": "07050",
    "Гатчина": "03400",
    "Усть-Луга": "07450",
    "Волховстрой": "04000",
    "Тихвин": "04750",
    "Бабаево": "04640",
    "Нелазское": "04620",
    "Хвойная": "04390",
    "Лодейное Поле": "04910",
    "Петрозаводск": "01000",
    "Медвежья Гора": "01130",
    "Беломорск": "01300",
    "Кемь": "01320",
    "Костомукша": "02780",
    "Сортавала": "02370",
    "Кандалакша": "01490",
    "Апатиты": "01600",
    "Оленегорск": "01630",
    "Полярный Круг": "01433",
    "Мурманск": "01840",
    "Магнетиты": "01683"
}

OBJ_FOR_JSON = {}

REGION = 0
STATION_NAME = 1


DB_COLUMS = """ (ks, dt_load, d_vrf, n_vrf, d_rf, n_rf, d_temp,
                     n_temp, d_sh, n_sh, d_gw, n_gw, d_bi, n_bi) """

STATIONS_ENCOUNTERED = {}

DATA_TO_ADD = []


def convert_date(date_str):
    for month, day in MONTH_VALUES.items():
        date_str = date_str.replace(month, str(MONTH_VALUES[month]))
        print(date_str)


def convert_region_number(region_str):
    region_str[REGION] = REGION_NAMES.index(region_str[REGION]) + 1
    region_str[STATION_NAME] = STATION_CODES[region_str[STATION_NAME]]
    return region_str


def create_json(name):
    json_data = []
    with open(name, "w") as write_file:
        json.dump(json_data, write_file)


def add_to_json(name, data_from_parsing):
    data = json.load(open(name))
    data.append(data_from_parsing)
    with open(name, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def date_correction(date):
    date_split = date.split('/')
    return f"{date_split[1]}.{date_split[0]}.{date_split[2]}"


def get_data_from_json():
    with open('example5.csv') as file_obj:
        reader_obj = csv.reader(file_obj)
        regexp = re.compile(r'\d+/\d')
        mas_of_dates = []
        mas_with_data = []
        for row_in_csv in reader_obj:
            # print(row_in_csv)
            if (len(row_in_csv)):
                mas_of_dates_unsorted = list(
                    filter(regexp.match, row_in_csv))
                if (len(mas_of_dates_unsorted) > 2):
                    # массив дат в конце прохождения
                    mas_of_dates.extend(
                        list(OrderedDict.fromkeys(mas_of_dates_unsorted)))
                for region in REGION_NAMES:
                    if (region in row_in_csv):
                        station_name = row_in_csv[1]
                        mas_with_data.append(convert_region_number(row_in_csv))
                        station_code = row_in_csv[1]
                        row_in_csv.pop(0)
                        row_in_csv.pop(0)
                        if (station_code not in STATIONS_ENCOUNTERED):
                            STATIONS_ENCOUNTERED[station_code] = {"index": 0}
                        else:
                            STATIONS_ENCOUNTERED[station_code]['index'] += 1
                        # массив для хранения данных построчно и по датам
                        DATA_ARRAY = {}
                        # НОМЕР ПРОХОДА ЦИКЛА ПО СТАНЦИИ РАВЕН КОЛИЧЕСТВУ СОВПАДЕНИЙ ПО ЭТИМ СТАНЦИЯМ
                        N_PASS = STATIONS_ENCOUNTERED[station_code]['index']
                        # ИНДЕКС ПРОХОДА ЦИКЛА, УМНОЖАЕТСЯ НА 3 ПОТОМУ ЧТО БЕРЕМ ПО 3 ДАТЫ
                        CYCLE_PASS_INDEX = N_PASS * 3
                        for index, str_indicator in enumerate(row_in_csv):
                            if (index % 6 < 2):
                                # ИНДЕКС УМНОЖЕНИЯ (ДЛЯ ВСЕХ РАЗНЫЙ ОТ 0 ДО 2)
                                MULTIPLICATION_INDEX = 0
                            elif (index % 6 < 4):
                                MULTIPLICATION_INDEX = 1
                            elif (index % 6 < 6):
                                MULTIPLICATION_INDEX = 2
                            #  ИНДЕКС ДАТЫ
                            DATE_INDEX = MULTIPLICATION_INDEX + CYCLE_PASS_INDEX
                            curr_date = date_correction(
                                mas_of_dates[DATE_INDEX])
                            if curr_date not in DATA_ARRAY:
                                DATA_ARRAY.update(
                                    {curr_date: [station_code, curr_date]})
                            DATA_ARRAY[curr_date].append(str_indicator)
                        DATA_TO_ADD.append(DATA_ARRAY)


try:
    db = database.DB(user="postgres",
                     # пароль, который указали при установке PostgreSQL
                     password="postgres",
                     host="localhost",
                     port="5432",
                     db_name="postgres"
                     )
    get_data_from_json()
    for data_row in DATA_TO_ADD:
        for indicators in data_row:
            db.insert(f""" INSERT INTO test.forecast {DB_COLUMS}
                  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   """, tuple(data_row[indicators]))
except Exception as e:
    print('Exception', e)
