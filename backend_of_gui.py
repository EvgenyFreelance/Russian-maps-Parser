import multiprocessing,multiprocessing.sharedctypes as sm
from main import Parser
import time
import threading
import json
from export_data import to_excel,to_sqlite
import os

# --- Главный стартующий процесс(функция запускающая его) запускающийся в отдельном окне ---
def start_parsing(start_bool_sm,pipe,txt_path,json_path,**kwargs,):
    process = multiprocessing.Process(target=nested_process, args=(start_bool_sm,pipe,txt_path,json_path))
    process.start()

# --- Вложенная функция с инициализаций класса и 2 потоками 1 из которых парсит другой проверяет состояние переменной ---
def nested_process(bool_sm,pipe,txt_path,json_path,**kwargs):

    proxies = get_json(json_path)
    requests = get_txt(txt_path)

    parser = Parser(url='https://yandex.ru/maps', requests=requests,proxies=proxies)

    def parsing():
        parser.parse()
        data = parser.get_result()
        pipe.send(data)

    t1 = threading.Thread(target=parsing)

    def checking():
        while True:
            if not bool_sm.value:
                parsed_data = parser.get_result()
                print(parsed_data)
                pipe.send(parsed_data) # <--
                parser.stop()
                break

    t2 = threading.Thread(target=checking)
    t1.start()
    t2.start()

# Сохраняет указанные данные
def saving(data,export_pieces):
    for export in export_pieces:
        os.makedirs(export[0],exist_ok=True)

        format = export[2][1:]

        if format == 'xlsx':
            to_excel(data,path=''.join(export))
        if format == 'db':
            data = [x for x in zip(range(1, len( max( list(data.values()),key=len ) ) + 1), *data.values())]
            to_sqlite(data,path=''.join(export))


# --- Получаем данные из txt и json файлов по пути и используем как аргументы в конструкторе класса Parser
def get_txt(path):
    with open(path,mode='r',encoding='utf-8') as f:
        strings = [x.strip() for x in f.readlines()]
        return strings

def get_json(path):
    if path.lower() == 'отсутствует' or '':
        return None
    with open(path,mode='r',encoding='utf-8') as f:
        proxies = json.load(f)
        return proxies





