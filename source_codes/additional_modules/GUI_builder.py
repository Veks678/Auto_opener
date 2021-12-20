from tkinter import *

from PIL import ImageTk

from .GUI_logic import Path_logic, Group_logic
from .internal_realization import GUI_realization_logic


class Constructor_gui(Frame, Path_logic, Group_logic, GUI_realization_logic):
    
    def __init__(self, base_dir, *args, **kwargs):
        GUI_realization_logic.__init__(self)
        Frame.__init__(self, *args, **kwargs)
        Path_logic.__init__(self)

        self.info_programm, self.info_path, self.info_group = dict(), dict(), dict()

        self.base_dir = base_dir
        self.config_path = f'{self.base_dir}\\additional_modules\\config_gui.txt'
        self.save_path = f'{self.base_dir}\\save\\save_path.txt'
        self.shortcuts_path = f'{self.base_dir}\\shortcuts'
        self.group_path = f'{self.base_dir}\\save\\group'
        self.img_path_dir = f'{self.base_dir}\\image\\'
        
        self.name_image = [
            'adding','adding_group','adding_push','cancel','clear',
            'clear_push','close_path','create_group',
            'open_path','save_all','save_all_push'
        ]
        
        self.img_paths = {
            name: f'{self.img_path_dir}{name}.png'
            for name in self.name_image
        }

    # Создание окна
    def windows_constructor(self, title, geo, resizable, bg, window):
        window.attributes("-topmost", True)
        window.title(title)
        window.geometry(f'{geo[0]}x{geo[1]}+{geo[2]}+{geo[3]}')
        window.resizable(resizable[0], resizable[1])
        window["bg"] = bg

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
        widget.place(
            x=self.arg_widgets[key]['x'],
            y=self.arg_widgets[key]['y'],
            height=self.arg_widgets[key]['h'],
            width=self.arg_widgets[key]['w'],
        )

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
        self.widget_builder(Label, 'paths_field_bg')
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
        add_path = self.widget_builder(Button, 'add_path')
        add_path.config(command=lambda: self.adding_path())
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
        self.widget_builder(Label, 'create_group_bg')
        #---------------------------------------------------------------------
        self.opening_starter_content()

    # Рестарт преложения
    def restart(self, x, y, w):
        run_gui(x, y, w, self.base_dir)

# Запуск приложения
def run_gui(x, y, w, base_dir):
    GUI = Constructor_gui(base_dir, Tk())
    GUI.reading_configuration_file()

    height = GUI.get_dynamic_height_window(GUI.starting_length_path_field())
    
    main_window = GUI.windows_constructor(
        '', [w, height, x, y], [False, False], "wheat4", GUI.master
    )
    GUI.windows = {'main': main_window}

    GUI.changing_position_widgets(height)
    GUI.widgets_creating()
    
    main_window.protocol("WM_DELETE_WINDOW", lambda: GUI.save_content(True))
    main_window.iconbitmap(f'{base_dir}\\image\\Auto-opener.ico')
    GUI.mainloop()


