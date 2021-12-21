from tkinter import filedialog as fd
from tkinter import *
import webbrowser
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
        
    # Удаление путей
    def delete_path(self, widget, off_top):
        path = self.info_path[widget][1].cget('text')

        if path in self.info_programm:
            self.removing_shortcuts(path)

        self.button_offset(self.info_path, widget, off_top)
        self.removing_traces_widget(self.info_path, widget)
        self.resizing_program(len(self.info_path))

    # Добавление путей
    def adding_path(self, pressing=True):
        if len(self.info_path) == 26:
            return self.update_start_message()

        if pressing == True:
            input_get = self.paths_input.get('1.0','end-1c').strip('"')

            if len(re.findall(self.url_template, input_get)) > 0:
                self.creating_path_buttons(input_get)

            elif Path(input_get).exists() and len(input_get) != 0:
                if os.path.isfile(input_get):
                    self.create_and_move_shortcuts(input_get)
                else:
                    self.creating_path_buttons(input_get)
            else:
                self.paths_input.delete('0.0', END)
                text = fd.askopenfilename().replace('/', '\\')
                
                if len(text) != 0:
                    self.paths_input.insert('0.0', text)
                    return self.adding_path()
                return
                    
            self.update_start_message()

        self.resizing_program(len(self.info_path))
        
    # Открытие путей
    def open_path(self, widget=False):
        if widget != False:
            path_widget = {widget: self.info_path[widget]}
        else:
            path_widget = self.info_path

        for key in path_widget:
            path = path_widget[key][1].cget('text')
            
            if len(re.findall(self.url_template, path)) > 0:
                webbrowser.open_new_tab(path)

            elif os.path.isdir(path):
                os.startfile(os.path.realpath(path))
            else:
                if self.search_running_processes(path) == None:
                    os.startfile(self.info_programm[path])

            time.sleep(0.5)

    # Закрытие путей
    def close_path(self):
        {(self.closing_running_process(self.search_running_processes(elem)),\
         time.sleep(0.5)) for elem in self.info_programm}


class Group_logic(Group_internal_realization):
    # Удаление групп
    def delete_group(self, widget, off_top):
        self.deleting_group_folder(widget)
        self.button_offset(self.info_group, widget, off_top)
        self.removing_traces_widget(self.info_group, widget)
        self.resizing_program(len(self.info_group))

    # Cоздание виджетов окна ввода имени
    def creating_name_window_widgets(self):
        #---------------------------------------------------------------------
        self.widget_builder(Label,'name_field_bg')     
        #---------------------------------------------------------------------
        self.name_field = self.widget_builder(Text, 'name_field')
        self.name_field.insert('0.0', self.start_text['group_name'])
        self.name_field.bind(
            "<Button>", lambda x: self.name_field.delete('0.0', END)
        )
        #---------------------------------------------------------------------
        add_group = self.widget_builder(Button, 'add_group')
        add_group.config(command = lambda: self.group_creation())
        #---------------------------------------------------------------------
        cancel = self.widget_builder(Button, 'cancel')
        cancel.config(command = lambda: self.windows['group'].destroy())
        #---------------------------------------------------------------------
        
    # Создание окна ввода имени группы
    def run_name_window(self):
        self.windows['group'] = self.windows_constructor(\
            '', [300,150,960,540], [False, False], "wheat4", Toplevel()\
        )   
        
        self.creating_name_window_widgets()
    
    # Cоздание группы
    def group_creation(self):
        name_group = self.save_info_about_groups()
        self.creating_group_buttons(name_group)
        
        self.windows['group'].destroy()
        self.resizing_program(len(self.info_group))
        
    # Добавление группы
    def adding_group(self, name_group):
        with os.scandir(self.group_path) as direct:
            for folder in direct:
                if folder.name == name_group:
                    group_shortcuts = f'{self.group_path}\\{name_group}'\
                                      + '\\shortcuts'
                    
                    self.clearing_shortcut_directory()                    
                        
                    if len(os.listdir(group_shortcuts)) != 0:   
                        self.moving_group_files(group_shortcuts)

                    self.replacing_path_save_file(name_group)
                    self.data_cleansing()
                    
                    x,y,w = self.get_geometry_window(self.windows['main'])
                    self.windows['main'].destroy()
                    self.restart(x,y,w)