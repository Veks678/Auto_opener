from tkinter import *
import tkinter as tk

from .field_constructor import Text_fields
from ..logic.button_logic import Widget_logic


# Класс реализации кнопок
class Buttons():
    def __init__(self, frame_widgets, bg_widgets, fg_widgets, activebg_widgets,\
                 font_widgets, width_widgets, padx_widgets, pady_widgets, \
                 widget_type, label_widgets):
        # Парамметры виджетов
        self.frame_widgets = frame_widgets        # Фрейм
        self.bg_widgets = bg_widgets              # Цвет фона
        self.fg_widgets = fg_widgets              # Цвет шрифта
        self.activebg_widgets = activebg_widgets  # Цвет при наведении курсора
        self.font_widgets = font_widgets          # Тип и размер шрифта
        self.width_widgets = width_widgets        # Ширина
        self.padx_widgets = padx_widgets          # Отсутпы по горизонтали
        self.pady_widgets = pady_widgets          # Отсутпы по вертикали
        self.widget_type = widget_type            # Тип виджета
        self.label_widgets = label_widgets        # Метка виджета

        self.side_widgets = LEFT                  # Выравнивание виджета

    # Создаем кнопки
    def create_widget(self):
        self.Reusable_button = self.widget_type(self.frame_widgets, \
                                                text = self.label_widgets, \
                                                bg = self.bg_widgets, \
                                                fg = self.fg_widgets, \
                                                font = self.font_widgets, \
                                                width = self.width_widgets, \
                                                activebackground = \
                                                self.activebg_widgets, \
                                                command = \
                        Commands_widgets(self.label_widgets).command_button)

    def run_widget(self):
        self.Reusable_button.pack(side = self.side_widgets, \
                                  padx = self.padx_widgets, \
                                  pady = self.pady_widgets, \
                                  expand = True, fill = BOTH)


# Класс реализации вызова команд для кнопок
class Commands_widgets():
    def __init__(self, label_widgets):
        self.label_widgets = label_widgets

    def command_button(self):
        if self.label_widgets in 'Открыть':
            self.command_open()
        elif self.label_widgets in 'Закрыть':
            self.command_close()
        elif self.label_widgets in 'Добавить':
            self.command_append()
        elif self.label_widgets in 'Удалить':
            self.command_delete()
        elif self.label_widgets in 'Сохранить':
            self.command_save()

    def command_open(self):
        print('\nКнопка: Открыть')
        Widget_logic(None, None).open_path()

    def command_close(self):
        print('\nКнопка: Закрыть')
        Widget_logic(None, None).close()

    def command_append(self):
        print('\nКнопка: Добавить')
        self.menu_input = Text_fields.menu_field_list[1].get(1.0, END)
        Widget_logic(self.menu_input, None).add()

    def command_delete(self):
        print('\nКнопка: Удалить')
        self.menu_input = Text_fields.menu_field_list[1].get(1.0, END)
        self.menu_input_list = Text_fields.menu_field_list[0].get(0, END)
        Widget_logic(self.menu_input, self.menu_input_list).erase()

    def command_save(self):
        print('\nКнопка: Сохранить')
        Widget_logic(None, None).save()
