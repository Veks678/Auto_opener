from tkinter import *

from PIL import ImageTk

from .GUI_logic import Path_logic, Group_logic
from .internal_realization import GUI_realization_logic


class Builder_gui(Frame, Path_logic, Group_logic, GUI_realization_logic):
    
    def __init__(self, base_dir, windows_param, *args, **kwargs):
        GUI_realization_logic.__init__(self)
        Frame.__init__(self, *args, **kwargs)
        Path_logic.__init__(self)

        self.info_content = []
        self.info_buttons = {'path': [], 'group': []}
        
        self.base_dir = base_dir
        self.windows_param = windows_param
        
        self.config_dir = f'{self.base_dir}\\additional_modules\\config_gui.txt'
        self.retention_dir = f'{self.base_dir}\\save\\retention.txt'
        self.group_dir = f'{self.base_dir}\\save\\group'
        self.img_dir = f'{self.base_dir}\\image\\'
        
        self.name_image = [
            'adding','adding_group','adding_push','cancel','clear',
            'clear_push','close_path','create_group',
            'open_path','save_all','save_all_push'
        ]
        
        self.img_paths = {
            name: f'{self.img_dir}{name}.png'
            for name in self.name_image
        }

    # Создание окна
    def windows_builder(self, window, param):
        window.attributes("-topmost", True)
        window.title(param['title'])
        
        self.set_window_geometry(window, param)
        window.resizable(param["resizable"][0], param["resizable"][1])
        window["bg"] = param["bg"]

        return window

    # Создание виджетов
    def widget_builder(self, TYPE, key):
        widget = TYPE(
            self.windows[self.arg_widgets[key]['windows']],
            bg=self.arg_widgets[key]['bg'],
            fg=self.arg_widgets[key]['fg'],
            font=self.arg_widgets[key]['font']
        )

        # Отображение изображений нажатия
        self.displaying_click_images(widget, key)
            
        widget.pack_propagate(False)
        widget.pack(expand=True, fill=BOTH)
        self.packaging_widgets(widget, key)

        return widget

    # Запуск виджетов
    def widgets_creating(self):
        self.start_text = {
            'paths_input': 'Введите путь или url-адресс',
            'group_name': 'Введите имя группы'
        }
        self.img_icon = {
            elem: ImageTk.PhotoImage(file=self.img_paths[elem])\
            for elem in self.img_paths
        }
        
        # VoxReguar
        #---------------------------------------------------------------------
        self.paths_field_bg = self.widget_builder(Label, 'paths_field_bg')
        #---------------------------------------------------------------------
        self.paths_input = self.widget_builder(Text, 'paths_input')
        self.paths_input.insert('0.0', self.start_text['paths_input'])
        self.paths_input.bind(
            "<Key>", lambda key: self.work_with_clipboard(key)
        )
        self.paths_input.config(borderwidth=0)
        #---------------------------------------------------------------------
        save_all = self.widget_builder(Button, 'save_all')
        save_all.config(command=lambda: self.save_content())
        #---------------------------------------------------------------------
        self.add_path = self.widget_builder(Button, 'add_path')
        self.add_path.config(command=lambda: self.adding_path())
        #---------------------------------------------------------------------
        open_path = self.widget_builder(Button, 'open_path')
        open_path.config(command=lambda: self.open_path())
        #---------------------------------------------------------------------
        close_path = self.widget_builder(Button, 'close_path')
        close_path.config(command=lambda: self.close_path())
        #---------------------------------------------------------------------
        create_group = self.widget_builder(Button, 'create_group')
        create_group.config(command = lambda: self.run_name_window())
        #---------------------------------------------------------------------
        self.create_group_bg = self.widget_builder(Label, 'create_group_bg')
        #---------------------------------------------------------------------
        self.display_content()

    # Запуск приложения
    def run_gui(self):
        len_content = self.start_length_content()
        self.start_height = self.get_dynamic_height_window(len_content)
        self.windows_param['main']['h'] = self.start_height
        
        main_window = self.windows_builder(
            self.master, self.windows_param['main']
        )
        self.windows = {'main': main_window}

        self.reading_configuration_file()
        self.set_height_of_dynamic_widgets(self.start_height)
        self.widgets_creating()

        main_window.protocol("WM_DELETE_WINDOW", lambda: self.save_content(True))
        main_window.iconbitmap(f'{self.base_dir}\\image\\Auto-opener.ico')
        self.mainloop()


