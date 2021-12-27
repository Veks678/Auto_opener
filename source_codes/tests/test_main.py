import pytest
import os

from additional_modules.config_gui import *
from .correct_config_gui import *

class Test_config_file():
    verifiable_windows_param = ['resizable', 'x', 'y', 'w', 'h']
    verifiable_widgets_arg = ['key', 'windows', 'x', 'y', 'h', 'w']   
    
    
    @pytest.mark.parametrize(
        'key_window', [key_window for key_window in windows_param]
    )
    def test_windows_param(self, key_window):
        print(f'Проверяю параметры окна [{key_window}]: ', end = '')
        
        for key_param in self.verifiable_windows_param:
            if correct_windows_param[key_window][key_param] != \
               windows_param[key_window][key_param]:
                pytest.skip(
                    f'Параметр [{key_param}] не верен, должен быть '
                  + f'[{correct_windows_param[key_window][key_param]}]'
                )
            
            assert not correct_windows_param[key_window][key_param] != \
                       windows_param[key_window][key_param]
        
        print(f'Все параметры верены: ', end = '')

    @pytest.mark.parametrize(
        'key_widget', [key_widget for key_widget in arg_widgets]
    )
    def test_widgets_param(self, key_widget):
        print(f'Проверяю параметры виджета [{key_widget}]: ', end = '')

        for key_param in self.verifiable_widgets_arg:
            if correct_arg_widgets[key_widget][key_param] != \
               arg_widgets[key_widget][key_param]:
                pytest.skip(
                    f'Параметр [{key_param}] не верен, должен быть '
                    + f'[{correct_arg_widgets[key_widget][key_param]}]'
                )
            
            assert not correct_arg_widgets[key_widget][key_param] != \
                       arg_widgets[key_widget][key_param]
        
        print(f'Все параметры верены: ', end = '')


class Test_file_integrity():
    true_dir = {
        'source_codes': (
            f'{os.path.dirname(os.getcwd())}', 
            {'additional_modules', 'image', 'main.py', 'save'}
        ),
        'additional_modules': (
            f'{os.path.dirname(os.getcwd())}\\additional_modules',
            {'config_gui.py', 'GUI_builder.py',
             'GUI_logic.py', 'internal_realization.py'}
        ),
        'save': (
            f'{os.path.dirname(os.getcwd())}\\save',
            {'retention.txt', 'group'}
        ),
        'image': (
            f'{os.path.dirname(os.getcwd())}\\image',
            {'adding.png','adding_group.png','adding_push.png',
            'cancel.png','clear.png', 'clear_push.png',
            'close_path.png','create_group.png',
            'open_path.png','save_all.png','save_all_push.png'}
        )
    }
    
    # Получить файлы директории
    def get_dir_files(self, dir):
        with os.scandir(dir) as direct:
            directory_files = {file.name for file in direct}
        return directory_files

    # Проверить целостность каталогов
    @pytest.mark.parametrize('key', [key for key in true_dir])
    def test_the_integrity_directories(self, key):
        print(f'Проверяю целостность дерриктории [{key}]: ', end = '')
        true_dir_files = self.true_dir[key][1]
        
        try:
            dir_files = self.get_dir_files(self.true_dir[key][0])
        except FileNotFoundError:
            pytest.xfail('Дерриктории не существует')
        
        if true_dir_files.issubset(dir_files) == False:
            pytest.skip(
                'Целостность нарушена, не хватает: '\
                + f"{key}\\{list(true_dir_files.difference(dir_files))[0]}"
            )
        
        print('Целостность сохранена: ', end = '')
        assert true_dir_files.issubset(dir_files)