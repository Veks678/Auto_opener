from tkinter import filedialog as fd
from tkinter import *
import time
import os
import re

from pathlib import Path
import pyperclip

from .internal_realization import Delete_content, Group_window,\
                                  Content_buttons, Opening_and_closing_content
                                  

class Command_logic(
    Delete_content, Group_window, Content_buttons,
    Opening_and_closing_content
):
    def __init__(self): 
        self.url_template = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'\
                           +'[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    # Обновление стартового сообщения
    def update_start_message(self):
        self.paths_input.delete('0.0', END)
        self.paths_input.config(fg='gray65')
        self.paths_input.insert('0.0', self.start_text['paths_input'])
    
    # Добавление путей
    def adding_path(self, pressing=True):
        if len(self.info_buttons['path']) == 26:
            return self.update_start_message()

        if pressing == True:
            input_get = self.paths_input.get('1.0','end-1c').strip('"')

            if len(re.findall(self.url_template, input_get)) > 0:
                self.info_content.append({'path': input_get, 'type': 'url'})
                self.creating_path_buttons(input_get)

            elif Path(input_get).exists() and len(input_get) != 0:
                if os.path.isfile(input_get):
                    self.info_content.append({'path': input_get, 'type': 'file'})
                    self.creating_path_buttons(input_get)
                else:
                    self.info_content.append({'path': input_get, 'type': 'dir'})
                    self.creating_path_buttons(input_get)
            else:
                self.paths_input.delete('0.0', END)
                text = fd.askopenfilename().replace('/', '\\')
                
                if len(text) != 0:
                    self.paths_input.insert('0.0', text)
                    return self.adding_path()
                return
                    
            self.update_start_message()

        self.resizing_program()
        
    # Открытие путей
    def open_path(self, widget=False):
        if widget != False:
            index = [
                i for i, elem in enumerate(self.info_buttons['path'])
                if elem['path_button'] == widget
            ][0]

            return self.path_opening_realization(self.info_content[index])

        elif widget == False:
            {
                (self.path_opening_realization(path_dict), time.sleep(0.5))
                for path_dict in self.info_content
            }            

    # Закрытие путей
    def close_path(self):
        {
            self.closing_running_process(
                self.get_name_from_path(elem['path'])
            )
            for elem in self.info_content if elem['type'] == 'file' and 
            self.search_running_processes(elem['path']) == True
        }

    # Создание окна ввода имени группы
    def run_name_window(self):
        self.windows['group'] = self.windows_builder(
            Toplevel(), self.windows_param['group']
        )
        self.creating_name_window_widgets()

    # Сохранение контента
    def save_content(self, exit=False):
        text_content = [
            f'path>{elem["path"]},type>{elem["type"]}'
            for elem in self.info_content
        ]
        with open(self.retention_dir, 'w') as file_path:
            file_path.write('\n'.join(text_content))

        if exit == True:
            self.master.destroy()

    # Работа с буфером обмена
    def work_with_clipboard(self, key):
        if self.paths_input.get('0.0', END).rstrip('\n') == \
           self.start_text['paths_input']:
            self.paths_input.delete('0.0', END)
            self.paths_input.config(fg='white')

        if key.char == '\x16':
            self.paths_input.insert('0.0', pyperclip.paste())
