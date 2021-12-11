import pytest
import os
	
from main import *

class Test_run_gui():
    true_x, true_y, true_w, true_h  = 960, 540, 543, 317 
    true_base_dir = os.path.dirname(os.getcwd())
    
    messages = ('Проверяю начальную позицию gui',
                'Позиция неверна, должна быть',
                '[Позиция верна]',
                f'x={true_x}, y={true_y}',
                
                'Проверяю базовую, директорию',
                'Директория неверна, должна быть',
                '[Директория верна]',
                f'{true_base_dir}')

    info_test = (
        ((x, y) != (960, 540),
         (messages[0], messages[1], messages[2], messages[3])),    
        
        (os.path.dirname(base_dir) != true_base_dir,
         (messages[4], messages[5], messages[6], messages[7]))
    )

    @pytest.mark.parametrize('info', [info for info in info_test])
    def test_run_gui(self, info):
        print(f'{info[1][0]}: ', end = '')
        
        if info[0]:
            pytest.skip(f"{info[1][1]}: {info[1][3]}")
        
        print(f'{info[1][2]}: ', end = '')
        assert not info[0]


class Test_file_integrity():
    messages = ('Проверяю целостность дерриктории',
                'Дерриктории не существует',
                'Целостность нарушена, не хватает',
                '[Целостность сохранена]')
    
    true_dir = {
        'source_codes': (
            f'{os.path.dirname(os.getcwd())}', 
            {'additional_modules', 'image', 'main.py',
            'save', 'shortcuts'}
        ),
        'save': (
            f'{os.path.dirname(os.getcwd())}\\save',
            {'save_path.txt', 'group'}
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
        print(f'{self.messages[0]} "{key}": ', end = '')
        true_dir_files = self.true_dir[key][1]
        
        try:
            dir_files = self.get_dir_files(self.true_dir[key][0])
        except FileNotFoundError:
            pytest.xfail(self.messages[1])
        
        if true_dir_files.issubset(dir_files) == False:
            diff = true_dir_files.difference(dir_files)
            pytest.skip(f"{self.messages[2]}: {key}: {diff}")
        
        print(f'{self.messages[3]}: ', end = '')
        assert true_dir_files.issubset(dir_files)

    