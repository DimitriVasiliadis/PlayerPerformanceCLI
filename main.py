# this will hook everything together. this will handle the base ui which is the main menu that is dynamic based on the modules.
# it will also have base functionality for navigation to and from each modules data. additional functionality can be added in the specific module file for abstraction

import os
import keyboard
import sqlite3
from importlib import import_module

# Define the modules directory
MODULES_DIR = 'modules'

class CLIApplication:
    def __init__(self):
        self.modules = self.load_modules()

    def load_modules(self):
        """Dynamically load modules from the modules directory."""
        modules = []
        for file_name in os.listdir(MODULES_DIR):
            if file_name.endswith('.py') and file_name != '__init__.py':
                module_name = file_name[:-3]
                module = import_module(f'{MODULES_DIR}.{module_name}')
                modules.append({
                    'name': module_name.capitalize().replace('_', ' '),
                    'handler': getattr(module, f'{module_name.capitalize().replace("_", "")}Handler')
                })
        return modules

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_main_menu(self):
        self.clear_screen()
        print("╔═════════════════════════════════════════╗")
        print("║       Welcome to Valorant CLI Stats      ║")
        print("╠═════════════════════════════════════════╣")
        for idx, module in enumerate(self.modules, start=1):
            print(f"║  {idx}. {module['name']: <38} ║")
        print("║  0. Exit                                 ║")
        print("╚═════════════════════════════════════════╝")

    def navigate_to_menu(self, key):
        num_modules = len(self.modules)

        if key == '`':  # Backtick key mapped to main menu
            self.display_main_menu()
        elif key == '0':
            print("Exiting program. Goodbye!")
            return False  # Exit program
        elif key.isdigit() and 1 <= int(key) <= num_modules:
            self.clear_screen()
            module_index = int(key) - 1

            # call the display function for the given modules data

        else:
            print("Invalid input. Please enter a valid menu option.")

        return True  # Continue program execution

    def run(self):
        self.display_main_menu()

# add updating database here


        while True:
            key = keyboard.read_event().name
            num_modules = len(self.modules)

            if key.isdigit() and 1 <= int(key) <= num_modules:
                if not self.navigate_to_menu(key):
                    break  # Exit loop and program
            elif key == '`':  # Backtick key mapped to main menu
                self.display_main_menu()
            elif key == '0':
                print("Exiting program. Goodbye!")
                break  # Exit loop and program
            else:
                print("Invalid input. Please enter a valid menu option.")

if __name__ == "__main__":
    app = CLIApplication()
    app.run()