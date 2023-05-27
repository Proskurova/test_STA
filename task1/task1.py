# Дан набор excel файлов с одинаковым набором полей.
# Необходимо объединить данные в один Excel и сохранить результат. Наименование вкладки брать из первого Excel.
# Порядок согласно полю Номер. Если значение Номер совпадает в двух и более Excel, то согласно очереди.
# Библиотеки для работы с excel выбирать на свое усмотрение.
# Т.е. есть файл Excel_1 со значением 2 в поле Номер и Excel_2 со значением 2 в поле Номер.
# Итого строки должны быть расположены подобный образом:
# - Строка 1: Excel_1 Номер=2
# - Строка 2: Excel_2 Номер=2


import pandas as pd
import os
import glob

os.chdir('excel')

data_all = []
sheet_name_all = []

xl_files = glob.glob('*.xlsx')


for xl_file in xl_files:
    xl_file_obj = pd.ExcelFile(xl_file)

    for sheet_name in xl_file_obj.sheet_names:
        sheet_name_all.append(sheet_name)
        data = pd.read_excel(xl_file_obj,
                             sheet_name=sheet_name)

        data.insert(loc=0,
                    column='file_excel',
                    value=xl_file)

        data_all.append(data)


result = pd.concat(data_all).sort_values(by=['номер'])

result.to_excel(f'{sheet_name_all[0]}.xlsx', sheet_name=f'{sheet_name_all[0]}', index=False)
