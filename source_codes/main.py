from additional_modules.GUI_builder import run_gui
import os

base_dir = os.getcwd()
x, y, w, h = 960, 540, 543, 317

if __name__ == '__main__':
    run_gui(x, y, w, h, base_dir)