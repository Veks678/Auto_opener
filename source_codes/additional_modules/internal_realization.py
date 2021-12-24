from tkinter import *
import os

from shutil import copy, rmtree
from psutil import process_iter
import webbrowser
import pyperclip

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

    # Удаление контента через кнопку
    def delete_content_via_button(self, key, widget, off_top):
        index_of_press = [
            index
            for index, elem in enumerate(self.info_buttons[key])
            if elem['clear_button'] == widget
        ][0]

        if key == 'group':
            self.deleting_group_folder(index_of_press)
              
        self.button_offset(key, index_of_press, off_top)
        self.removing_traces_widget(key, index_of_press)
        self.resizing_program()

    # Вычисление динамической высоты виджета
    def get_dynamic_height_widget(self, key_content, key_image, h, y):
        y = (h * (len(self.info_buttons[key_content])) + 1) + y
        for key in key_image:
            self.arg_widgets[key]['y'] = y

        return y

    # Удаление следов виджетов
    def removing_traces_widget(self, key, index_of_press):
        self.info_buttons[key][index_of_press][f'{key}_button'].destroy()
        self.info_buttons[key][index_of_press]['clear_button'].destroy()
        del self.info_buttons[key][index_of_press]
        if key == 'path':
            del self.info_content[index_of_press]

    # Смещение кнопок
    def button_offset(self, key, index_of_press, offset_value):
        for dict in self.info_buttons[key]:
            if dict['y'] > self.info_buttons[key][index_of_press]['y']:
                dict['y'] -= offset_value
                dict[f'{key}_button'].place_configure(y = dict['y'])
                dict['clear_button'].place_configure(y = dict['y'])

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
        with open(self.config_dir, "r") as config_file:
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
    def resizing_program(self, ):
        len_content = max(
            len(self.info_buttons['path']),
            len(self.info_buttons['group'])
        )
        height_dynamic = self.get_dynamic_height_window(len_content)
        height_main = self.master.winfo_height()

        if height_dynamic != height_main != 1:  
            self.save_content()
            self.windows_param['main']["x"] = self.master.winfo_x()
            self.windows_param['main']["y"] = self.master.winfo_y()
            self.windows_param['main']["h"] = height_dynamic
            self.set_window_geometry(self.master, self.windows_param['main'])
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
        with open(self.retention_dir,"r") as retention_file,\
             os.scandir(self.group_dir) as group_dir:
            
            self.getting_content_info(retention_file)

            return max(
                [len(self.info_content),
                 len([folder.name for folder in group_dir])]
            )

    # Cоздание сохраненных виджетов контента
    def creating_saved_content_widgets(self):
        {
            self.creating_path_buttons(elem['path'])
            for elem in self.info_content
        }

    # Cоздание сохраненных виджетов групп
    def create_saved_group_widgets(self, group_dir):
        {
            self.creating_group_buttons(folder.name)
            for folder in group_dir
        }
         
    # Получение информации о контенте
    def getting_content_info(self, retention_dir):
        try:
            content = retention_dir.readlines()[0:]
        except IndexError:
            self.info_content = []
            return

        content = [elem.split(',') for elem in content]
        
        content = [
            [elem[0].split('>'), elem[1].strip('\n').split('>')]
            for elem in content
        ]
        
        self.info_content = [
            {elem[0][0]: elem[0][1], elem[1][0]: elem[1][1]} 
            for elem in content
        ]

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
    
    # Открытие контента
    def display_content(self):
        with open(self.retention_dir,"r") as retention_dir,\
             os.scandir(self.group_dir) as group_dir:

            self.getting_content_info(retention_dir)
            self.creating_saved_content_widgets()
            self.create_saved_group_widgets(group_dir)

    # Работа с буфером обмена
    def work_with_clipboard(self, key):
        if self.paths_input.get('0.0', END).rstrip('\n') == \
           self.start_text['paths_input']:
            self.paths_input.delete('0.0', END)
            self.paths_input.config(fg='white')

        if key.char == '\x16':
            self.paths_input.insert('0.0', pyperclip.paste())

    # Получить имя из пути
    def get_name_from_path(self, path):
        for elem in self.info_content:
            if path == elem['path'] and elem['type'] == 'file':
                return path.split("\\")[-1] 
        return path


class Path_internal_realization():
    # Поиск запущенного процесса
    def search_running_processes(self, path): 
        for proc in process_iter(['name']):
            if proc.info['name'] == self.get_name_from_path(path):
                return True
    
    # Распознавание и открытие пути
    def path_opening_realization(self, dict_path):
        if dict_path['type'] == 'url':
            webbrowser.open_new_tab(dict_path['path'])
        elif dict_path['type'] == 'dir':
            os.startfile(os.path.realpath(dict_path['path']))
        elif dict_path['type'] == 'file':
            if self.search_running_processes(dict_path['path']) != True:
                os.startfile(dict_path['path'])

    # Создание кнопок путей
    def creating_path_buttons(self, path):
        off_top, between = 24, 46
        y = self.get_dynamic_height_widget(
            'path', ('path_button', 'clear_path'),
            off_top, between
        )
        
        clear_button = self.widget_builder(Button, 'clear_path')
        clear_button.config(
            command=lambda: self.delete_content_via_button(
                'path', clear_button, off_top
            )
        )

        path_button = self.widget_builder(Button, 'path_button')
        path_button.config(
            command = lambda: self.open_path(path_button),
            text = self.get_name_from_path(path), anchor="w", borderwidth=0
        )

        self.info_buttons['path'].append(
            {'path_button': path_button,
             'clear_button': clear_button,
             'y': y}
        )

    # Обновление стартового сообщения
    def update_start_message(self):
        self.paths_input.delete('0.0', END)
        self.paths_input.config(fg='gray65')
        self.paths_input.insert('0.0', self.start_text['paths_input'])
    
    # Закрытие запущенного процесса
    def closing_running_process(self, name):
        {
            proc.kill() for proc in process_iter(['name'])
            if proc.info['name'] == name
        }


class Group_internal_realization():
    # Обновление поля путей
    def paths_field_update(self):
        {
            (dict['path_button'].destroy(),
             dict['clear_button'].destroy())
            for dict in self.info_buttons['path']
        }

        self.info_content.clear()
        self.info_buttons['path'].clear()

        with open(self.retention_dir,"r") as save_file:
            self.getting_content_info(save_file)
            self.creating_saved_content_widgets()
        
        self.resizing_program()

    # Замена файла сохранений
    def replacing_save_file(self, name_group):
        os.remove(self.retention_dir)
        
        copy(f'{self.group_dir}\\{name_group}\\retention.txt',\
             f'{self.base_dir}\\save')    
 
    # Удаление папки группы
    def deleting_group_folder(self, index_of_press):
        dict_button = self.info_buttons['group'][index_of_press]
        name_button = dict_button['group_button'].cget('text')
        
        with os.scandir(self.group_dir) as direct:
            {
                rmtree(f'{self.group_dir}\\{fold.name}') 
                for fold in direct if fold.name == name_button
            }

    # Сохраняем информацию о группах
    def save_info_about_groups(self, name_field):
        name_group = name_field.get('0.0', END).rstrip('\n')

        os.mkdir(f'{self.group_dir}\\{name_group}')
        copy(self.retention_dir, f'{self.group_dir}\\{name_group}')
                    
        return name_group

    # Cоздание кнопок групп
    def creating_group_buttons(self, name_group):
        off_top, between = 24, 46
        y = self.get_dynamic_height_widget(
            'group', ('group', 'clear_group'),
            off_top, between
        )
        
        clear_button = self.widget_builder(Button, 'clear_group')
        clear_button.config(
            command = lambda: self.delete_content_via_button(
                'group', clear_button, off_top
            )
        )
        
        group_button = self.widget_builder(Button, 'group')
        group_button.config(
            command = lambda: self.adding_group(name_group),
            text = name_group, borderwidth=0
        ) 

        self.info_buttons['group'].append(
            {'group_button': group_button,
             'clear_button': clear_button,
             'y': y}
        )