from tkinter import filedialog as fd
from tkinter import *
import time
import os
import re

from pathlib import Path
from .internal_realization import Path_internal_realization,\
                                  Group_internal_realization

class Path_logic(Path_internal_realization):
    def __init__(self): 
        self.url_template = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'\
                           +'[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

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


class Group_logic(Group_internal_realization):
    # Cоздание виджетов окна ввода имени
    def creating_name_window_widgets(self):
        #---------------------------------------------------------------------
        self.widget_builder(Label,'name_field_bg')     
        #---------------------------------------------------------------------
        name_field = self.widget_builder(Text, 'name_field')
        name_field.insert('0.0', self.start_text['group_name'])
        name_field.bind("<Button>", lambda x: name_field.delete('0.0', END))
        #---------------------------------------------------------------------
        add_group = self.widget_builder(Button, 'add_group')
        add_group.config(command = lambda: self.group_creation(name_field))
        #---------------------------------------------------------------------
        cancel = self.widget_builder(Button, 'cancel')
        cancel.config(command = lambda: self.windows['group'].destroy())
        #---------------------------------------------------------------------
        
    # Создание окна ввода имени группы
    def run_name_window(self):
        self.windows['group'] = self.windows_builder(
            Toplevel(), self.windows_param['group']
        )
        self.creating_name_window_widgets()
    
    # Cоздание группы
    def group_creation(self, name_field):
        self.save_content()

        name_group = self.save_info_about_groups(name_field)
        self.creating_group_buttons(name_group)
        
        self.windows['group'].destroy()
        self.resizing_program()
        
    # Добавление группы
    def adding_group(self, name_group):
        with os.scandir(self.group_dir) as direct:
            {
                (self.replacing_save_file(name_group),
                 self.paths_field_update())
                 for folder in direct if folder.name == name_group
            }
