from tkinter import *
import tkinter as tk

from window_constructor import Window
from frame_constructor import Frames
from field_constructor import Text_fields
from button_constructor import Buttons
from submenu_constructor import Submenu

class Window_param:
    def __init__(self):
        self.Main_window = Window((False, False), '400', \
                                  '260', 'Автооткрыватор')
        self.Main_window.Create_main_window()

    def run_window(self):
        self.Main_window.Running_main_window()

class Frame_param:
    def __init__(self, frame_label):
        self.frame_label = frame_label

        # Создаем параметры фрейма
        self.Main_frames = Frames(Window.root_main, 'olivedrab', \
                                  400, 45, 220, self.frame_label)
    def run_frame(self):
        self.Main_frames.create_frame()
        self.Main_frames.run_frame()

class Widget_param:
    def __init__(self, widget_label, field_text):
        self.widget_label = widget_label
        self.field_text = field_text

        if self.widget_label in 'Текст':
            # Передаю параметры виджетов
            self.Call_widget = Text_fields(Frames.List_frames[1], None, \
                                           "gray8", "white", "Arial 10", \
                                           85, None, 2, 2, Text, \
                                           self.widget_label, \
                                           self.field_text)
        elif self.widget_label in 'Меню':
            # Передаю параметры виджетов
            self.Call_widget = Submenu(Window.menu_root, "#555", "white", \
                                       'olivedrab', "Arial 9", 1, Menu, \
                                       self.widget_label)

        elif self.widget_label in ('Открыть', 'Закрыть'):
            self.Call_widget = Buttons(Frames.List_frames[0], "#555", \
                                       "white", 'olivedrab', "Arial 15", \
                                       13, 2, 1,  Button, self.widget_label)


    def run_widget(self):
        self.Call_widget.create_widget()
        self.Call_widget.run_widget()
