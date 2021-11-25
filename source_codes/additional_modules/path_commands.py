from tkinter import *
from tkinter import filedialog as fd

from psutil import process_iter
from pathlib import Path
import win32com.client
import webbrowser
import time
import os
import re

class internal_realization():
    def __init__(self, GUI, main_window):
        self.GUI, self.main_window = GUI, main_window

    # Удаление ярлыков
    def removing_shortcuts(self, field_get):
        with os.scandir(self.GUI.shortcuts_path) as direct:
            {os.remove(self.GUI.INFO_PROGRAMM[field_get]) for file in direct\
             if file.name == field_get}
        del self.GUI.INFO_PROGRAMM[field_get]

    # Удаление следов путей
    def removing_traces_path(self, widget, index):
        del self.GUI.INFO_PATH[widget]
        self.GUI.TEXT_FIELD['listbox'].delete(index)

    # Смещение кнопок удаления
    def offset_delete_buttons(self, index):
        for i, elem in enumerate(self.GUI.INFO_PATH):
            if i > index - 1:
                self.GUI.INFO_PATH[elem] -= 20
                elem.place_configure(y=self.GUI.INFO_PATH[elem])

    # Обновление стартового сообщения
    def update_start_message(self):
        self.GUI.TEXT_FIELD['Text'].delete('0.0', END)
        self.GUI.TEXT_FIELD['Text'].insert('0.0', self.GUI.start_text['path'])

    # Создание и перемещение ярлыков
    def create_and_move_shortcuts(self, text_get):
        name = ''.join(text_get.split('\\')[-1:])[0:-4].rstrip('.')
        shortcut = win32com.client.Dispatch("WScript.Shell")
        shortcut = shortcut.CreateShortCut(\
            (f'{self.GUI.shortcuts_path}\\{name}.lnk')\
        )
        shortcut.Targetpath = text_get
        shortcut.save()

        self.GUI.INFO_PROGRAMM[f'{name}.lnk'] = text_get
        self.GUI.TEXT_FIELD['listbox'].insert(END, f'{name}.lnk')

    # Создание кнопок удаления
    def create_delete_buttons(self, x, y):
        y = (20 * (len(self.GUI.INFO_PATH) + 1)) + (y - 20)
        clear = self.GUI.widgets_constructor(self.main_window, Button,\
                                             ('clear','clear_p'), "gray25", "white")
        clear.place(x=x, y=y, height=20, width=20)
        return y, clear

    # Поиск запущенного процесса
    def search_running_processes(self, elem):
        programm_name = ''.join(self.GUI.INFO_PROGRAMM[elem].split('\\')[-1:])[0:-3]
        proc_name = [proc.info['name'] for proc in process_iter(['name'])\
                     if proc.info['name'] != None and\
                     proc.info['name'][0:-3] == programm_name]
        if len(proc_name) != 0:
            return proc_name
        return None

    # Закрытие запущенного процесса
    def closing_running_process(self, proc_name):
        if proc_name != None:
            {proc.kill() for proc in process_iter(['name'])\
             if proc.info['name'] == proc_name[0]}


class Path_commands_logic(internal_realization):
    def __init__(self, GUI, main_window):
        internal_realization.__init__(self, GUI, main_window)
        self.GUI, self.main_window = GUI, main_window
        self.url_template = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    # Удаление путей
    def delete_path(self, widget):
        index = list(self.GUI.INFO_PATH.keys()).index(widget)
        field_get = self.GUI.TEXT_FIELD['listbox'].get(index)

        if field_get in self.GUI.INFO_PROGRAMM:
            self.removing_shortcuts(field_get)

        self.removing_traces_path(widget, index)
        widget.destroy()
        self.offset_delete_buttons(index)

    # Добавление путей
    def adding_path(self, pressing=True):
        text_get = self.GUI.TEXT_FIELD['Text'].get('1.0', 'end-1c').strip('"')
        name = ''.join(text_get.split('\\')[-1:])[0:-4].rstrip('.')
        if {True for text in self.GUI.TEXT_FIELD['listbox'].get(0, END)\
            if text.rstrip('\n') == f'{name}.lnk'} == {True}:
            return self.update_start_message()

        if (20 * len(self.GUI.INFO_PATH) + 28) == 268:
            self.update_start_message()
            return

        elif pressing == True:
            if len(re.findall(self.url_template, text_get)) > 0:
                self.GUI.TEXT_FIELD['listbox'].insert(END, text_get)

            elif Path(text_get).exists() and len(text_get) != 0:
                if os.path.isfile(text_get):
                    self.create_and_move_shortcuts(text_get)
                else:
                    self.GUI.TEXT_FIELD['listbox'].insert(END, text_get)
            else:
                self.GUI.TEXT_FIELD['Text'].delete('0.0', END)
                text = fd.askopenfilename().replace('/', '\\')
                if len(text) == 0:
                    return
                else:
                    self.GUI.TEXT_FIELD['Text'].insert('0.0', text)
                    return self.adding_path()

            self.update_start_message()

        y, clear = self.create_delete_buttons(369, 48)
        clear.config(command=lambda: self.delete_path(clear))
        self.GUI.INFO_PATH[clear] = y

    # Открытие путей
    def Open(self):
        for elem in list(self.GUI.TEXT_FIELD['listbox'].get(0, END)):
            if len(re.findall(self.url_template, elem)) > 0:
                webbrowser.open_new_tab(elem)

            elif os.path.isdir(elem):
                os.startfile(os.path.realpath(elem))
            else:
                if self.search_running_processes(elem) == None:
                    os.startfile(self.GUI.INFO_PROGRAMM[elem])

            time.sleep(0.5)

    # Закрытие путей
    def close(self):
        for elem in self.GUI.INFO_PROGRAMM:
            self.closing_running_process(self.search_running_processes(elem))
            time.sleep(0.5)

