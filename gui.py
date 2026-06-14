from tkinter import *
from tkinter import ttk
from tkinter import filedialog

# --- Создаем контекстное меню ---
window = Tk()
window.title('Контекстное меня для настройки парсера')
# window.iconbitmap('templates/blueprint_backgroundv2.ico')
window.geometry('500x600')
window.resizable(width=False,height=False)

# --- Необходимые функции для фронтенда ---
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

def run_and_stop():
    cur_text = run_btn.cget('text')
    if cur_text == 'Старт':
        run_btn.config(text='Стоп',bg='red',fg='white',width=5)
    else:
        run_btn.config(text='Старт',bg='green',fg='white',width=5)

button_style = {
    '' : '',
}

# --- Поле указания пути к json конфигу прокси ---
proxy = Entry(window,width=38,font=16)
proxy.place(x=20,y=15)
addPlaceholder(proxy,'укажите путь к .json проки конфигурации')

json_path_button = Button(window,text='Путь',command=select_file_json,font=15)
json_path_button.place(x=380,y=10)

# --- Поле для Указания txt файла парсинга нужных организаций ---
requests = Entry(window,width=38,font=16)
requests.place(x=20,y=55)
addPlaceholder(requests,'укажите путь к .txt файлу с нужными запросами')

txt_path_button = Button(window,text='Путь',command=select_file_txt,font=16)
txt_path_button.place(x=380,y=50)

# --- Описание для выпадающего списка ---
site_select_label = Label(window,text='Выберите сайт с картами :',font=16)
site_select_label.place(x=20,y=80)

# --- Создание выпадающего списка с вариантами сайтов карт которые может парсить парсер ---
site_choose = ttk.Combobox(window,values=['Яндекс карты','2ГИС'],state='readonly',font=16)
site_choose.current(0)
site_choose.place(x=20,y=110)

# --- Описание для поля с экспортами ---
exports_label = Label(window,text='Список директорий куда будут экспортироваться данные :',font=16)
exports_label.place(x=20,y=160)

# --- Создание списка с экспортами и всеми прилегающими для его контроля ---
exports_scroll_bar = Scrollbar(window)
exports_scroll_bar.place(x=465,y=190,height=100)

export_variables = Variable(value=[])
exports = Listbox(window,height=5,width=48,listvariable=export_variables,yscrollcommand=exports_scroll_bar.set,font=16)
exports.place(x=25,y=190)

exports_scroll_bar.config(command=exports.yview)

change_btn = Button(window,text='Изменить',command=changeExport,font=14)
change_btn.place(x=25,y=300)
add_export_button = Button(window,text='Добавить экспорт',command=addExport,font=14)
add_export_button.place(x=155,y=300)
del_btn = Button(window,text='Удалить экспорт',command=deleteExport,font=14)
del_btn.place(x=344,y=300)

# --- Описание для указания пути экспорта ---
dirnpath_label = Label(window,text='Папка куда экспортировать файлы :',font=16)
dirnpath_label.place(x=20,y=360)

export_dir = Entry(window,font=16,width=38)
export_dir.place(x=20,y=400)
export_dir.insert(0,'C:\\Users\\User\\Desktop\\outputs\\')
addPlaceholder(export_dir,'Укажите путь к папке для хранения данных')
dir_path_button = Button(window,text='Путь',command=select_file_dir,font=16)
dir_path_button.place(x=380,y=395)

# --- Имя, формат ---
name_label = Label(window,text='Имя файла :',font=16)
name_label.place(x=20,y=440)

export_name = Entry(window,font=16)
export_name.insert(0,'parsing results')
addPlaceholder(export_name,'Укажите имя файлы без расширения')
export_name.place(x=150,y=440)

formats_label = Label(window,text='Формат файла :',font=16)
formats_label.place(x=20,y=480)

formats = ttk.Combobox(window,values=['.xlsx(Excel)','.csv','.bd(SQLite)'],state='readonly',font=16)
formats.current(0)
formats.place(x=150,y=480)

format_converter = {
    '.xlsx(Excel)' : '.xlsx',
    '.csv' : '.csv',
    '.bd(SQLite)' : '.bd',
}

# --- Копки старта и остановки парсера (мягкой остановки со всеми спаршенными данными) ---
run_btn = Button(window,text='Старт',command=run_and_stop,bg='green',fg='white',font='Sans 22',width=5)
run_btn.place(x=70,y=530)

# --- Кнопка экспорта ---
export_btn = Button(window,text='Сохранить',bg='blue',fg='white',font='Sans 22')
export_btn.place(x=250,y=530)

window.mainloop()
