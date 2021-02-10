from tkinter import *
import tkinter as tk

from menu_window_options import Window_param, Widgets_param

# Класс реализации меню
class Submenu():
    def __init__(self, menu_root, bg_widgets, fg_widgets, active_bg_menu, \
                 font_widgets, width_widgets, widget_type, label_widgets):
        # Парамметры виджетов
        self.menu_root = menu_root                # Пренадлежность к окну
        self.bg_widgets = bg_widgets              # Цвет фона
        self.fg_widgets = fg_widgets              # Цвет шрифта
        self.active_bg_menu = active_bg_menu      # Цвет фона при нажатии
        self.font_widgets = font_widgets          # Тип и размер шрифта
        self.width_widgets = width_widgets        # Ширина
        self.widget_type = widget_type            # Тип виджета
        self.label_widgets = label_widgets        # Метка виджета

    # создаем меню
    def create_widget(self):
        self.Submenu = self.widget_type(bg = self.bg_widgets, \
                                        fg = self.fg_widgets, \
                                        font = self.font_widgets, \
                                        activeborderwidth = \
                                        self.width_widgets, \
                                        activebackground = \
                                        self.active_bg_menu, tearoff = 0)

        self.Submenu.add_command(label = "Редактировать пути", \
                                 command =  Commands_widgets().command_menu)

    # запускаем меню
    def run_widget(self):
        self.menu_root.add_cascade(label = "Настройки", menu = self.Submenu)


class Commands_widgets():
    def __init__(self):
        print('\nКнопка меню: Редактировать пути')

    def command_menu(self):
        # Метки виджетов
        self.widget_labels = ['Список', 'Ввод', 'Добавить', \
                              'Удалить', 'Сохранить']

        object_window = Window_param().run_frame()

        for label in self.widget_labels:
            Widgets_param(label, object_window).run_widget()
