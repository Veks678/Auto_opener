FONT = 'Arial 10 bold'

windows = {}
arg_widgets = {
    'paths_field': {
        'bg': "gray8", 'fg': "white", 'font': 'Arial 10',
        'key': False, 'windows': 'main',
        'x': 2, 'y': 46, 'h': 243, 'w': 388
    },
    'paths_input': {
        'bg': "gray8", 'fg': "gray65", 'font': FONT,
        'key': False, 'windows': 'main',
        'x': 27, 'y': 291, 'h': 23, 'w': 363
    },
    'save_all': {
        'bg': "gray30", 'fg': "white", 'font': FONT,
        'key': ('save_all', 'save_all_push'), 'windows': 'main',
        'x': 350, 'y': 3, 'h': 40, 'w': 40
    },
    'add_path': {
        'bg': "gray35", 'fg': "white", 'font': FONT,
        'key': ('adding', 'adding_push'), 'windows': 'main',
        'x': 2, 'y': 291, 'h': 23, 'w': 23
    },
    'open_path': {
        'bg': "gray30", 'fg': "white", 'font': FONT,
        'key': ['open_path'], 'windows': 'main',
        'x': 2, 'y': 3, 'h': 40, 'w': 172
    },
    'close_path': {
        'bg': "gray30", 'fg': "white", 'font': FONT,
        'key': ['close_path'], 'windows': 'main',
        'x': 176, 'y': 3, 'h': 40, 'w': 172
    },
    'create_group': {
        'bg': "gray30", 'fg': "white", 'font': FONT,
        'key': ['create_group'], 'windows': 'main',
        'x': 393, 'y': 3, 'h': 40, 'w': 148
    },
    'create_group_bg': {
        'bg': "gray10", 'fg': "black", 'font': 'Arial 10',
        'key': False, 'windows': 'main',
        'x': 393, 'y': 47, 'h': 267, 'w': 148
    },
    'clear_path': {
        'bg': "gray25", 'fg': "white", 'font': 'Arial 10 bold',
        'key': ('clear','clear_push'), 'windows': 'main',
        'x': 369, 'h': 20, 'w': 20
    },
    'clear_group': {
        'bg': "gray25", 'fg': "white", 'font': FONT,
        'key': ('clear','clear_push'), 'windows': 'main',
        'x': 518, 'h': 22, 'w': 22
    },
    'group': {
        'bg': "gray25", 'fg': "white", 'font': 'Arial 8 bold',
        'key': False, 'windows': 'main',
        'x': 394, 'h': 22, 'w': 123
    },
    'name_group_bg': {
        'bg': "gray10", 'fg': "white", 'font': FONT,
        'key': False, 'windows': 'group',
        'x': 5, 'y': 5, 'h': 95, 'w': 290
    },
    'name_group': {
        'bg': "white", 'fg': "black", 'font': FONT,
        'key': False, 'windows': 'group',
        'x': 40, 'y': 40, 'h': 25, 'w': 220
    },
    'add_group': {
        'bg': "gray30", 'fg': "white", 'font': FONT,
        'key': ['adding_group'], 'windows': 'group',
        'x': 5, 'y': 105, 'h': 40, 'w': 142
    },
    'cancel': {
        'bg': "gray30", 'fg': "white", 'font': FONT,
        'key': ['cancel'], 'windows': 'group',
        'x': 153, 'y': 105, 'h': 40, 'w': 142
    }
}