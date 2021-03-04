from tkinter import *
import tkinter as tk

import subprocess
import webbrowser
import os
import time

from field_constructor import Text_fields

# Реализация логики клавиш
class Widget_logic():
    def __init__(self, menu_input, menu_input_list):
        self.menu_input = menu_input
        self.menu_input_list = menu_input_list

    # Кнопка [Открыть]
    def open_path(self):
        print(Text_fields.saved_list)
        for elem in Text_fields.saved_list:
            if '/' not in elem:
                program_process = subprocess.Popen(('start', elem), shell = True)
                time.sleep(0.5)
            elif '/' in elem:
                webbrowser.open(elem, new = 0)
                time.sleep(1)


    # Кнопка [Закрыть]
    def close(self):
        for elem in Text_fields.saved_list:
            if '/' not in elem:
                elem = list(reversed(elem))
                for i, e in enumerate(elem):
                    if '\\' in e:
                        elem = [e for e in reversed(elem[0:i])]
                        elem = ''.join(elem[0:])
                        break
                for i, e in enumerate(elem):
                    if '.' in e:
                        if 'exe' in elem[i+1:]:
                            subprocess.call("taskkill /F /IM "+ elem)
                        elif 'pdf' in elem[i+1:]:
                            subprocess.call("taskkill /F /IM PDFXCview.exe")
                        break


    # Кнопка [Добавить]
    def add(self):
        if len(Text_fields.selected_list_item) > 0:
            index = int(Text_fields.selected_list_item[0])
            Text_fields.menu_field_list[0].insert(index, self.menu_input)
            Text_fields.menu_field_list[1].delete(1.0, END)
            del Text_fields.selected_list_item[0]
        elif len(self.menu_input) > 1 and not \
           set([':','_','.','/']).isdisjoint(list(self.menu_input)):
            Text_fields.menu_field_list[0].insert(END, self.menu_input)
            Text_fields.menu_field_list[1].delete(1.0, END)
        else:
            return

    # Кнопка [Удалить]
    def erase(self):
        if len(Text_fields.selected_list_item) > 0:
            index = int(Text_fields.selected_list_item[0])
            Text_fields.menu_field_list[0].delete(index)
            del Text_fields.selected_list_item[0]

        elif len(self.menu_input_list) > 0:
            end_symbol = Text_fields.menu_field_list[0].get(END)
            end_symbol = end_symbol.rstrip('\n')
            Text_fields.menu_field_list[0].delete(END)
        else:
            return

    # Кнопка [Сохранить]
    def save(self):
        self.input_list = [elem.rstrip('\n') for elem in \
                          Text_fields.menu_field_list[0].get(0, END)]

        with open('PATH.txt', 'w') as self.file_path:
            for elem in self.input_list:
                self.file_path.write(elem + '\n')

        for elem in self.input_list.copy():
            if set([elem]).isdisjoint(Text_fields.saved_list):
                Text_fields.saved_list += [elem]

            while len(Text_fields.saved_list) > len(self.input_list):
                del Text_fields.saved_list[-1:]

        Text_fields.main_field_list[0].delete('2.0', END)
        index, num = 2.0, 1
        for elem in self.input_list.copy():
            if len(elem) > 42:
                elem = elem[0:41]

            Text_fields.main_field_list[0].insert(\
            str(index), '\n['+str(num)+']:  '+elem)
            index += 1.0
            num += 1

        return self.input_list
