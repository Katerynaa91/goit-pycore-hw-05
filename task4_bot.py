"""Завдання 4. Створити декоратор input_error для обробки помилок введення користувача.
Декоратор повинен обробляти винятки, що виникають у функціях, такі як: KeyError, ValueError, IndexError. 
Виконання програми при цьому не припиняється."""
"""Також додала глобальну змінну для словника контактів до основної функції, щоб можна було зберігати 
дані, отримані під час циклу."""

from typing import Callable
from functools import wraps

def input_error(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        try:
            return func(*args, **kwargs)
        except (TypeError, ValueError, IndexError):
            print("""Invalid request. Enter your request in the following format:
            - Add Name Phone
            - Change Name Phone
            - Show Name
            - All
            - Delete Name
            - Close or q (to close the program)""")
        except (KeyError): 
            print("Name not found in the Contacts")
    return wrapper
    

@input_error
def parse_input(input_val: str) -> list:
    """Функція парсить рядок-запит, введений користувачем та обробляє випадок, якщо кількість 
    введених елементів не відповідає очікуваній структурі команди."""

    parsed_input = input_val.lower().split()
    if len(parsed_input) <= 3:
        return parsed_input
    else: raise ValueError
    

@input_error
def add_contact(parsed_input_args: list, contacts_dict: dict):
    """Аргументи функції - введене значення без назви команди та словник контаків.
    Функція перевіріє, чи існує ім'я у словнику. Якщо не існує, створюється новий запис.
    Обробляється помилка, якщо кількість отриманих аргументів не відповідає очікуваній кількості. """

    if parsed_input_args[0] not in contacts_dict.keys():
        contacts_dict[parsed_input_args[0]] = parsed_input_args[1]
        print("Contact added!")
    else:
        print("Contact already exists. To create a new contact - use a different name")
    

@input_error
def change_contact(parsed_input_args:list, contacts_dict: dict):
    """Якщо ім'я, отримане у запиті користувача, відповідає ключу словника, функція змінює значення для 
    відповідного ключа"""

    if len(parsed_input_args) == 2 and contacts_dict.get(parsed_input_args[0]):
        contacts_dict[parsed_input_args[0]] = parsed_input_args[1]
        print("Contact updated!")    
    else: 
        print("Name not found in contacts. If you want to add a new contact, please use 'add' command")
    

@input_error 
def show_phone(parsed_input_args:list, contacts_dict: dict):
    """Функція повертає пару ключ (ім'я контакта) - значення (номер телефона) відповідно до введеного запиту."""

    if parsed_input_args[0] not in contacts_dict or len(parsed_input_args) != 1:
        print("Contact not found")
            
    else:
        for key, value in contacts_dict.items():
            if parsed_input_args[0] == key:
                print(key.capitalize(), value)


@input_error 
def show_all(contacts_dict: dict):
    """Функція отримує словник контактів у якості параметра та повертає зміст цього словника."""

    if contacts_dict:
        for key, value in contacts_dict.items():
            print(key.capitalize(), value)
    else: print("Contacts list is empty.")


@input_error 
def delete_contact(parsed_input_args:list, contacts_dict: dict):
    """Функція видаляє запис зі словника відповідно до введеного запиту."""
    if len(parsed_input_args) == 1:
        contacts_dict.pop(parsed_input_args[0])
        print("Contact deleted")
    else: raise ValueError


def main(*args, **kwargs):
    command_names = {
        "greeting": ["hi", "hello"],
        "add": ["add"],
        "change": ["change", "update"],
        "show": ["show", "view"],
        "show_all": ["all"],
        "close": ["close", "exit", "quit", "q", "bye"],
        "delete": ["remove", "delete", "del"]
    }
    global phone_book

    while True:
        user_input = input("Enter your request: ")
        if parse_input(user_input):
            command, *args = parse_input(user_input)

            if command in command_names["greeting"]:
                print("Hi. How may I help you?")
            elif command in command_names["add"]:
                add_contact(args, phone_book)
            elif command in command_names["change"]:
                change_contact(args, phone_book)
            elif command in command_names["show"]:
                show_phone(args, phone_book)
            elif command in command_names["show_all"]:
                print("Type 'all' to check all contacts list") if args else show_all(phone_book)
            elif command in command_names["delete"]:
                delete_contact(args, phone_book)
            elif command in command_names["close"]:
                print("Bye!")
                break
            else: print("Invalid command")
        else: print("Cannot read your request. Please try again.")


if __name__ == "__main__":
    phone_book = {}
    main()
    print(phone_book)