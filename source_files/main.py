from tkinter import *
import os

from additional_modules.GUI import Start_gui


def main(base_dir):
    Start_gui(base_dir, Tk()).run_gui()

if __name__ == '__main__':
    main(os.getcwd())