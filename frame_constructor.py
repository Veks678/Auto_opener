from tkinter import *
import tkinter as tk


# Класс реализации фреймов
class Frames():
    # Лист фреймов
    List_frames = []

    def __init__(self, window_name, background_line, \
                 width_line, height_one_line, height_two_line, frame_label):
        self.window_name = window_name               # Имя окна
        self.background_line = background_line       # Задний фон
        self.width_line = width_line                 # Ширина линии
        self.height_one_line = height_one_line       # Высота первой линии
        self.height_two_line = height_two_line       # Высота третьей линии
        self.frame_label = frame_label               # Метка фрейма

        self.height_line = self.height_one_line      # Высота линии
        self.side_line = BOTTOM

    def create_frame(self):
        if self.frame_label in 'Two_line':
            self.height_line = self.height_two_line

        self.name_frame = Frame(self.window_name, \
                                background = self.background_line, \
                                width = self.width_line,
                                height = self.height_line)

    def run_frame(self):
        self.name_frame.pack(side = self.side_line)
        self.name_frame.pack_propagate(False)

        if len(self.List_frames) < 2:
            self.List_frames.append(self.name_frame)
        else:
            del self.List_frames[:]
            self.List_frames.append(self.name_frame)
