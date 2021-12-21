from PyInstaller.__main__ import run
from shutil import copy, rmtree
import os


class Bilder():
    def __init__(self):
        self.auto_opener_dir = os.path.dirname(os.getcwd())
        self.source_codes_dir = os.getcwd()

        self.dict_dir = {\
            'img_dir_path': f'{self.auto_opener_dir}\\exe_file\\image',\
            'save_dir_path': f'{self.auto_opener_dir}\\exe_file\\save',\
            'shortcuts_dir_path': f'{self.auto_opener_dir}\\exe_file\\\shortcuts',\
            'group_dir_path': f'{self.auto_opener_dir}\\exe_file\\save\\group'}

    # Подготовка к запуску 
    def preparation_for_launch(self):
        try:    
            rmtree(f'{self.auto_opener_dir}\\exe_file')
            os.mkdir(f'{self.auto_opener_dir}\\exe_file')
        except FileNotFoundError:
            print(f'>>> Path not found: {self.auto_opener_dir}\\exe_file')
        except FileExistsError:
            print(f'>>> The file has already been created: {self.auto_opener_dir}\\exe_file')

    # Создание exe файла
    def create_exe_file(self):
        run(
            ['-F',
            '-w',
            f'--icon={self.source_codes_dir}\\image\\Auto-opener.ico',
            '--name=Auto-opener',
            f'--distpath={self.auto_opener_dir}\\exe_file',
            'main.py']
        )

    # Очистка следов
    def cleaning_up_traces(self):
        {rmtree(f'{os.getcwd()}\\{elem}')\
        for elem in os.listdir() if elem in ('dist', 'build')}
    
        {os.remove(f'{os.getcwd()}\\{elem}')\
        for elem in os.listdir() if elem[-4:] == 'spec'}\

    # Перемещение вспомогательных элементов  
    def moving_construction_elements(self):
        {os.mkdir(self.dict_dir[path]) for path in self.dict_dir}

        copy(f'{self.source_codes_dir}\\save\\save_path.txt',\
                 self.dict_dir['save_dir_path'])

        with os.scandir(f'{self.source_codes_dir}\\image') as img_dir,\
             open(f'{self.dict_dir["save_dir_path"]}\\save_path.txt', 'w') as save_file:
            
            save_file.write(f'buttons_len: 0')
            
            {copy(f'{self.source_codes_dir}\\image\\{img.name}',\
            self.dict_dir['img_dir_path']) for img in img_dir}

    # Сборка проекта
    def build_the_project(self):
        self.preparation_for_launch()
        self.create_exe_file()
        self.cleaning_up_traces()
        self.moving_construction_elements()

if __name__ == '__main__':
    Bilder().build_the_project()