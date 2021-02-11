from tkinter import *
import tkinter as tk
import os


# Класс реализации полей текста
class Text_fields():
    # Список сохраненых путей
    save_file = open('PATH.txt', 'r')
    saved_list = [elem.rstrip('\n') for elem \
                  in save_file.readlines()]

    # Список виджетов текста
    main_field_list = []
    menu_field_list = []

    def __init__(self, frame_widgets, window_name, bg_widgets, fg_widgets, \
                 font_widgets, selectbg, width_widgets, height_widgets, \
                 padx_widgets, pady_widgets, widget_type, label_widgets, \
                 text_widgets):
        # Парамметры виджетов
        self.frame_widgets = frame_widgets            # Фрейм
        self.window_name = window_name                # Родительское окно
        self.bg_widgets = bg_widgets                  # Цвет фона
        self.fg_widgets = fg_widgets                  # Цвет шрифта
        self.font_widgets = font_widgets              # Тип и размер шрифта
        self.selectbg = selectbg                      # Цвет выделения
        self.width_widgets = width_widgets            # Ширина
        self.height_widgets = height_widgets          # Высота
        self.padx_widgets = padx_widgets              # Отсутпы по горизонтали
        self.pady_widgets = pady_widgets              # Отсутпы по вертикали
        self.widget_type = widget_type                # Тип виджета
        self.label_widgets = label_widgets            # Метка виджета
        self.text_widgets = text_widgets              # Текст виджета

        self.side_widgets = LEFT                      # Выравнивание виджета

    # Создание полей
    def create_widget(self):
        # Блокировка ввода в текстовое поле
        def check_keys(event):
            if event:
                return "break"

        if self.label_widgets in 'Список':
            self.side_widgets = TOP
        elif self.label_widgets in ('Текст', 'Ввод'):
            self.window_name = self.frame_widgets

        self.Reusable_Text = self.widget_type(self.window_name, \
                                         bg = self.bg_widgets, \
                                         fg = self.fg_widgets, \
                                         font = self.font_widgets, \
                                         width = self.width_widgets, \
                                         selectbackground = self.selectbg)

        if self.label_widgets in 'Текст':
            self.Reusable_Text.bind("<Key>", check_keys)

    def run_widget(self):
        self.Reusable_Text.pack(padx = self.padx_widgets, \
                                pady = self.pady_widgets)

        if self.label_widgets in 'Текст':
            self.main_field_list.append(self.Reusable_Text)
            self.main_field_list[0].insert('1.0', self.text_widgets)

            index, num = 2.0, 1
            for path in self.saved_list:
                self.main_field_list[0].insert(str(index), '['+str(num)\
                                               +']:  ' +path+'\n')
                index += 1.0
                num += 1


        elif self.label_widgets in ('Список', 'Ввод'):
            if len(self.menu_field_list) < 2:
                self.menu_field_list.append(self.Reusable_Text)
            else:
                del self.menu_field_list[:]
                self.menu_field_list.append(self.Reusable_Text)

            if self.label_widgets in 'Список' and \
               len(self.saved_list) > 0:
                for elem in self.saved_list:
                    Text_fields.menu_field_list[0].insert(END, elem)
