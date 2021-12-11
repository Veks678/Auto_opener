from tkinter import filedialog as fd
from tkinter import *
import webbrowser
import time
import os
import re

from shutil import copy, rmtree
from pathlib import Path

from .customizing_widgets import windows
from .internal_realization import Path_internal_realization,\
                                  Group_internal_realization

class Path_logic(Path_internal_realization):
    def __init__(self): 
        self.url_template = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    # Удаление путей
    def delete_path(self, widget):
        index = list(self.INFO_PATH.keys()).index(widget)
        field_get = self.paths_field.get(index)

        if field_get in self.INFO_PROGRAMM:
            self.removing_shortcuts(field_get)

        self.removing_traces_path(widget, index)
        widget.destroy()
        self.offset_delete_buttons_path(index)

    # Добавление путей
    def adding_path(self, pressing=True):
        if (20 * len(self.INFO_PATH) + 28) == 268:
            return self.update_start_message()

        elif pressing == True:
            text_get = self.paths_input.get('1.0','end-1c').strip('"')

            if len(re.findall(self.url_template, text_get)) > 0:
                self.paths_field.insert(END, text_get)

            elif Path(text_get).exists() and len(text_get) != 0:
                if os.path.isfile(text_get):
                    self.create_and_move_shortcuts(text_get)
                else:
                    self.paths_field.insert(END, text_get)
            else:
                self.paths_input.delete('0.0', END)
                text = fd.askopenfilename().replace('/', '\\')
                
                if len(text) != 0:
                    self.paths_input.insert('0.0', text)
                    return self.adding_path()
                return
                    
            self.update_start_message()

        y, clear = self.create_delete_buttons_path()
        clear.config(command=lambda: self.delete_path(clear))
        self.INFO_PATH[clear] = y

    # Открытие путей
    def open_path(self):
        for elem in list(self.paths_field.get(0, END)):
            if len(re.findall(self.url_template, elem)) > 0:
                webbrowser.open_new_tab(elem)

            elif os.path.isdir(elem):
                os.startfile(os.path.realpath(elem))
            else:
                if self.search_running_processes(elem) == None:
                    os.startfile(self.INFO_PROGRAMM[elem])

            time.sleep(0.5)

    # Закрытие путей
    def close_path(self):
        {(self.closing_running_process(self.search_running_processes(elem)),\
         time.sleep(0.5)) for elem in self.INFO_PROGRAMM}


class Group_logic(Group_internal_realization):
    # Cоздание виджетов окна ввода имени
    def creating_name_window_widgets(self):
        #---------------------------------------------------------------------
        self.widget_builder(Label,'name_group_bg')     
        #---------------------------------------------------------------------
        name_group = self.widget_builder(Text, 'name_group')
        name_group.insert('0.0', self.start_text['group_name'])
        name_group.bind("<Button>", lambda x: name_group.delete('0.0', END))
        #---------------------------------------------------------------------
        add_group = self.widget_builder(Button, 'add_group')
        add_group.config(
            command = lambda: self.group_creation(name_group)
        )
        #---------------------------------------------------------------------
        cancel = self.widget_builder(Button, 'cancel')
        cancel.config(command = lambda: windows['group'].destroy())
        #---------------------------------------------------------------------
        
    # Создание окна ввода имени группыы
    def run_name_window(self):
        windows['group'] = self.windows_constructor(\
            '', [300,150,960,540], [False, False], "wheat4", Toplevel()\
        )   
        
        self.creating_name_window_widgets()
        
    # Удаление групп
    def delete_group(self, widget):
        index = list(self.INFO_GROUP.keys()).index(widget)
        
        with os.scandir(self.group_path) as direct:
            for i, fold in enumerate(direct):
                if index == i:
                    mame_fold = str(fold)[10:].rstrip('>').replace("'",'')
                    self.removing_traces_group(widget)
                    rmtree(f'{self.group_path}\\{mame_fold}')
                        
        self.offset_delete_buttons_group(index)
        self.group_button_offset(index)
    
    # Cоздание группы
    def group_creation(self, widget):
        name_group = self.save_info_about_groups(widget)
        self.creating_group_widgets(name_group)
        
        windows['group'].destroy()
        
    # Добавление группы
    def adding_group(self, name_group):
        with os.scandir(self.group_path) as direct:
            for folder in direct:
                if folder.name == name_group:
                    group_shortcuts = \
                        f'{self.group_path}\\{name_group}\\shortcuts'
                    
                    {os.remove(f'{self.shortcuts_path}\\{file}')\
                     for file in os.listdir(self.shortcuts_path)}                    
                        
                    if len(os.listdir(group_shortcuts)) != 0:   
                        {copy(f'{group_shortcuts}\\{file}',
                         self.shortcuts_path)\
                         for file in os.listdir(group_shortcuts) 
                         if file != 'shortcuts'}

                    os.remove(self.save_path)
                    copy(f'{self.group_path}\\{name_group}\\save_path.txt',\
                         f'{self.base_dir}\\save') 

                    self.data_cleansing()
                    
                    x, y = windows['main'].winfo_x(),\
                           windows['main'].winfo_y()
                    
                    windows['main'].destroy()
                    self.restart(x, y, self.w, self.h)