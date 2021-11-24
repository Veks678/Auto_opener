from tkinter import *
from tkinter import ttk
import os

from shutil import copy, rmtree

class internal_realization():
    def __init__(self, GUI, main_window):
        self.main_window = main_window
        self.GUI = GUI
        
    # Удаление следов групп
    def removing_traces_group(self, widget):
        self.GUI.INFO_GROUP[widget][1].destroy()
        widget.destroy()
        del self.GUI.INFO_GROUP[widget]  
        
    # Смещение кнопок удаления
    def offset_delete_buttons(self, index):
        for i, elem in enumerate(self.GUI.INFO_GROUP):
            if i > index-1:
                self.GUI.INFO_GROUP[elem][0] -= 24
                elem.place_configure(y = self.GUI.INFO_GROUP[elem][0]) 
                
    # Cмещение кнопок группы            
    def group_button_offset(self, index):
        for i, elem in enumerate(self.GUI.INFO_GROUP):
            if i > index-1:     
                self.GUI.INFO_GROUP[elem][1].place_configure(\
                    y = self.GUI.INFO_GROUP[elem][0]\
                ) 
    
    # Создание кнопок удаления
    def create_delete_buttons(self): 
        y = (24 * (len(self.GUI.INFO_GROUP) + 1)) + 26
        clear = self.GUI.widgets_constructor(self.main_window, Button,\
                                             ('clear','clear_p'), "gray25", "white")
        clear.config(command = lambda: self.delete_group(clear))
        clear.place(x = 519, y = y, height = 22, width = 22) 
        return y, clear      
    
    # Сохраняем информацию о группах
    def save_info_about_groups(self, widget):
        name_group = widget.get('0.0', END).rstrip('\n')
            
        os.mkdir(f'{self.GUI.group_path}\\{name_group}')
        os.mkdir(f'{self.GUI.group_path}\\{name_group}\\shortcuts')
        copy(self.GUI.save_path, f'{self.GUI.group_path}\\{name_group}')
        
        with os.scandir(self.GUI.shortcuts_path) as direct:
            for file in direct:
                copy(file, f'{self.GUI.group_path}\\{name_group}\\shortcuts') 
                    
        return name_group
    
    # Cоздание виджетов групп
    def creating_group_widgets(self, name_group):
        y = (24 * (len(self.GUI.INFO_GROUP) + 1)) + 26
        
        group = self.GUI.widgets_constructor(self.main_window, Button,\
                                             False, "gray25", "white",\
                                             ('Arial','8','bold'))
        group.config(command = lambda: self.group_inclusion(name_group),\
                     text = name_group)
        group.place(x = 395, y = y, height = 22, width = 123)   
        
        y, clear = self.create_delete_buttons()
        self.GUI.INFO_GROUP[clear] = [y, group] 
        
class Group_commands_logic(internal_realization):
    def __init__(self, GUI, main_window):
        internal_realization.__init__(self, GUI, main_window)
        self.main_window = main_window
        self.GUI = GUI
    
    # Cоздание виджетов окна ввода имени
    def creating_name_window_widgets(self, group_window):
        #---------------------------------------------------------------------
        label = self.GUI.widgets_constructor(group_window, Label, False,\
                                             "gray10", "white" )
        label.place(x = 5, y = 5, height = 95, width = 290)         
        #---------------------------------------------------------------------
        text = self.GUI.widgets_constructor(group_window, Text, False,\
                                             "white", "black" )
        text.insert('0.0', 'Введите имя группы')
        text.bind("<Button>", lambda x: text.delete('0.0', END))
        text.place(x = 40, y = 40, height = 25, width = 220)
        #---------------------------------------------------------------------
        add_group = self.GUI.widgets_constructor(group_window, Button, ['add_group'],\
                                                "gray30", "white" )
        add_group.config(command = lambda: self.group_creation(text, group_window))
        add_group.place(x = 5, y = 105, height = 40, width = 142) 
        #---------------------------------------------------------------------
        cancel = self.GUI.widgets_constructor(group_window, Button, ['cancel'],\
                                             "gray30", "white" )
        cancel.config(command = lambda: group_window.destroy())
        cancel.place(x = 153, y = 105, height = 40, width = 142)
        #---------------------------------------------------------------------
        
    # Создание окна ввода имени группыы
    def run_name_window(self):
        group_window = self.GUI.windows_constructor(\
            '', [300,150,960,540], [False, False], "wheat4", Toplevel()\
        )   
        
        self.creating_name_window_widgets(group_window)
        
    # Удаление групп
    def delete_group(self, widget):
        index = list(self.GUI.INFO_GROUP.keys()).index(widget)
        
        with os.scandir(self.GUI.group_path) as direct:
            for i, folder in enumerate(direct):
                if index == i:
                    mame_folder = str(folder)[10:].rstrip('>').replace("'",'')
                    self.removing_traces_group(widget)
                    rmtree(f'{self.GUI.group_path}\\{mame_folder}')
                        
        self.offset_delete_buttons(index)
        self.group_button_offset(index)
    
    # Cоздание группы
    def group_creation(self, widget, group_window):
        name_group = self.save_info_about_groups(widget)
        self.creating_group_widgets(name_group)
        
        group_window.destroy()
        
    # Включение группы
    def group_inclusion(self, name_group):
        with os.scandir(self.GUI.group_path) as direct:
            for folder in direct:
                if folder.name == name_group:
                    group_shortcuts = f'{self.GUI.group_path}\\{name_group}\\shortcuts'
                    {os.remove(f'{self.GUI.shortcuts_path}\\{file}')\
                     for file in os.listdir(self.GUI.shortcuts_path)}                    
                        
                    if len(os.listdir(group_shortcuts)) != 0:   
                        {copy(f'{group_shortcuts}\\{file}',self.GUI.shortcuts_path)\
                         for file in os.listdir(group_shortcuts) if file != 'shortcuts'}

                    os.remove(self.GUI.save_path)
                    copy(f'{self.GUI.group_path}\\{name_group}\\save_path.txt',\
                         f'{os.getcwd()}\\source_codes\\save') 
                    
                    self.GUI.data_cleansing()
                    x, y = self.main_window.winfo_x(), self.main_window.winfo_y()
                    self.main_window.destroy()
                    self.GUI.restart(x, y)   
                
    