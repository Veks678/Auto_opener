from tkinter import *
import os

from additional_modules.GUI_builder import Builder_gui

base_dir = os.getcwd()
tk_param = {
    'title': '',
    'resizable': [False, False],
    'bg': "wheat4",
    'x': 689,
    'y': 269,
    'w': 543
}
toplevel_param = {
    'title': '',
    'resizable': [False, False],
    'bg': "wheat4",
    'x': 543,
    'y': 689,
    'w': 300,
    'h': 150
}

def main(base_dir):
    Builder_gui(base_dir, tk_param, toplevel_param, Tk()).run_gui()

if __name__ == '__main__':
    main(base_dir)