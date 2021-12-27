correct_dynamic_height_windows = {
    tuple(range(0,11)): 315,
    tuple(range(11,15)): 411,
    tuple(range(15,19)): 507,
    tuple(range(19,23)): 603,
    tuple(range(23,27)): 700,
}

correct_dynamic_height_widgets = {
    315: {
        'paths_field_bg': ('h', 241),
        'create_group_bg': ('h', 266),
        'paths_input': ('y', 289),
        'add_path': ('y', 289)
    },
    411: {
        'paths_field_bg': ('h', 337),
        'create_group_bg': ('h', 362),
        'paths_input': ('y', 385),
        'add_path': ('y', 385)
    },
    507: {
        'paths_field_bg': ('h', 433),
        'create_group_bg': ('h', 458),
        'paths_input': ('y', 481),
        'add_path': ('y', 481) 
    },
    603: {
        'paths_field_bg': ('h', 529),
        'create_group_bg': ('h', 554),
        'paths_input': ('y', 578),
        'add_path': ('y', 578)
    },
    700: {
        'paths_field_bg': ('h', 625),
        'create_group_bg': ('h', 651),
        'paths_input': ('y', 674),
        'add_path': ('y', 674)
    }
}

correct_windows_param = {
        'main': {
            'resizable': [False, False],
            'x': 689, 'y': 269, 'w': 543, 'h': 0
        },
        'group': {
            'resizable': [False, False],
            'x': 543, 'y': 689, 'w': 300, 'h': 150
        }
    }

correct_arg_widgets = {
        'paths_field_bg': {
            'key': False, 'windows': 'main', 
            'x': 2, 'y': 46, 'h': 0, 'w': 388
        }, 
        'paths_input': {
            'key': False, 'windows': 'main',
            'x': 27, 'y': 0, 'h': 23, 'w': 363
        },
        'save_all': {
            'key': ['save_all','save_all_push'], 'windows': 'main',
            'x': 350, 'y': 3, 'h': 40, 'w': 40
        },
        'add_path': {
            'key': ['adding', 'adding_push'], 'windows': 'main',
            'x': 2, 'y': 0, 'h': 23, 'w': 23
        },
        'open_path': {
            'key': ['open_path'], 'windows': 'main',
            'x': 2, 'y': 3, 'h': 40, 'w': 172
        },
        'close_path': {
            'key': ['close_path'], 'windows': 'main',
            'x': 176, 'y': 3, 'h': 40, 'w': 172
        },
        'create_group': {
            'key': ['create_group'], 'windows': 'main',
            'x': 393, 'y': 3, 'h': 40, 'w': 148
        },
        'create_group_bg': {
            'key': False, 'windows': 'main',
            'x': 393, 'y': 46, 'h': 0, 'w': 148
        },
        'path_button': {
            'key': False, 'windows': 'main',
            'x': 3, 'y': 0, 'h': 23, 'w': 363
        },
        'clear_path': {
            'key': ['clear','clear_push'], 'windows': 'main',
            'x': 367, 'y': 0, 'h': 23, 'w': 23
        },
        'clear_group': {
            'key': ['clear','clear_push'], 'windows': 'main',
            'x': 518, 'y': 0, 'h': 23, 'w': 23
        },
        'group': {
            'key': False, 'windows': 'main',
            'x': 394, 'y': 0, 'h': 23, 'w': 123
        },
        'name_field_bg': {
            'key': False, 'windows': 'group',
            'x': 5, 'y': 5, 'h': 95, 'w': 290
        },
        'name_field': {
            'key': False, 'windows': 'group',
            'x': 40, 'y': 40, 'h': 25, 'w': 220
        },
        'add_group': {
            'key': ['adding_group'], 'windows': 'group',
            'x': 5, 'y': 105, 'h': 40, 'w': 142
        },
        'cancel': {
            'key': ['cancel'], 'windows': 'group',
            'x': 153, 'y': 105, 'h': 40, 'w': 142
        }
    }