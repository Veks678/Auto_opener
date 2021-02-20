from tkinter import *
import tkinter as tk

import os
import pyperclip


# Класс реализации полей текста
class Text_fields():
    # Список виджетов текста
    main_field_list = []
    menu_field_list = []

    # Выделенный элемент списка
    selected_list_item = []

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
        # Получения индекса елемента в списке
        def Get(event):
            if len(self.selected_list_item) == 0:
                self.selected_list_item.append(str(event.widget.curselection()))
            else:
                del self.selected_list_item[0]
                self.selected_list_item.append(str(event.widget.curselection()))

            for elem in self.selected_list_item[0]:
                if elem in ('(',')',','):
                    self.selected_list_item[0] = \
                    self.selected_list_item[0].replace(elem, '')

        # Блокировка ввода в текстовое поле
        def check_keys(event):
            if self.label_widgets in 'Ввод':
                if event.state == 4 and event.keycode == 86:
                    self.menu_field_list[1].insert(END, pyperclip.paste())
            elif self.label_widgets in 'Текст':
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

        if self.label_widgets in ('Текст', 'Ввод'):
            self.Reusable_Text.bind("<Key>", check_keys)
        if self.label_widgets in ('Список'):
            self.Reusable_Text.bind("<<ListboxSelect>>", Get)

    def run_widget(self):
        self.Reusable_Text.pack(padx = self.padx_widgets, \
                                pady = self.pady_widgets, \
                                expand = True, fill = BOTH)

        if self.label_widgets in 'Текст':
            self.main_field_list.append(self.Reusable_Text)
            self.main_field_list[0].insert('1.0', self.text_widgets)

            index, num = 2.0, 1
            for elem in open('PATH.txt', 'r').readlines():
                if len(elem) > 42:
                    elem = elem[0:41]
                self.main_field_list[0].insert(str(index), '['+str(num)\
                                               +']:  ' +elem+'\n')
                index += 1.0
                num += 1

        elif self.label_widgets in ('Список', 'Ввод'):
            if len(self.menu_field_list) < 2:
                self.menu_field_list.append(self.Reusable_Text)
            else:
                del self.menu_field_list[:]
                self.menu_field_list.append(self.Reusable_Text)

            if self.label_widgets in 'Список' and \
               len(open('PATH.txt', 'r').readlines()) > 0:
                for elem in open('PATH.txt', 'r').readlines():
                    Text_fields.menu_field_list[0].insert(END, elem)
            else:
                return
