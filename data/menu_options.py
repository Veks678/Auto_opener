from tkinter import *
import tkinter as tk

from .constructor.window_constructor import Window
from .constructor.frame_constructor import Frames
from .constructor.field_constructor import Text_fields
from .constructor.button_constructor import Buttons


class Window_param:
    def __init__(self):
        self.frame_labels = ['One_line', 'Two_line']

        self.root_path = Window((False, False), '400',\
                                '250', 'Редактор пути').Create_path_window()

    def run_frame(self):
        for label in self.frame_labels:
            # Создание фреймов
            self.object_frame = Frames(self.root_path, 400, \
                                       29, 43, label)

            self.object_frame.create_frame()
            self.object_frame.run_frame()

        return self.root_path

class Widgets_param:
    def __init__(self, widgets_label, window_name):
        self.widgets_label = widgets_label
        self.window_name = window_name

        if self.widgets_label in 'Список':
            # Передаю параметры виджета
            self.Call_widget = Text_fields(None, self.window_name, "gray8",\
                                           "white", "Arial 10", 'RoyalBlue4',\
                                           100, 50, 2, 2, Listbox, \
                                           self.widgets_label, '')
        elif self.widgets_label in 'Ввод':
            # Передаю параметры виджета
            self.Call_widget = Text_fields(Frames.List_frames[0],None, \
                                           "gray8", "white", "Arial 10", \
                                           'RoyalBlue4', 50, None, 2, 2, \
                                           Text, self.widgets_label, '')
        else:
            # Передаю параметры виджета
            self.Call_widget = Buttons(Frames.List_frames[1], "RoyalBlue4", \
                                       "white", 'gray8', "Arial 14", \
                                       9, 3, 3, Button, self.widgets_label)


    def run_widget(self):
        self.Call_widget.create_widget()
        self.Call_widget.run_widget()
