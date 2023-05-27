# Дан набор документов в формате pdf.
# Необходимо объединить эти документы в один документ,
# при условии, что каждый итоговый объединенный документ не должен превышать 100 КБ (Килобайт).
# Порядок объединения согласно содержимому документов, а именно по значению "Номер" в документе.
# Название объединенных документов pack_1, pack_2 и т.д.
# Ориентация страниц документов должна сохраниться.
# Библиотеки для работы с pdf (и не только) выбирать на свое усмотрение.
# Сохранить результат в файле форма json, в котором будет указано наименование итогового документа
# и список документов, содержащиеся в итоговом.

from PyPDF2 import PdfReader, PdfMerger
from pathlib import Path
import os
import re


def collect_all_files(parent_folder: str) -> list:

    ''' Эта функция собирает все файлы pdf из папки pdf, которые нужно объединить и
    выдает список с названием файлов '''

    target_files = []
    for path, subdir, files in os.walk(parent_folder):
        for name in files:
            target_files.append(os.path.join(path, name))
        return target_files


def sort_files(number_file: dict) -> list:

    ''' Эта функция собирает сортирует поочередность соединяемых файлов '''

    keys = list(number_file.keys())
    keys.sort()
    result = {}
    for i in keys:
        result[i] = number_file[i]
    result_path = [value for value in result.values()]
    return result_path


def read_pdf(name_pdfs: list) -> list:

    ''' Эта функция читает файлы и смотрит номер документа '''

    data_files = {}
    for name_pdf in name_pdfs:
        pdf_path = (
                Path().absolute()
                / f'{name_pdf}'
        )
        pdf = PdfReader(str(pdf_path))

        for page in pdf.pages:
            text = page.extract_text()
            #Определяем номер документа
            #Здесь регулярное выражение можно редактировать в зависимости от задачи
            number = str(re.findall(r"[нН]омер[\s\d]{1,7}", text)).replace(' ', '').replace("'", "")\
                .replace('Номер', '').replace('номер', '').replace('[', '').replace(']', '')
            data_files.update([(number, str(pdf_path))])

    paths = sort_files(data_files)
    return paths


def main():

    ''' Эта функция обьеденяет файлы '''

    collected_files = read_pdf(collect_all_files('./pdf'))
    merge = PdfMerger()

    for pdf in collected_files:
        merge.append(pdf)

    merge.write('./final.pdf')
    merge.close()


if __name__ == '__main__':
    main()


