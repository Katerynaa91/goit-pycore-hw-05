"""Завдання 2.1. Створити функцію generator_numbers, яка буде аналізувати текст, ідентифікувати всі 
дійсні числа і повертати їх як генератор. Дійсні числа у тексті вважаються записаними без помилок і 
чітко відокремлені пробілами з обох боків.

2.2. Реалізувати функцію sum_profit, яка буде використовувати generator_numbers 
для обчислення загальної суми чисел у вхідному рядку (тексті). """

from typing import Callable
from collections.abc import Generator
import re


def generator_numbers(text: str) -> Generator[float]:
    """Функція приймає рядок як аргумент і повертає генератор, що ітерує по всіх дійсних числах у тексті.
    Для ідентифікації дійсних чисел використовуються регулярні вирази """
   
    pattern = re.findall(r'\b[0-9]+\.[0-9]+\b', text)
    for num in pattern:
  
        yield float(num)

#Варіант без використання регулярних виразів для ідентифікації дійсних чисел у тексті
# def generator_numbers(text: str):
#     text_lst = text.split()
#     for word in text_lst:
#         try:
#             if float(word):
#                 yield float(word)
#         except ValueError:
#             pass


def sum_profit(text: str, func: Callable) ->float:
    """У якості параметрів Функція приймає рядок та генератор. 
    Функція повертає суму дійсних чисел, отриманих у результаті роботи генератора"""

    return sum(func(text))
    # Або:
    # sums = 0
    # for num in func(text):
    #     sums += num
    # return sums



text_to_count = """Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, 
доповнений додатковими надходженнями 27.45 і 324.00 доларів."""

total_income = sum_profit(text_to_count, generator_numbers)
print(f"Загальний дохід: {total_income}")
