from tkinter import *

from psutil import process_iter
from PIL import ImageTk
import pyperclip
import os

from .path_commands import Path_commands_logic
from .group_commands import Group_commands_logic


class internal_realization():
    # Применение изображений нажатия
    def applying_click_images(self, widget, key):
        widget.config(image=self.img[key[0]])
        if len(key) > 1:
            widget.bind('<ButtonPress-1>', lambda x: widget.config(\
                image = self.img[key[1]]\
            ))
            widget.bind('<ButtonRelease-1>', lambda x: widget.config(\
                image = self.img[key[0]]\
            ))

    # Cоздание словаря виджетов
    def creating_dict_widgets(self, widget, key):
        widget["border"], self.TEXT_FIELD[key] = "0", widget

    # Cоздание сохраненных виджетов
    def creating_saved_widgets(self, group_dir, content):
        {self.COMMANDS_DICT['group'].creating_group_widgets(folder.name)\
         for folder in group_dir}

        {(self.TEXT_FIELD['listbox'].insert(index, elem.rstrip('\n')),\
          self.COMMANDS_DICT['path'].adding_path(False))\
          for index, elem in enumerate(content)}

    # Получение информации о контенте
    def getting_content_info(self, file_path, main_dir):
        try:
            number_buttons = int(file_path.readlines()[0][13:])
            file_path.seek(0)
            content = file_path.readlines()[1:]
        except IndexError:
            content, number_buttons = [], 0

        for file in main_dir:
            if f'{file.name}\n' not in content:
                number_buttons += 1
                content.append(f'{file.name}\n')
            self.INFO_PROGRAMM[file.name] = f'{self.shortcuts_path}\\{file.name}'

        return content, number_buttons

    # Открытие стартового контента
    def opening_starter_content(self):
        with open(self.save_path,"r") as file_path,\
             os.scandir(self.shortcuts_path) as main_dir,\
             os.scandir(self.group_path) as group_dir:

            content, number_buttons = self.getting_content_info(file_path, main_dir)
            self.creating_saved_widgets(group_dir, content)

    # Статус процесса
    def process_status(self, process_name):
        return len([proc.info['name'] for proc in process_iter(['name'])\
                    if proc.info['name'] == process_name])

    # Очистка данных
    def data_cleansing(self):
        {data.clear()
         for data in (self.TEXT_FIELD, self.INFO_PATH, self.INFO_PROGRAMM, self.INFO_GROUP)}

    # Cохранение контента
    def preservation_content(self):
        number_buttons, content = 0, ''
        for num in range(len(self.TEXT_FIELD['listbox'].get(0, END))):
            if '.lnk' not in self.TEXT_FIELD['listbox'].get(num):
                number_buttons += 1
                text_listbox = self.TEXT_FIELD['listbox'].get(num)
                content += f'{text_listbox}\n'

        with open(self.save_path, 'w') as file_path:
            file_path.write(f'buttons_len: {number_buttons}\n{content}')

    # Работа с буфером обмена
    def work_with_the_clipboard(self, key):
        if self.TEXT_FIELD['Text'].get('0.0', END).rstrip('\n') == \
           self.start_text['path']:
            self.TEXT_FIELD['Text'].delete('0.0', END)
            self.TEXT_FIELD['Text'].config(fg='white')

        if key.char == '\x16':
            self.TEXT_FIELD['Text'].insert('0.0', pyperclip.paste())


class Constructor_gui(Frame, internal_realization):
    TEXT_FIELD, INFO_PATH, INFO_PROGRAMM, INFO_GROUP = {}, {}, {}, {}
    COMMANDS_DICT = {'path': None, 'group': None}

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.save_path = f'{os.getcwd()}\\source_codes\\save\\save_path.txt'
        self.save_open = f'{os.getcwd()}\\source_codes\\save\\save_open.txt'
        self.shortcuts_path = f'{os.getcwd()}\\source_codes\\shortcuts'
        self.group_path = f'{os.getcwd()}\\source_codes\\save\\group'
        self.img_path = f'{os.getcwd()}\\source_codes\\image\\'

        self.start_text = {'path': 'Введите путь или url-адресс', 'group': 'Имя группы'}

        self.img = {'add': ImageTk.PhotoImage(file=f"{self.img_path}adding.png"),\
                    'add_p': ImageTk.PhotoImage(file=f"{self.img_path}adding_push.png"),\
                    'clear': ImageTk.PhotoImage(file=f"{self.img_path}clear.png"),\
                    'clear_p': ImageTk.PhotoImage(file=f"{self.img_path}clear_push.png"),\
                    'save': ImageTk.PhotoImage(file=f"{self.img_path}save.png"),\
                    'save_p': ImageTk.PhotoImage(file=f"{self.img_path}save_push.png"),\
                    'open': ImageTk.PhotoImage(file=f"{self.img_path}open.png"),\
                    'close': ImageTk.PhotoImage(file=f"{self.img_path}close.png"),\
                    'group': ImageTk.PhotoImage(file=f"{self.img_path}create_group.png"),\
                    'add_group': ImageTk.PhotoImage(file=f"{self.img_path}adding_group.png"),\
                    'cancel': ImageTk.PhotoImage(file=f"{self.img_path}cancel.png")}

    def windows_constructor(self, title, geometry, resizable, bg, window='main'):
        if window == 'main':
            window = self.master

        window.attributes("-topmost", True)
        window.title(title)
        window.geometry(f'{geometry[0]}x{geometry[1]}+{geometry[2]}+{geometry[3]}')
        window.resizable(resizable[0], resizable[1])
        window["bg"] = bg

        return window

    def widgets_constructor(self, window, TYPE, key, BG, FG, FONT=('Arial', '10', 'bold')):
        widget = TYPE(window, bg=BG, fg=FG, font=f'{FONT[0]} {FONT[1]} {FONT[2]}')

        if TYPE != Button and key != False:
            self.creating_dict_widgets(widget, key)
        elif key != False:
            self.applying_click_images(widget, key)

        widget.pack_propagate(False)
        widget.pack(expand=True, fill=BOTH)
        return widget

    def widgets_creating(self):
        #---------------------------------------------------------------------
        listbox = self.widgets_constructor(self.master, Listbox, 'listbox',\
                                           "gray8", "white", ('Arial','10',''))
        listbox.place(x=2, y=46, height=243, width=388)
        #---------------------------------------------------------------------
        text = self.widgets_constructor(self.master, Text, 'Text', "gray8",\
                                        "gray65", ('Arial','10',''))
        text.place(x=27, y=291, height=23, width=363)
        text.insert('0.0', self.start_text['path'])
        text.bind("<Key>", lambda key: self.work_with_the_clipboard(key))
        #---------------------------------------------------------------------
        save = self.widgets_constructor(self.master, Button,
                                        ('save', 'save_p'), "gray30", "white")
        save.config(command=lambda: self.save_content())
        save.place(x=350, y=3, height=40, width=40)
        #---------------------------------------------------------------------
        add = self.widgets_constructor(self.master, Button, ('add', 'add_p'),\
                                       "gray35", "white")
        add.config(command=lambda: self.COMMANDS_DICT['path'].adding_path())
        add.place(x=2, y=291, height=23, width=23)
        #---------------------------------------------------------------------
        #VoxReguar
        Open = self.widgets_constructor(self.master, Button, ['open'],\
                                        "gray30","white")
        Open.config(command=lambda: self.COMMANDS_DICT['path'].Open())
        Open.place(x=2, y=3, height=40, width=172)
        #---------------------------------------------------------------------
        close = self.widgets_constructor(self.master, Button, ['close'],\
                                         "gray30", "white")
        close.config(command=lambda: self.COMMANDS_DICT['path'].close())
        close.place(x=176, y=3, height=40, width=172)
        #---------------------------------------------------------------------
        group = self.widgets_constructor(self.master, Button, ['group'],\
                                         "gray30","white")
        group.config(command=lambda: self.COMMANDS_DICT['group'].run_name_window())
        group.place(x=393, y=3, height=40, width=148)
        #---------------------------------------------------------------------
        group_bg = self.widgets_constructor(self.master, Label, False,
                                            "gray10", "black",
                                            ('Arial', '10', ''))
        group_bg.place(x=393, y=47, height=267, width=148)
        #---------------------------------------------------------------------
        self.starter_content()

    def save_content(self, exit=False):
        self.preservation_content()
        self.data_cleansing()

        x, y = self.master.winfo_x(), self.master.winfo_y()
        self.master.destroy()
        if exit == False:
            self.restart(x, y)

    def starter_content(self):
        self.opening_starter_content()

    def restart(self, x, y):
        run_gui(x, y)


def run_gui(x, y):
    GUI = Constructor_gui(Tk())
    main_window = GUI.windows_constructor('', [543, 317, x, y], [False, False],
                                          "wheat4")

    # path_commands, group_commands
    GUI.COMMANDS_DICT['path'] = Path_commands_logic(GUI, main_window)
    GUI.COMMANDS_DICT['group'] = Group_commands_logic(GUI, main_window)
    GUI.widgets_creating()

    main_window.protocol("WM_DELETE_WINDOW", lambda: GUI.save_content(True))
    main_window.iconbitmap(f'{os.getcwd()}\\source_codes\\image\\Auto-opener_icon.ico')
    GUI.mainloop()
