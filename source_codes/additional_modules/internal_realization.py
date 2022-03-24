from tkinter import *
import os

from shutil import copy, rmtree
from psutil import process_iter
import webbrowser

from .config_gui import dynamic_widgets_key, dynamic_height_window,\
                        dynamic_height_widgets


# Масштабирование графического интерфейса
class Scaling_the_GUI():
    def __init__(self):
        self.dynamic_widgets_key = dynamic_widgets_key
        self.dynamic_height_window = dynamic_height_window
        self.dynamic_height_widgets = dynamic_height_widgets()

    # Получить динамическую высоту окна
    def get_dynamic_height_window(self, path_field_length):
        height_range = [
            height_range for height_range in self.dynamic_height_window
            if path_field_length in height_range
        ][0]

        return self.dynamic_height_window[height_range]

    # Задать геометрию окна
    def set_window_geometry(self, window, param):
        window.geometry(
            f'{param["w"]}x' + f'{param["h"]}+' +\
            f'{param["x"]}+' + f'{param["y"]}'
        ) 
    
    # Установить высоту виджетов 
    def set_height_of_dynamic_widgets(self, height):
        for key in self.dynamic_height_widgets[height]:
            key_arg = self.dynamic_height_widgets[height][key]
            self.arg_widgets[key][key_arg[0]] = key_arg[1]
    
    # Изменить динамические виджеты
    def change_dynamic_widgets(self):
        dynamic_widgets = [
            self.paths_field_bg, self.create_group_bg,
            self.paths_input, self.add_path
        ]
        for index, widget in enumerate(dynamic_widgets):
            widget.place_forget()
            self.packaging_widgets(widget, self.dynamic_widgets_key[index])
    
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


# Получить стартовый контент
class Get_Starter_Content():
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

    # Стартовая длина контента
    def start_length_content(self):
        with open(self.retention_dir,"r") as retention_file,\
             os.scandir(self.group_dir) as group_dir:
            
            self.getting_content_info(retention_file)

            return max(
                [len(self.info_content),
                 len([folder.name for folder in group_dir])]
            )


# Отображение сохраненной информации
class Displaying_saved_info(Get_Starter_Content):
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

    # Открытие контента
    def display_content(self):
        with open(self.retention_dir,"r") as retention_dir,\
             os.scandir(self.group_dir) as group_dir:

            self.getting_content_info(retention_dir)
            self.creating_saved_content_widgets()
            self.create_saved_group_widgets(group_dir)


# Удаление контента
class Delete_content():
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

    # Удаление папки группы
    def deleting_group_folder(self, index_of_press):
        dict_button = self.info_buttons['group'][index_of_press]
        name_button = dict_button['group_button'].cget('text')
        
        with os.scandir(self.group_dir) as direct:
            {
                rmtree(f'{self.group_dir}\\{fold.name}') 
                for fold in direct if fold.name == name_button
            }
    
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


# Окно группы
class Group_window():
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

    # Cоздание группы
    def group_creation(self, name_field):
        self.save_content()

        name_group = self.save_info_about_groups(name_field)
        self.creating_group_buttons(name_group)
        
        self.windows['group'].destroy()
        self.resizing_program()

     # Сохраняем информацию о группах
    def save_info_about_groups(self, name_field):
        name_group = name_field.get('0.0', END).rstrip('\n')

        os.mkdir(f'{self.group_dir}\\{name_group}')
        copy(self.retention_dir, f'{self.group_dir}\\{name_group}')
                    
        return name_group


# Выбор группы
class Group_selection():
    # Замена файла сохранений
    def replacing_save_file(self, name_group):
        os.remove(self.retention_dir)
        
        copy(f'{self.group_dir}\\{name_group}\\retention.txt',\
             f'{self.base_dir}\\save') 

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

    # Добавление группы
    def adding_group(self, name_group):
        with os.scandir(self.group_dir) as direct:
            {
                (self.replacing_save_file(name_group),
                 self.paths_field_update())
                 for folder in direct if folder.name == name_group
            }


# Кнопки контента
class Content_buttons(Group_selection):
    # Вычисление динамической высоты виджета
    def get_dynamic_height_widget(self, key_content, key_image, h, y):
        y = (h * (len(self.info_buttons[key_content])) + 1) + y
        for key in key_image:
            self.arg_widgets[key]['y'] = y

        return y    
    
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
            {
                'path_button': path_button,
                'clear_button': clear_button,
                'y': y
            }
        )
    
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
            {
                'group_button': group_button,
                'clear_button': clear_button,
                'y': y
            }
        )


# Открытие и закрытие контента
class Opening_and_closing_content():
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

    # Закрытие запущенного процесса
    def closing_running_process(self, name):
        {
            proc.kill() for proc in process_iter(['name'])
            if proc.info['name'] == name
        }

    # Получить имя из пути
    def get_name_from_path(self, path):
        for elem in self.info_content:
            if path == elem['path'] and elem['type'] == 'file':
                return path.split("\\")[-1] 
        return path
