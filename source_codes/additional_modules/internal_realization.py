from tkinter import *
from shutil import copy, rmtree
from psutil import process_iter
import win32com.client
import pyperclip
import os

class GUI_realization_logic():
    def __init__(self):
        self.dynamic_height_windows = {
            tuple(range(0,11)): 315,
            tuple(range(11,15)): 411,
            tuple(range(15,19)): 507,
            tuple(range(19,23)): 603,
            tuple(range(23,27)): 700,
        }
        
        self.dynamic_widgets_key = [
            'paths_field_bg', 'create_group_bg', 'paths_input', 'add_path'
        ]
        
        self.dynamic_height_widgets = {
            315: {
                'paths_field_bg': 241,
                'create_group_bg': 266,
                'paths_input': 289,
                'add_path': 289
            },
            411: {
                'paths_field_bg': 337,
                'create_group_bg': 362,
                'paths_input': 385,
                'add_path': 385
            },
            507: {
                'paths_field_bg': 433,
                'create_group_bg': 458,
                'paths_input': 481,
                'add_path': 481 
            },
            603: {
                'paths_field_bg': 529,
                'create_group_bg': 554,
                'paths_input': 578,
                'add_path': 578 
            },
            700: {
                'paths_field_bg': 625,
                'create_group_bg': 651,
                'paths_input': 674,
                'add_path': 674 
            }
        }

    # Вычисление динамической высоты виджета
    def get_dynamic_height_widget(self, dicti_len, key_dict, h, y):
        y = (h * (dicti_len) + 1) + y
        for key in key_dict:
            self.arg_widgets[key]['y'] = y

        return y

    # Удаление следов виджетов
    def removing_traces_widget(self, info_dict, widget):
        info_dict[widget][1].destroy()
        del info_dict[widget]
        widget.destroy()

    # Смещение кнопок
    def button_offset(self, info_dict, widget, offset_value):
        for key in info_dict:
            if info_dict[key][0] > info_dict[widget][0]:
                info_dict[key][0] -= offset_value
                key.place_configure(y = info_dict[key][0])
                info_dict[key][1].place_configure(y = info_dict[key][0])

    # Получить геометрию окна
    def get_geometry_window(self, windows):
        return windows.winfo_x(), windows.winfo_y(), windows.winfo_width()

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

    # Задать геометрию окна
    def set_window_geometry(self, window, param):
        window.geometry(
            f'{param["w"]}x' + f'{param["h"]}+' +\
            f'{param["x"]}+' + f'{param["y"]}'
        )
    
    # Упаковка виджетов
    def packaging_widgets(self, widget, key):
        widget.place(
            x=self.arg_widgets[key]['x'],
            y=self.arg_widgets[key]['y'],
            height=self.arg_widgets[key]['h'],
            width=self.arg_widgets[key]['w'],
        )

    # Изменение размеров программы
    def resizing_program(self, len_info_dict):
        height_dynamic = self.get_dynamic_height_window(len_info_dict)
        height_main = self.master.winfo_height()

        if height_dynamic != height_main != 1:  
            self.save_content()
            self.tk_param["x"] = self.master.winfo_x()
            self.tk_param["y"] = self.master.winfo_y()
            self.tk_param["h"] = height_dynamic
            self.set_window_geometry(self.master, self.tk_param)
            self.set_height_of_dynamic_widgets(height_dynamic)
            self.change_dynamic_widgets()

    # Получить динамическую высоту окна
    def get_dynamic_height_window(self, path_field_length):
        height_range = [
            height_range for height_range in self.dynamic_height_windows 
            if path_field_length in height_range
        ][0]

        return self.dynamic_height_windows[height_range]
    
    # Упаковка виджетов
    def packaging_widgets(self, widget, key):
        widget.place(
            x=self.arg_widgets[key]['x'],
            y=self.arg_widgets[key]['y'],
            height=self.arg_widgets[key]['h'],
            width=self.arg_widgets[key]['w'],
        )
    
    # Изменить динамические виджеты
    def change_dynamic_widgets(self):
        self.paths_field_bg.place_forget()
        self.create_group_bg.place_forget()
        self.paths_input.place_forget()
        self.add_path.place_forget()

        self.packaging_widgets(self.paths_field_bg, 'paths_field_bg')
        self.packaging_widgets(self.create_group_bg, 'create_group_bg')
        self.packaging_widgets(self.paths_input, 'paths_input')
        self.packaging_widgets(self.add_path, 'add_path')
            
    # Установить высоту динамических виджетов 
    def set_height_of_dynamic_widgets(self, height):
        for index, key in enumerate(['h','h','y','y']):
            widgets_key = self.dynamic_widgets_key[index]
            self.arg_widgets[widgets_key][key] = \
                self.dynamic_height_widgets[height][widgets_key]
        
    # Стартовая длина контента
    def start_length_content(self):
        with open(self.save_path,"r") as save_path_file,\
             os.scandir(self.shortcuts_path) as shortcuts_dir,\
             os.scandir(self.group_path) as group_dir:
            
            return max(
                [len(self.getting_content_info(
                        save_path_file, shortcuts_dir
                    )),
                len([folder.name for folder in group_dir])]
            )

    # Cоздание сохраненных виджетов контента
    def creating_saved_content_widgets(self, content):
        {self.creating_path_buttons(elem.rstrip('\n'))
         for elem in content}

    # Cоздание сохраненных виджетов групп
    def create_saved_group_widgets(self, group_dir):
        {self.creating_group_buttons(folder.name)\
         for folder in group_dir}

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

    # Сохранение контента
    def save_content(self, exit=False):
        self.preservation_content()
        if exit == True:
            self.master.destroy()
    
    # Открытие контента
    def display_content(self):
        with open(self.save_path,"r") as save_path_file,\
             os.scandir(self.shortcuts_path) as shortcuts_dir,\
             os.scandir(self.group_path) as group_dir:

            content = self.getting_content_info(save_path_file, shortcuts_dir)
            self.creating_saved_content_widgets(content)
            self.create_saved_group_widgets(group_dir)

    # Получение статуса процесса
    def process_status(self, process_name):
        return len([
            proc.info['name'] for proc in process_iter(['name'])\
            if proc.info['name'] == process_name
        ])

    # Cохранение контента
    def preservation_content(self):
        content = ''
        for key in self.info_path:
            path = self.info_path[key][1].cget('text')

            if '.lnk' not in path:
                text_listbox = path
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
    # Создание кнопок путей
    def creating_path_buttons(self, path):
        off_top, between = 24, 46
        y = self.get_dynamic_height_widget(
            len(self.info_path), ('path_button', 'clear_path'),
            off_top, between
        )
        
        clear = self.widget_builder(Button, 'clear_path')
        clear.config(command=lambda: self.delete_path(clear, off_top))

        path_button = self.widget_builder(Button, 'path_button')
        path_button.config(
            command = lambda: self.open_path(clear),
            text = path, anchor="w", borderwidth=0
        )

        self.info_path[clear] = [y, path_button]

    # Удаление ярлыков
    def removing_shortcuts(self, field_get):
        with os.scandir(self.shortcuts_path) as direct:
            {os.remove(self.info_programm[field_get]) \
             for file in direct if file.name == field_get}
                    
        del self.info_programm[field_get]

    # Обновление стартового сообщения
    def update_start_message(self):
        self.paths_input.delete('0.0', END)
        self.paths_input.config(fg='gray65')
        self.paths_input.insert('0.0', self.start_text['paths_input'])

    # Создание и перемещение ярлыков
    def create_and_move_shortcuts(self, path):
        name = ''.join(path.split('\\')[-1:])[0:-4].rstrip('.')
        
        shortcut = win32com.client.Dispatch("WScript.Shell")
        shortcut = shortcut.CreateShortCut(\
            (f'{self.shortcuts_path}\\{name}.lnk')\
        )
        shortcut.Targetpath = path
        shortcut.save()

        self.info_programm[f'{name}.lnk'] = \
            f'{self.shortcuts_path}\\{name}.lnk'

        self.creating_path_buttons(f'{name}.lnk')

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
    # Обновление поля путей
    def paths_field_update(self):
        {(widget.destroy(), self.info_path[widget][1].destroy())
        for widget in self.info_path}

        self.info_programm.clear()
        self.info_path.clear()

        with open(self.save_path,"r") as save_path_file,\
             os.scandir(self.shortcuts_path) as shortcuts_dir:

            content = self.getting_content_info(save_path_file, shortcuts_dir)
            self.creating_saved_content_widgets(content)
        
        self.resizing_program(
            max(len(self.info_group), len(self.info_path))
        )

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


    # Удаление папки группы
    def deleting_group_folder(self, widget):
        path = self.info_group[widget][1].cget('text')
        
        with os.scandir(self.group_path) as direct:
            {rmtree(f'{self.group_path}\\{fold.name}') 
             for fold in direct if fold.name == path}

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

    # Cоздание кнопок групп
    def creating_group_buttons(self, name_group):
        off_top, between = 24, 46
        y = self.get_dynamic_height_widget(
            len(self.info_group), ('group', 'clear_group'),
            off_top, between
        )
        
        clear = self.widget_builder(Button, 'clear_group')
        clear.config(command = lambda: self.delete_group(clear, off_top))
        
        group = self.widget_builder(Button, 'group')
        group.config(
            command = lambda: self.adding_group(name_group),
            text = name_group, borderwidth=0
        ) 

        self.info_group[clear] = [y, group]