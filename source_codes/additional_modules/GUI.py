from tkinter import *

from PIL import ImageTk

from .Command import Command_logic
from .internal_realization import Displaying_saved_info, Scaling_the_GUI
from .config_gui import windows_param, arg_widgets


class Builder_gui(Command_logic): 
    def __init__(self):
        Command_logic.__init__(self)

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
            bg = self.arg_widgets[key]['bg'],
            fg = self.arg_widgets[key]['fg'],
            font = self.arg_widgets[key]['font']
        )

        # Отображение изображений нажатия
        if self.arg_widgets[key]['key'] != False:
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
            
        widget.pack_propagate(False)
        widget.pack(expand=True, fill=BOTH)
        self.packaging_widgets(widget, key)

        return widget

    # Упаковка виджетов
    def packaging_widgets(self, widget, key):
        widget.place(
            x = self.arg_widgets[key]['x'],
            y = self.arg_widgets[key]['y'],
            height = self.arg_widgets[key]['h'],
            width = self.arg_widgets[key]['w'],
        )


class Start_gui(Frame, Builder_gui, Scaling_the_GUI, Displaying_saved_info):
    def __init__(self, base_dir, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        Builder_gui.__init__(self)
        Scaling_the_GUI.__init__(self)

        self.base_dir = base_dir
        
        self.arg_widgets = arg_widgets
        self.windows_param = windows_param

        self.info_buttons = {'path': [], 'group': []}
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

        self.set_height_of_dynamic_widgets(self.start_height)
        self.widgets_creating()

        main_window.protocol("WM_DELETE_WINDOW", lambda: self.save_content(True))
        main_window.iconbitmap(f'{self.base_dir}\\image\\Auto-opener.ico')
        self.mainloop()


