from tkinter import *

from shutil import copy, rmtree
from psutil import process_iter
import win32com.client
import pyperclip
import os

class GUI_realization_logic():
    def __init__(self):
        self.dynamic_height_windows = {
            tuple(range(0,13)): 317,
            tuple(range(13,20)): 457,
            tuple(range(20,27)): 597,
            tuple(range(27,34)): 737,
            tuple(range(34,41)): 877,
        }
        
        self.dynamic_widgets_key = [
            'paths_field', 'create_group_bg', 'paths_input', 'add_path'
        ]
        
        self.dynamic_height_widgets = {
            317: {
                'paths_field': 243,
                'create_group_bg': 267,
                'paths_input': 291,
                'add_path': 291
            },
            457: {
                'paths_field': 383,
                'create_group_bg': 407,
                'paths_input': 431,
                'add_path': 431
            },
            597: {
                'paths_field': 523,
                'create_group_bg': 547,
                'paths_input': 571,
                'add_path': 571 
            },
            737: {
                'paths_field': 663,
                'create_group_bg': 713,
                'paths_input': 711,
                'add_path': 711 
            },
            877: {
                'paths_field': 803,
                'create_group_bg': 853,
                'paths_input': 851,
                'add_path': 851 
            }
        }

    # Распаковать информацию об аргументах виджетов
    def unpack_widgets_arg_info(self, config_file):
        split_str = [e.split(' = ') for e in config_file.split('>')]
        key = [elem[0] for elem in split_str]
        filt_value = [elem[1].split(', ') for elem in split_str]
        filt_value = [[e.split(': ') for e in elem] for elem in filt_value]
        
        value = [{e[0]: e[1] for e in elem} for elem in filt_value]
        
        return {key: value[index] for index, key in enumerate(key)}

    # Чтение конфигурационного файла
    def reading_configuration_file(self):
        with open(self.config_path,"r") as config_file:
            config_file = config_file.read().replace('\n','')

        self.arg_widgets = self.unpack_widgets_arg_info(config_file)

        for e in self.arg_widgets:
            self.arg_widgets[e]['key'] = self.arg_widgets[e]['key'].split('.')
            self.arg_widgets[e]['x'] = int(self.arg_widgets[e]['x'])
            self.arg_widgets[e]['y'] = int(self.arg_widgets[e]['y'])
            self.arg_widgets[e]['w'] = int(self.arg_widgets[e]['w'])
            self.arg_widgets[e]['h'] = int(self.arg_widgets[e]['h'])       

    # Отображение изображений нажатия
    def displaying_click_images(self, widget, key):
        if self.arg_widgets[key]['key'] != ['False']:
            widget.config(
                image=self.img_icon[self.arg_widgets[key]['key'][0]]
            )
            
            if len(self.arg_widgets[key]['key']) > 1:
                widget.bind('<ButtonPress-1>', lambda x: widget.config(\
                    image = self.img_icon[self.arg_widgets[key]['key'][1]]\
                ))
                widget.bind('<ButtonRelease-1>', lambda x: widget.config(\
                    image = self.img_icon[self.arg_widgets[key]['key'][0]]\
                ))

    # Получить динамическую высоту
    def get_dynamic_height(self, path_field_length):
        height_range = [
            height_range for height_range in self.dynamic_height_windows 
            if path_field_length in height_range
        ][0]

        return self.dynamic_height_windows[height_range]

    # Изменения положения виджетов
    def changing_position_widgets(self, height_windows):
        for index, key in enumerate(['h','h','y','y']):
            widgets_key = self.dynamic_widgets_key[index]
            self.arg_widgets[widgets_key][key] = \
                self.dynamic_height_widgets[height_windows][widgets_key]
        
    # Стартовая длина поля путей
    def starting_length_path_field(self):
        with open(self.save_path,"r") as save_path_file,\
             os.scandir(self.shortcuts_path) as shortcuts_dir:
            
            return len(self.getting_content_info(
                save_path_file, shortcuts_dir
            ))

    # Cоздание сохраненных виджетов
    def creating_saved_widgets(self, group_dir, content):
        {self.creating_group_widgets(folder.name)\
         for folder in group_dir}

        {(self.paths_field.insert(index, elem.rstrip('\n')),\
          self.adding_path(False))\
          for index, elem in enumerate(content)}

    # Получение информации о контенте
    def getting_content_info(self, save_path_file, shortcuts_dir):
        try:
            content = save_path_file.readlines()[0:]
        except IndexError:
            content = []

        for file in shortcuts_dir:
            if f'{file.name}\n' not in content:
                content.append(f'{file.name}\n')
            
            self.info_programm[file.name] = \
                f'{self.shortcuts_path}\\{file.name}'

        return content

    # Получить геометрию окна
    def get_geometry_window(self, windows):
        return windows.winfo_x(), windows.winfo_y(), windows.winfo_width()

    # Сохранение контента
    def save_content(self, exit=False):
        self.preservation_content()
        self.data_cleansing()

        x,y,w = self.get_geometry_window(self.master)
        self.master.destroy()
        if exit == False:
            self.restart(x,y,w)
    
    # Открытие стартового контента
    def opening_starter_content(self):
        with open(self.save_path,"r") as save_path_file,\
             os.scandir(self.shortcuts_path) as shortcuts_dir,\
             os.scandir(self.group_path) as group_dir:

            content = self.getting_content_info(save_path_file, shortcuts_dir)
            self.creating_saved_widgets(group_dir, content)

    # Получение статуса процесса
    def process_status(self, process_name):
        return len([
            proc.info['name'] for proc in process_iter(['name'])\
            if proc.info['name'] == process_name
        ])

    # Очистка данных
    def data_cleansing(self):
        dict_data = (self.info_path, self.info_programm, self.info_group)
        {data.clear() for data in dict_data}

    # Cохранение контента
    def preservation_content(self):
        content = ''
        for num in range(len(self.paths_field.get(0, END))):
            if '.lnk' not in self.paths_field.get(num):
                text_listbox = self.paths_field.get(num)
                content += f'{text_listbox}\n'

        with open(self.save_path, 'w') as file_path:
            file_path.write(f'{content}')

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
            {os.remove(self.info_programm[field_get]) \
             for file in direct if file.name == field_get}
                    
        del self.info_programm[field_get]

    # Удаление следов путей
    def removing_traces_path(self, widget, index):
        del self.info_path[widget]
        self.paths_field.delete(index)
    
    # Изменение размеров программы
    def resizing_program(self):
        height_dynamic = self.get_dynamic_height(len(self.info_path))
        height_main = self.windows['main'].winfo_height()
        if height_dynamic != height_main != 1:  
            self.save_content()

    # Смещение кнопок удаления путей
    def offset_delete_buttons_path(self, index):
        for i, elem in enumerate(self.info_path):
            if i > index - 1:
                self.info_path[elem] -= 20
                elem.place_configure(y=self.info_path[elem])

    # Обновление стартового сообщения
    def update_start_message(self):
        self.paths_input.delete('0.0', END)
        self.paths_input.config(fg='gray65')
        self.paths_input.insert('0.0', self.start_text['paths_input'])

    # Создание и перемещение ярлыков
    def create_and_move_shortcuts(self, input_get):
        name = ''.join(input_get.split('\\')[-1:])[0:-4].rstrip('.')
        
        shortcut = win32com.client.Dispatch("WScript.Shell")
        shortcut = shortcut.CreateShortCut(\
            (f'{self.shortcuts_path}\\{name}.lnk')\
        )
        shortcut.Targetpath = input_get
        shortcut.save()

        self.info_programm[f'{name}.lnk'] = \
            f'{self.shortcuts_path}\\{name}.lnk'
        
        self.paths_field.insert(END, f'{name}.lnk')

    # Создание кнопок удаления путей
    def create_delete_buttons_path(self):
        y = self.arg_widgets['clear_path']['y'] = 48
        y = (20 * (len(self.info_path) + 1)) + (y - 20)
        self.arg_widgets['clear_path']['y'] = y

        clear_main = self.widget_builder(Button, 'clear_path')
        clear_main.config(command=lambda: self.delete_path(clear_main))
        self.info_path[clear_main] = y

        return y, clear_main

    # Поиск запущенного процесса
    def search_running_processes(self, elem):
        programm_name = ''.join(
            self.info_programm[elem].split('\\')[-1:]
        )[0:-3]
        
        proc_name = [
            proc.info['name'] for proc in process_iter(['name'])\
            if proc.info['name'] != None and\
            proc.info['name'][0:-3] == programm_name
        ]
        
        if len(proc_name) != 0:
            return proc_name

    # Закрытие запущенного процесса
    def closing_running_process(self, proc_name):
        if proc_name != None:
            {proc.kill() for proc in process_iter(['name'])\
             if proc.info['name'] == proc_name[0]}


class Group_internal_realization():
    # Очистка директории ярлыков
    def clearing_shortcut_directory(self):
        {os.remove(f'{self.shortcuts_path}\\{file}')\
         for file in os.listdir(self.shortcuts_path)}

    # Замена файла сохранений путей
    def replacing_path_save_file(self, name_group):
        os.remove(self.save_path)
        
        copy(f'{self.group_path}\\{name_group}\\save_path.txt',\
             f'{self.base_dir}\\save')    

    # Перемещение файлов группы
    def moving_group_files(self, group_shortcuts):
        {copy(f'{group_shortcuts}\\{file}',
         self.shortcuts_path)\
         for file in os.listdir(group_shortcuts) 
         if file != 'shortcuts'}

    # Смещение кнопок удаления групп
    def offset_delete_buttons_group(self, index):
        for i, elem in enumerate(self.info_group):
            if i > index-1:
                self.info_group[elem][0] -= 24
                elem.place_configure(y = self.info_group[elem][0])

    # Cмещение кнопок группы            
    def group_button_offset(self, index):
        {self.info_group[elem][1].place_configure(y = self.info_group[elem][0])\
         for i, elem in enumerate(self.info_group) if i > index-1}

    # Создание кнопок удаления групп
    def create_delete_buttons_group(self): 
        y = self.arg_widgets['clear_group']['y'] = 26
        y = (24 * (len(self.info_group) + 1)) + y
        self.arg_widgets['clear_group']['y'] = y
        
        clear_group = self.widget_builder(Button, 'clear_group')
        clear_group.config(command = lambda: self.delete_group(clear_group))

        return y, clear_group     

    # Удаление групп
    def delete_group(self, widget):
        index = list(self.info_group.keys()).index(widget)
        
        with os.scandir(self.group_path) as direct:
            for i, fold in enumerate(direct):
                if index == i:
                    mame_fold = str(fold)[10:].rstrip('>').replace("'",'')
                    self.removing_traces_group(widget)
                    rmtree(f'{self.group_path}\\{mame_fold}')
                        
        self.offset_delete_buttons_group(index)
        self.group_button_offset(index)

    # Удаление следов групп
    def removing_traces_group(self, widget):
        self.info_group[widget][1].destroy()
        widget.destroy()
        del self.info_group[widget]

    # Сохраняем информацию о группах
    def save_info_about_groups(self):
        name_group = self.name_field.get('0.0', END).rstrip('\n')
            
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
        y = self.arg_widgets['group']['y'] = 26
        y = (24 * (len(self.info_group) + 1)) + y
        self.arg_widgets['group']['y'] = y
        
        group = self.widget_builder(Button, 'group')
        group.config(
            command = lambda: self.adding_group(name_group),
            text = name_group
        ) 
        y, clear = self.create_delete_buttons_group()
        self.info_group[clear] = [y, group]