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
        proxy.delete(0, END)
        proxy.insert(END,file_path)

def select_file_txt():
    file_path = filedialog.askopenfilename(
        title='выберете файл',
        filetypes = (('Текстовые файлы','*.txt'),('Все файлы','*.*'))
    )

    if file_path:
        requests.delete(0, END)
        requests.insert(END,file_path)

def select_file_dir():
    file_path = filedialog.askdirectory(
        title='выберете файл',
    )
    if file_path:
        file_path = file_path if file_path == 'D:/' or file_path == 'C:/' else file_path+'/'
        export_dir.delete(0,END)
        export_dir.insert(END,file_path)

def addPlaceholder(entry,text):
    if entry.get() == '':
        entry.insert(0,text)
        entry.config(fg='gray')
    def focus_in(event):
        if entry.get() == text:
            entry.delete(0,END)
            entry.config(fg='black')
    def focus_out(event):
        if entry.get() == '':
            entry.insert(0,text)
            entry.config(fg='gray')

    entry.bind('<FocusIn>',focus_in)
    entry.bind('<FocusOut>',focus_out)

def addExport():
    export_variables.set(
        list(export_variables.get()) + [export_dir.get()+export_name.get()+format_converter[formats.get()]]
    )

def changeExport():
    change_idx = exports.curselection()[0]
    new_exports = list(export_variables.get())
    new_exports[change_idx] = export_dir.get()+export_name.get()+format_converter[formats.get()]
    export_variables.set(new_exports)

def deleteExport():
    change_idx = exports.curselection()[0]
    new_exports = list(export_variables.get())
    del new_exports[change_idx]
    export_variables.set(new_exports)

button_style = {
    '' : '',
}

# --- Поле указания пути к json конфигу прокси
proxy = Entry(window)
proxy.pack()
addPlaceholder(proxy,'Укажите прокси сервера(json), при его отсутсвии напишите "Отсутствует"')

json_path_button = Button(window,text='Путь',command=select_file_json)
json_path_button.pack()

# --- Поле для Указания txt файла парсинга нужных организаций
requests = Entry(window)
requests.pack()
addPlaceholder(requests,'укажите .txt файл с нужными запросами')

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

export_variables = Variable(value=[])
exports = Listbox(window,height=5,width=25,listvariable=export_variables,yscrollcommand=exports_scroll_bar.set)
exports.pack()

exports_scroll_bar.config(command=exports.yview)

change_btn = Button(window,text='Изменить',command=changeExport)
change_btn.pack()
add_export_button = Button(window,text='Добавить экспорт',command=addExport)
add_export_button.pack()
del_btn = Button(window,text='Удалить экспорт',command=deleteExport)
del_btn.pack()

export_dir = Entry(window)
export_dir.pack()
export_dir.insert(0,'C:\\Users\\User\\Desktop\\outputs\\')
addPlaceholder(export_dir,'Укажите путь к папке для хранения данных')
dir_path_button = Button(window,text='Путь',command=select_file_dir)
dir_path_button.pack()

export_name = Entry(window)
export_name.insert(0,'parsing results')
addPlaceholder(export_name,'Укажите имя файлы без расширения')
export_name.pack()

formats = ttk.Combobox(window,values=['xlsx(Excel)','csv','bd(SQLite)'],state='readonly')
formats.current(0)
formats.pack()

format_converter = {
    'xlsx(Excel)' : '.xlsx',
    'csv' : '.csv',
    'bd(SQLite)' : '.bd',
}

export_btn = Button(window,text='Экспортировать')
export_btn.pack()

window.mainloop()
