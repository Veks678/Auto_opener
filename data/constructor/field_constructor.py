from tkinter import *
import tkinter as tk

import os
import pyperclip
from pathlib import Path


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
        if self.label_widgets in 'Список':
            self.side_widgets = TOP
        elif self.label_widgets in ('Инфо', 'Ввод'):
            self.window_name = self.frame_widgets

        self.Reusable_Text = self.widget_type(self.window_name, \
                                         bg = self.bg_widgets, \
                                         fg = self.fg_widgets, \
                                         font = self.font_widgets, \
                                         width = self.width_widgets, \
                                         selectbackground = self.selectbg)

        self.checking_press()

    def run_widget(self):
        self.Reusable_Text.pack(padx = self.padx_widgets, \
                                pady = self.pady_widgets, \
                                expand = True, fill = BOTH)

        self.updating_widgets()

    # Обновление информации в полях текста
    def updating_widgets(self):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent

        if self.label_widgets in 'Инфо':
            self.main_field_list.append(self.Reusable_Text)
            self.main_field_list[0].insert('1.0', self.text_widgets)

            # Ввод начального текста в поле 'Инфо'
            index, num = 2.0, 1
            for elem in open(f'{BASE_DIR}\\PATH.txt', 'r').readlines():
                if len(elem) > 42:
                    elem = elem[0:41]
                self.main_field_list[0].insert(str(index), '['+str(num)\
                                               +']:  ' +elem+'\n')
                index += 1.0
                num += 1

        elif self.label_widgets in ('Список', 'Ввод'):
            if len(self.menu_field_list) == 2:
                del self.menu_field_list[:]
                self.menu_field_list.append(self.Reusable_Text)
            else:
                self.menu_field_list.append(self.Reusable_Text)

            # Ввод начального текста в поле 'Список', 'Ввод'
            if self.label_widgets in 'Список' and \
               len(open(f'{BASE_DIR}\\PATH.txt', 'r').readlines()) > 0:
                for elem in open(f'{BASE_DIR}\\PATH.txt', 'r').readlines():
                    Text_fields.menu_field_list[0].insert(END, elem)
            else:
                return

    # Функция обработки нажатий, на поля текста
    def checking_press(self):
        # Получения индекса елемента в списке
        def Get(event):
            if len(event.widget.curselection()) != 0:
                del self.selected_list_item[:]
                self.selected_list_item.append(str(event.widget.curselection()))
                for elem in self.selected_list_item[0]:
                    if elem in ('(',')',','):
                        self.selected_list_item[0] = \
                        self.selected_list_item[0].replace(elem, '')
            else:
                return
        # Блокировка ввода в текстовое поле
        def check_keys(event):
            if self.label_widgets in 'Ввод':
                if event.state == 4 and event.keycode == 86:
                    self.menu_field_list[1].insert(END, pyperclip.paste())
            elif self.label_widgets in 'Инфо':
                if event:
                    return "break"

        if self.label_widgets in ('Инфо', 'Ввод'):
            self.Reusable_Text.bind("<Key>", check_keys)
        if self.label_widgets in ('Список'):
            self.Reusable_Text.bind("<<ListboxSelect>>", Get)
