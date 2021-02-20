from tkinter import *
import tkinter as tk


class Window():
    # Инициализация главного окна приложения
    root_main = Tk()
    # Инициализируем меню
    menu_root = Menu()

    def __init__(self, resizable = (False, False), width = 500, \
                 height = 500, title = 'Window'):
        self.resizable = resizable
        self.width = width
        self.height = height
        self.title = title

    # Параметры главного окна
    def Create_main_window(self):
        # Заголовок окна
        self.root_main.title(self.title)
        # Размер окна
        self.root_main.geometry('{}x{}'.format(self.width, self.height))
        # Запрет пользователя на изменение рамеров окна
        self.root_main.resizable(self.resizable[0], self.resizable[1])

    # Запуска дочеренго окна и установка его параметров
    def Create_path_window(self):
        # Инициализация дочернего окна приложения
        self.root_path = Toplevel(self.root_main)
        self.root_path.title(self.title)
        self.root_path.geometry('{}x{}'.format(self.width, self.height))
        self.root_path.resizable(self.resizable[0], self.resizable[1])
        self.focus_window_path()
        return self.root_path

    # Блокировка фонового окна
    def focus_window_path(self):
        self.root_path.grab_set()

    # Запуска главного окна
    def Running_main_window(self):
        # Устновливаем меню для текущего окна
        self.root_main.config(menu = self.menu_root)
        # Реализация бесконечного цикла окна (работа окна)
        self.root_main.mainloop()
