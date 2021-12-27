dynamic_window_height_values = [315, 411, 507, 603, 700]

dynamic_height_window = {
    tuple(range(values[0], values[1])): dynamic_window_height_values[index]
    for index, values in enumerate([(0,11),(11,15),(15,19),(19,23),(23,27)])
}

dynamic_widgets_value = [241, 266, 289, 289]
dynamic_widgets_key = [
    'paths_field_bg', 'create_group_bg', 'paths_input', 'add_path'
]

def dynamic_height_widgets():
    return {
        value: {
            dynamic_widgets_key[i]: (key, 96*index+dynamic_widgets_value[i])
            for i, key in enumerate(['h','h','y','y'])
        }
        for index, value in enumerate(dynamic_window_height_values)
    }

windows_param = {
    'main': {
        'title': '', 'resizable': [False, False], 'bg': "wheat4",
        'x': 689, 'y': 269, 'w': 543, 'h': 0
    },
    'group': {
        'title': '', 'resizable': [False, False], 'bg': "wheat4",
        'x': 543, 'y': 689, 'w': 300, 'h': 150
    }
}

arg_widgets = {
    'paths_field_bg': {
        'bg': 'gray8', 'fg': 'white', 'font': 'Arial 10', 
        'key': False, 'windows': 'main', 
        'x': 2, 'y': 46, 'h': 0, 'w': 388
    }, 
    'paths_input': {
        'bg': 'gray8', 'fg': 'gray65', 'font': 'Arial 10',
        'key': False, 'windows': 'main',
        'x': 27, 'y': 0, 'h': 23, 'w': 363
    },
    'save_all': {
        'bg': 'gray30', 'fg': 'white', 'font': 'Arial 10 bold',
        'key': ['save_all','save_all_push'], 'windows': 'main',
        'x': 350, 'y': 3, 'h': 40, 'w': 40
    },
    'add_path': {
        'bg': 'gray35', 'fg': 'white', 'font': 'Arial 10 bold',
        'key': ['adding', 'adding_push'], 'windows': 'main',
        'x': 2, 'y': 0, 'h': 23, 'w': 23
    },
    'open_path': {
        'bg': 'gray30', 'fg': 'white', 'font': 'Arial 10 bold',
        'key': ['open_path'], 'windows': 'main',
        'x': 2, 'y': 3, 'h': 40, 'w': 172
    },
    'close_path': {
        'bg': 'gray30', 'fg': 'white', 'font': 'Arial 10 bold',
        'key': ['close_path'], 'windows': 'main',
        'x': 176, 'y': 3, 'h': 40, 'w': 172
    },
    'create_group': {
        'bg': 'gray10', 'fg': 'white', 'font': 'Arial 10 bold',
        'key': ['create_group'], 'windows': 'main',
        'x': 393, 'y': 3, 'h': 40, 'w': 148
    },
    'create_group_bg': {
        'bg': 'gray30', 'fg': 'black', 'font': 'Arial 10',
        'key': False, 'windows': 'main',
        'x': 393, 'y': 46, 'h': 0, 'w': 148
    },
    'path_button': {
        'bg': 'gray25', 'fg': 'white', 'font': 'Arial 10',
        'key': False, 'windows': 'main',
        'x': 3, 'y': 0, 'h': 23, 'w': 363
    },
    'clear_path': {
        'bg': 'gray25', 'fg': 'white', 'font': 'Arial 10 bold',
        'key': ['clear','clear_push'], 'windows': 'main',
        'x': 367, 'y': 0, 'h': 23, 'w': 23
    },
    'clear_group': {
        'bg': 'gray10', 'fg': 'white', 'font': 'Arial 10 bold',
        'key': ['clear','clear_push'], 'windows': 'main',
        'x': 518, 'y': 0, 'h': 23, 'w': 23
    },
    'group': {
        'bg': 'gray10', 'fg': 'white', 'font': 'Arial 8 bold',
        'key': False, 'windows': 'main',
        'x': 394, 'y': 0, 'h': 23, 'w': 123
    },
    'name_field_bg': {
        'bg': 'gray10', 'fg': 'white', 'font': 'Arial 10 bold',
        'key': False, 'windows': 'group',
        'x': 5, 'y': 5, 'h': 95, 'w': 290
    },
    'name_field': {
        'bg': 'white', 'fg': 'black', 'font': 'Arial 10 bold',
        'key': False, 'windows': 'group',
        'x': 40, 'y': 40, 'h': 25, 'w': 220
    },
    'add_group': {
        'bg': 'gray30', 'fg': 'white', 'font': 'Arial 10 bold',
        'key': ['adding_group'], 'windows': 'group',
        'x': 5, 'y': 105, 'h': 40, 'w': 142
    },
    'cancel': {
        'bg': 'gray30', 'fg': 'white', 'font': 'Arial 10 bold',
        'key': ['cancel'], 'windows': 'group',
        'x': 153, 'y': 105, 'h': 40, 'w': 142
    }
}
