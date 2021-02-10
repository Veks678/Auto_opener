from tkinter import *
import tkinter as tk

from main_window_options import Window_param, Frame_param, Widget_param


class Main:
    def __init__(self):
        self.frame_label = ['One_line', 'Two_line']
        self.button_label = ['Меню','Текст','Открыть','Закрыть']
        self.field_text = ''

        object_window = Window_param()

        for label in self.frame_label:
            Frame_param(label).run_frame()

        for label in self.button_label:
            Widget_param(label, self.field_text).run_widget()

        object_window.run_window()


# Создаю главное окно со всем содержимым
if __name__ == '__main__':
    Main()
