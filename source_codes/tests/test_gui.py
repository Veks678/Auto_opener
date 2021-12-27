from tkinter import *
import pytest
import os

from main import *
from additional_modules.GUI_builder import Builder_gui


class Test_builder_gui():
    def test_init_builder_gui(self):
        object = Builder_gui(os.path.dirname(os.getcwd()), Tk())
        print(object.__dict__)
