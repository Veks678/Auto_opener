# Передача аргументов декоратору (декоратор для декоратора и для функции "Пиздос")

def decorator_arg(arg_three, arg_four):
    def decorator_func(func):
        def wrapping_function():
            print(f'start: {arg_three}')
            func()
            print(f'stop: {arg_four}')
        return wrapping_function
    return decorator_func
    
@decorator_arg(3, 4)
def func():
    print(f'content')

func()
