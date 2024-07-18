import builtins
import io
import sys
import os
import pkgutil
import importlib


def print_divider():
    terminal_width = os.get_terminal_size().columns
    print('-' * terminal_width)


def list_all_modules():
    print_divider()
    print("Available modules:")
    for module_info in pkgutil.iter_modules():
        print(module_info.name)
    print_divider()
    print("Listing of modules finished.")


def print_module_function_help(module):
    for name in dir(module):
        obj = getattr(module, name)
        if callable(obj):
            print_divider()
            print('NEW FUNCTION')
            print_divider()
            print(f"Function: {name}")
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout
            try:
                help(obj)
            finally:
                sys.stdout = old_stdout
            help_output = new_stdout.getvalue()
            print(help_output)


def print_builtin_functions():
    print_divider()
    print("Built-in functions:")
    print_module_function_help(builtins)
    print_divider()
    print("Listing of built-in functions finished")


def main():
    while True:
        choice = input("Enter choice 1 = print every module / 2 = print built-in function info Y/N / 3 = Enter which modules you want info on. Input NOT case sensitive. / 4 = Quit: ").strip().lower()
        if choice == '1':
            list_all_modules()
        elif choice == '2':
            print_builtin_functions()
        elif choice == '3':
            user_input = input("Enter the module names separated by spaces: ").strip().lower()
            module_names = user_input.split()
            for module_name in module_names:
                try:
                    module = importlib.import_module(module_name) 
                    print(f"Information about module: {module_name}")
                    print_module_function_help(module)
                    print(f"Listing of {module_name} functions finished")
                except ImportError:
                    print(f"Module '{module_name}' was not found.")
        elif choice == '4':
            print("Quitting program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
