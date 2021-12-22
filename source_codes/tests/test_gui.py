from tkinter import *
import traceback
import pytest
import os

from main import *
from additional_modules.GUI_builder import Builder_gui

class Test_constructor_gui():
    def test_run_gui(self):
        try:
            run_gui(x, y, w, os.path.dirname(base_dir))
        except TclError:
            print('Error')


