#!/usre/bin/python3

import csv
import re
from collections import OrderedDict
from datetime import datetime
import json

FILE_NAME = "weather.json"

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

OBJ_FOR_JSON = {

}


def convert_date(date_str):
    for month, day in MONTH_VALUES.items():
        date_str = date_str.replace(month, str(MONTH_VALUES[month]))
        print(date_str)


def convert_number_of_region(region_str):
    region_str[0] = REGION_NAMES.index(region_str[0]) + 1
    region_str[1] = STATION_CODES[region_str[1]]
    return region_str


def create_json(name):
    json_data = []
    with open(name, "w") as write_file:
        json.dump(json_data, write_file)


def add_to_json_test(data_from_parsing):
    print(data_from_parsing)
    json_data = {
        data_from_parsing[1]: {
            "region": data_from_parsing[0],
            "header": "День",
            "data": [
                {
                    "titleOfWindGusts": "Порывы ветра, м/с",
                    "titleOfTemperature": "Температура возд, гр.С.",
                    "titleOfSnowHeight": "Высота снега,см",
                    "titleOfRainfall": "Осадки, мм/12ч.",
                    "titleOfBlackIce": "Гололед",
                }]
        }
    }
    data = json.load(open(FILE_NAME))
    data.append(json_data)
    with open(FILE_NAME, "w") as file:
        json.dump(data, file)

def add_to_json(name, data_from_parsing):
    data = json.load(open(name))
    data.append(data_from_parsing)
    with open(name, "w", encoding='utf-8') as file:
        json.dump(data, file,indent=2,ensure_ascii=False)
    

try:
    create_json(FILE_NAME)
    with open('example5.csv') as file_obj:
        reader_obj = csv.reader(file_obj)
        # regexp = re.compile(r'[A-Za-z]')
        regexp = re.compile(r'\d+/\d')
        mas_of_dates = []
        mas_with_data = []
        for row_in_csv in reader_obj:
            if (len(row_in_csv)):
                mas_of_dates_unsorted = list(
                    filter(regexp.match, row_in_csv))
                if (len(mas_of_dates_unsorted) > 2):
                    mas_of_dates.extend(
                        list(OrderedDict.fromkeys(mas_of_dates_unsorted)))
                for region in REGION_NAMES:
                    if (region in row_in_csv):
                        mas_with_data.append(
                            convert_number_of_region(row_in_csv))
                        station = row_in_csv[1]
                        # if (station in OBJ_FOR_JSON):
                        #     # удаляем код региона и станции
                        #     row_in_csv.pop(0)
                        #     row_in_csv.pop(0)
                        #     OBJ_FOR_JSON[station].append(row_in_csv)
                        if (station not in OBJ_FOR_JSON): 
                            # удаляем код региона и станции
                            row_in_csv.pop(0)
                            row_in_csv.pop(0)
                            OBJ_FOR_JSON[station] = []
                            OBJ_FOR_JSON[station].append({"header": "День",
                                                          "data": [{
                "index": 1,
                "titleOfWindGusts": "Порывы ветра, м/с",
                "titleOfTemperature": "Температура возд, гр.С.",
                "titleOfSnowHeight":"Высота снега,см",
                "titleOfRainfall": "Осадки, мм/12ч.",
                "titleOfBlackIce": "Гололед",
                "viewOsad": [],
                "indicatorsOfRainfall": [],
                "indicatorsOfTemperature": [],
                "indicatorsOfSnowHeight": [],
                "indicatorsOfGustWind": [],
                "indicatorsOfBlackIce": []
                }]})
                            OBJ_FOR_JSON[station].append({"header": "Ночь",
                                                          "data": [{
                "index": 1,
                "titleOfWindGusts": "Порывы ветра, м/с",
                "titleOfTemperature": "Температура возд, гр.С.",
                "titleOfSnowHeight":"Высота снега,см",
                "titleOfRainfall": "Осадки, мм/12ч.",
                "titleOfBlackIce": "Гололед",
                "viewOsad": [],
                "indicatorsOfRainfall": [],
                "indicatorsOfTemperature": [],
                "indicatorsOfSnowHeight": [],
                "indicatorsOfGustWind": [],
                "indicatorsOfBlackIce": []
                }]})
                            # OBJ_FOR_JSON[station].append(row_in_csv)
                        for index, str_indicator in enumerate(row_in_csv):
                            night_data_in_json = OBJ_FOR_JSON[station][0]["data"][0]
                            day_data_in_json = OBJ_FOR_JSON[station][1]["data"][0]
                            if(index < 6):
                                if(index % 2):
                                    night_data_in_json['viewOsad'].append(str_indicator)
                                else:
                                    day_data_in_json['viewOsad'].append(str_indicator)
                            elif(index < 12):
                                if(index % 2):
                                    night_data_in_json['indicatorsOfRainfall'].append(str_indicator)
                                else:
                                    day_data_in_json['indicatorsOfRainfall'].append(str_indicator)
                            elif(index < 18):
                                if(index % 2):
                                    night_data_in_json['indicatorsOfTemperature'].append(str_indicator)
                                else:
                                    day_data_in_json['indicatorsOfTemperature'].append(str_indicator)
                            elif(index < 24):
                                if(index % 2):
                                    night_data_in_json['indicatorsOfSnowHeight'].append(str_indicator)
                                else:
                                    day_data_in_json['indicatorsOfSnowHeight'].append(str_indicator)
                            elif(index < 30):
                                if(index % 2):
                                    night_data_in_json['indicatorsOfGustWind'].append(str_indicator)
                                else:
                                    day_data_in_json['indicatorsOfGustWind'].append(str_indicator)
                            elif(index < 36):
                                if(index % 2):
                                    night_data_in_json['indicatorsOfBlackIce'].append(str_indicator)
                                else:
                                    day_data_in_json['indicatorsOfBlackIce'].append(str_indicator)
    if(len(OBJ_FOR_JSON)):                            
        add_to_json(FILE_NAME, OBJ_FOR_JSON)
except Exception as e:
    print('Exception', e)
