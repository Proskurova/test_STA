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
import json


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
    result_path = [[keys, value] for keys, value in result.items()]
    return result_path


def counts_weight_files(file: str) -> float:

    ''' Эта функция измеряет размер файла '''

    size_file = os.path.getsize(file) / 1024
    return size_file


def save_json(list_pdf: list, name_file: str):

    ''' Эта функция сохраняет данные в json '''

    list_file = [(re.findall(r"pack_[1-9]{1,6}.pdf", docs[0])[0]) for docs in list_pdf]
    list_number_doc = [docs[1] for docs in list_pdf]
    data = {
        "name_doc": name_file,
        "list_file_pdf": list_file,
        "list_number_doc": list_number_doc
    }
    with open(f"{name_file[:-4]}.json", "w", encoding="utf-32") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def file_separator() -> list:

    ''' Эта функция разделяет файлы для объеденения и их общий размер не должен быть больше 100 КБ '''

    path_file_size = read_pdf(collect_all_files('./pdf'))
    split_files = []
    files100 = []
    size = 20
    for index, list_pdf in enumerate(path_file_size):
        files100.append([list_pdf[1][0], list_pdf[0]])
        if size < 80 and not index == (len(path_file_size)-1):
            size += list_pdf[1][1]
        elif size > 80:
            files = files100.copy()
            split_files.append(files)
            files100.clear()
            size = 0
        else:
            split_files.append(files100)

    return split_files


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
            #Здесь регулярное выражение можно редактировать в зависимости от того, по чем ищем.
            number = re.findall(r"[нН]омер[\s\d]{1,7}", text)[0].replace(' ', '').replace("'", "")\
                .replace('Номер', '').replace('номер', '')
            size = counts_weight_files(str(pdf_path))
            data_files.update([(number, [str(pdf_path), size])])

    paths = sort_files(data_files)
    return paths


def main():

    ''' Эта функция обьеденяет файлы'''

    path_file = file_separator()
    for index, list_pdf in enumerate(path_file):
        merge = PdfMerger()
        for pdf in list_pdf:
            merge.append(pdf[0])
        name_file = f'final{index}.pdf'
        merge.write(name_file)
        save_json(list_pdf, name_file)
        merge.close()


if __name__ == '__main__':
    main()

