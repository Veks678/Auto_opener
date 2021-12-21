from additional_modules.GUI_builder import run_gui
import os


base_dir = os.getcwd()
x, y, w = 689, 269, 543

if __name__ == '__main__':
    run_gui(x, y, w, base_dir)