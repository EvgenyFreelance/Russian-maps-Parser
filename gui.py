from tkinter import *
from tkinter import ttk
from tkinter import filedialog

# --- Создаем контекстное меню ---
window = Tk()
window.title('Контекстное меня для настройки парсера')
# window.iconbitmap('templates/blueprint_backgroundv2.ico')
window.geometry('500x600')
window.resizable(width=False,height=False)


def select_file_json():
    file_path = filedialog.askopenfilename(
        title='выберете файл',
        filetypes = (('json файлы','*.json'),('Все файлы','*.*'))
    )

    if file_path:
        proxy.insert(END,file_path)

def select_file_txt():
    file_path = filedialog.askopenfilename(
        title='выберете файл',
        filetypes = (('Текстовые файлы','*.txt'),('Все файлы','*.*'))
    )

    if file_path:
        requests.insert(END,file_path)

def select_file_dir():
    file_path = filedialog.askdirectory(
        title='выберете файл',
    )
    if file_path:
        export_dir.insert(END,file_path)


# --- Поле указания пути к json конфигу прокси
proxy = Entry(window)
proxy.pack()

json_path_button = Button(window,text='Путь',command=select_file_json)
json_path_button.pack()

# --- Поле для Указания txt файла парсинга нужных организаций
requests = Entry(window)
requests.pack()

txt_path_button = Button(window,text='Путь',command=select_file_txt)
txt_path_button.pack()

# --- Создание выпадающего списка с вариантами сайтов карт которые может парсить парсер ---
site_choose = ttk.Combobox(window,values=['Яндекс карты','2ГИС'],state='readonly')
site_choose.current(0)
site_choose.pack()

# --- Копки старта и остановки парсера (мягкой остановки со всеми спаршенными данными) ---
start_btn = Button(window,text='Старт')
start_btn.pack()
stop_btn = Button(window,text='Стоп')
stop_btn.pack()

# --- Создание списка с экспортами и всеми прилегающими для его контроля ---
exports_scroll_bar = Scrollbar(window)
exports_scroll_bar.pack()

variables = Variable(value=['1','2','3','4','5','6','7','8','9','10'])
exports = Listbox(window,height=5,width=25,listvariable=variables,yscrollcommand=exports_scroll_bar.set)
exports.pack()

exports_scroll_bar.config(command=exports.yview)

change_btn = Button(window,text='Изменить')
change_btn.pack()
add_export_button = Button(window,text='Добавить экспорт')
add_export_button.pack()

export_dir = Entry(window)
export_dir.pack()
dir_path_button = Button(window,text='Путь',command=select_file_dir)
dir_path_button.pack()

export_name = Entry(window)
export_name.pack()

formats = ttk.Combobox(window,values=['xlsx(Excel)','csv','bd(SQLite)'],state='readonly')
formats.current(0)
formats.pack()

export_btn = Button(window,text='Экспортировать')
export_btn.pack()

window.mainloop()
