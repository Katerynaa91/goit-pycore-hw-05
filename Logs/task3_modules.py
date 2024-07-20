"""Завдання 3. Розробити Python-скрипт для аналізу файлів логів. Скрипт повинен вміти читати лог-файл, 
переданий як аргумент командного рядка, і виводити статистику за рівнями логування:
INFO, ERROR, DEBUG, WARNING. 
Скрипт повинен приймати шлях до файлу логів як аргумент командного рядка.
Скрипт повинен приймати не обов'язковий аргумент командного рядка, після аргументу шляху до файлу логів. 
Він відповідає за виведення всіх записів певного рівня логування. 
Наприклад аргумент error виведе всі записи рівня ERROR з файлу логів.
Скрипт має підраховуючи кількість записів для кожного рівня логування (INFO, ERROR, DEBUG, WARNING).
Результати мають бути представлені у вигляді таблиці з кількістю записів для кожного рівня."""

from prettytable import PrettyTable
from pathlib import Path


def error_handler(func):
    """Декоратор для "відлову" помилок різних типів"""
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except FileNotFoundError: print("File Not Found")
        except TypeError: print("Incorrect arguments")
        except ValueError: print("Incorrect arguments")
        except KeyError: print("The record in dictionary is not found. Incorrect key.")

        return res
    return wrapper

@error_handler
def load_logs(file_path: str) -> list: 
    """Функція для читання лог-файлу. У якості параматра отримує шлях до файла, повертає список рядків файлу."""

    if Path(file_path).exists():
        with open(file_path, "r", encoding="utf-8") as fp:
            logs = fp.readlines()
            return logs
    else: print("File Not Found")


@error_handler 
def parse_log_line(line: str) -> dict: 
    """Функція для парсингу рядків лог-файлу. Функція повертає словник, де ключами виступають категорії
    записів лог-файлу (дата, час, рівень події та її опис), а значеннями - власне події та записи, отримані
    з лог-файлу."""
    logs_dict = {}
    record = line.strip().split()
    date, time, status, *status_description = record 
    status_description = ' '.join(status_description)
    logs_dict = {"date": date, "time": time, "level": status, "description": status_description}
    return logs_dict


@error_handler 
def filter_logs_by_level(logs: list, level: str) -> list: 
    """Функція для фільтрації подій логу за їх рівнем (INFO, ERROR, DEBUG, WARNING). Повертає список. """
    level_logs = []
    for line in logs:
        if line["level"].lower() == level.lower():
            level_logs.append(line)
    return level_logs


@error_handler
def logs_to_table(logs: list, Table: PrettyTable, columns: list) -> PrettyTable:
    """Функція для повернення записів логу у вигляді таблиці. Для форматування результатів у таблицю
    функція використовує модуль PrettyTable та повертає об'єкт класу prettyTable. Назви стовпців - ключі словників списку записів лог-файлу,
    дані колонок - події лог-файлу."""
    for index, name in enumerate(columns):
        Table.add_column(columns[index], [line[columns[index]] for line in logs])
    Table.align = 'l'
    return Table


@error_handler
def count_logs_by_level(logs: list) -> dict:
    """Функція рахує кількість записів кожного рівня. Повертає словник, де ключ - це назва рівня, значення - скільки разів цей рівень 
    зустрічається у лог-файлі."""
    counts_dict = {}
    for line in logs:
        if line["level"] in counts_dict:
            counts_dict[line["level"]]+=1
        else:
            counts_dict[line["level"]]=1
    return counts_dict

@error_handler
def display_log_counts(counts: dict, column1 = "Level", column2 = "Count") -> PrettyTable:
    """Функція для повернення результатів, отриманих за допомогою попередньої функції, у вигляді таблиці. Для форматування результатів 
    у таблицю функція використовує модуль PrettyTable та повертає об'єкт класу prettyTable."""
    Table = PrettyTable()
    Table.add_column(column1, [key for key in counts.keys()])
    Table.add_column(column2, [value for value in counts.values()])
    Table.align = 'l'
    return Table