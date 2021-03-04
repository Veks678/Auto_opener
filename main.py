from tkinter import *
import tkinter as tk

from data.main_options import Window_param, Frame_param, Widget_param


class Main:
    def __init__(self):
        self.frame_label = ['One_line', 'Two_line']
        self.widget_label = ['Меню','Инфо','Открыть','Закрыть']
        self.field_text = 'Список открываемых путей: \n'

        object_window = Window_param()

        for label in self.frame_label:
            Frame_param(label).run_frame()

        for label in self.widget_label:
            Widget_param(label, self.field_text).run_widget()

        object_window.run_window()


# Создаю главное окно со всем содержимым
if __name__ == '__main__':
    Main()
