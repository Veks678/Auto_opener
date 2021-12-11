from tkinter import *

from shutil import copy
from psutil import process_iter
import win32com.client
import pyperclip
import os

from .customizing_widgets import arg_widgets


class GUI_realization_logic():
    # Отображение изображений нажатия
    def displaying_click_images(self, widget, key):
        if arg_widgets[key]['key'] != False:
            widget.config(image=self.img_icon[arg_widgets[key]['key'][0]])
            if len(arg_widgets[key]['key']) > 1:
                widget.bind('<ButtonPress-1>', lambda x: widget.config(\
                    image = self.img_icon[arg_widgets[key]['key'][1]]\
                ))
                widget.bind('<ButtonRelease-1>', lambda x: widget.config(\
                    image = self.img_icon[arg_widgets[key]['key'][0]]\
                ))

    # Cоздание сохраненных виджетов
    def creating_saved_widgets(self, group_dir, content):
        {self.creating_group_widgets(folder.name)\
         for folder in group_dir}

        {(self.paths_field.insert(index, elem.rstrip('\n')),\
          self.adding_path(False))\
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
            
            self.INFO_PROGRAMM[file.name] = \
                f'{self.shortcuts_path}\\{file.name}'

        return content, number_buttons

    # Сохранение контента
    def save_content(self, exit=False):
        self.preservation_content()
        self.data_cleansing()

        x, y = self.master.winfo_x(), self.master.winfo_y()
        self.master.destroy()
        if exit == False:
            self.restart(x, y, self.w, self.h)
    
    # Открытие стартового контента
    def opening_starter_content(self):
        with open(self.save_path,"r") as file_path,\
             os.scandir(self.shortcuts_path) as main_dir,\
             os.scandir(self.group_path) as group_dir:

            content, number_buttons = \
                self.getting_content_info(file_path, main_dir)
            
            self.creating_saved_widgets(group_dir, content)

    # Получение статуса процесса
    def process_status(self, process_name):
        return len([proc.info['name'] for proc in process_iter(['name'])\
                    if proc.info['name'] == process_name])

    # Очистка данных
    def data_cleansing(self):
        {data.clear() 
        for data in (self.INFO_PATH, self.INFO_PROGRAMM, self.INFO_GROUP)}

    # Cохранение контента
    def preservation_content(self):
        number_buttons, content = 0, ''
        for num in range(len(self.paths_field.get(0, END))):
            if '.lnk' not in self.paths_field.get(num):
                number_buttons += 1
                text_listbox = self.paths_field.get(num)
                content += f'{text_listbox}\n'

        with open(self.save_path, 'w') as file_path:
            file_path.write(f'buttons_len: {number_buttons}\n{content}')

    # Работа с буфером обмена
    def work_with_clipboard(self, key):
        if self.paths_input.get('0.0', END).rstrip('\n') == \
           self.start_text['paths_input']:
            self.paths_input.delete('0.0', END)
            self.paths_input.config(fg='white')

        if key.char == '\x16':
            self.paths_input.insert('0.0', pyperclip.paste())


class Path_internal_realization():
    # Удаление ярлыков
    def removing_shortcuts(self, field_get):
        with os.scandir(self.shortcuts_path) as direct:
            {os.remove(self.INFO_PROGRAMM[field_get]) \
             for file in direct if file.name == field_get}
                    
        del self.INFO_PROGRAMM[field_get]

    # Удаление следов путей
    def removing_traces_path(self, widget, index):
        del self.INFO_PATH[widget]
        self.paths_field.delete(index)
    
    # Смещение кнопок удаления путей
    def offset_delete_buttons_path(self, index):
        for i, elem in enumerate(self.INFO_PATH):
            if i > index - 1:
                self.INFO_PATH[elem] -= 20
                elem.place_configure(y=self.INFO_PATH[elem])

    # Обновление стартового сообщения
    def update_start_message(self):
        self.paths_input.delete('0.0', END)
        self.paths_input.insert('0.0', self.start_text['paths_input'])

    # Создание и перемещение ярлыков
    def create_and_move_shortcuts(self, text_get):
        name = ''.join(text_get.split('\\')[-1:])[0:-4].rstrip('.')
        
        shortcut = win32com.client.Dispatch("WScript.Shell")
        shortcut = shortcut.CreateShortCut(\
            (f'{self.shortcuts_path}\\{name}.lnk')\
        )
        shortcut.Targetpath = text_get
        shortcut.save()

        self.INFO_PROGRAMM[f'{name}.lnk'] = \
            f'{self.shortcuts_path}\\{name}.lnk'
        
        self.paths_field.insert(END, f'{name}.lnk')

    # Создание кнопок удаления путей
    def create_delete_buttons_path(self):
        y = arg_widgets['clear_path']['y'] = 48
        y = (20 * (len(self.INFO_PATH) + 1)) + (y - 20)
        arg_widgets['clear_path']['y'] = y

        clear_main = self.widget_builder(Button, 'clear_path')
        
        return y, clear_main

    # Поиск запущенного процесса
    def search_running_processes(self, elem):
        programm_name = ''.join(
            self.INFO_PROGRAMM[elem].split('\\')[-1:]
        )[0:-3]
        
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


class Group_internal_realization():
    # Удаление следов групп
    def removing_traces_group(self, widget):
        self.INFO_GROUP[widget][1].destroy()
        widget.destroy()
        del self.INFO_GROUP[widget]

    # Смещение кнопок удаления групп
    def offset_delete_buttons_group(self, index):
        for i, elem in enumerate(self.INFO_GROUP):
            if i > index-1:
                self.INFO_GROUP[elem][0] -= 24
                elem.place_configure(y = self.INFO_GROUP[elem][0])

    # Cмещение кнопок группы            
    def group_button_offset(self, index):
        {self.INFO_GROUP[elem][1].place_configure(y = self.INFO_GROUP[elem][0])\
         for i, elem in enumerate(self.INFO_GROUP) if i > index-1}

    # Создание кнопок удаления групп
    def create_delete_buttons_group(self): 
        y = arg_widgets['clear_group']['y'] = 26
        y = (24 * (len(self.INFO_GROUP) + 1)) + y
        arg_widgets['clear_group']['y'] = y
        
        clear_group = self.widget_builder(Button, 'clear_group')
        clear_group.config(command = lambda: self.delete_group(clear_group))

        return y, clear_group     

    # Сохраняем информацию о группах
    def save_info_about_groups(self, widget):
        name_group = widget.get('0.0', END).rstrip('\n')
            
        self.preservation_content()
        os.mkdir(f'{self.group_path}\\{name_group}')
        os.mkdir(f'{self.group_path}\\{name_group}\\shortcuts')
        copy(self.save_path, f'{self.group_path}\\{name_group}')
        
        with os.scandir(self.shortcuts_path) as direct:
            {copy(file, f'{self.group_path}\\{name_group}\\shortcuts')\
             for file in direct}
                    
        return name_group

     # Cоздание виджетов групп
    def creating_group_widgets(self, name_group):
        y = arg_widgets['group']['y'] = 26
        y = (24 * (len(self.INFO_GROUP) + 1)) + y
        arg_widgets['group']['y'] = y
        
        group = self.widget_builder(Button, 'group')
        group.config(
            command = lambda: self.adding_group(name_group), text = name_group
        ) 
        y, clear = self.create_delete_buttons_group()
        self.INFO_GROUP[clear] = [y, group]