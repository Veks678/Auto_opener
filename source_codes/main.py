from tkinter import *
import os

from additional_modules.GUI_builder import Builder_gui


def main(base_dir):
    Builder_gui(base_dir, Tk()).run_gui()

if __name__ == '__main__':
    main(os.getcwd())