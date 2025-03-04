import math

from dto.equation import Equation  # Импорт класса уравнения
from methods.half_division import HalfDivisionMethod  # Метод половинного деления
from methods.newton import NewtonMethod  # Метод Ньютона
from methods.simple_iterations import SimpleIterationsMethod  # Метод простых итераций
from methods.chord import ChordMethod  # Метод хорд

import equations_system  # Модуль для работы с системами уравнений
import input_handler  # Модуль для обработки ввода пользователя

# Словарь доступных методов решения
methods = {
    1: HalfDivisionMethod,
    2: ChordMethod,
    3: SimpleIterationsMethod,
    4: NewtonMethod
}

# Предопределенные функции, представленные в виде лямбда-выражений
predefined_functions = {
    1: Equation(lambda x: (-1.38*x**3 - 5.42*x**2 + 2.57*x + 10.95), '-1.38*x^3 - 5.42*x^2 + 2.57*x + 10.95'),
    2: Equation(lambda x: (x**3 - 1.89*x**2 - 2*x + 1.76), 'x^3 - 1.89*x^2 - 2*x + 1.76'),
    # Источник функции: https://cutt.ly/6zNbCha
    3: Equation(lambda x: (x / 2 - 2 * (x + 2.39) ** (1 / 3)), 'x/2 - 2*(x + 2.39)^(1/3)'),
    # Источник функции: https://cutt.ly/MzNdHH5
    4: Equation(lambda x: (-x / 2 + math.e ** x + 5 * math.sin(x)), '-x/2 + e^x + 5*sin(x)'),
}

ENABLE_LOGGING = True  # Флаг для включения логирования

while True:
    # Выбор типа уравнения (нелинейное уравнение, система уравнений, выход)
    equation_type = input_handler.choose_equation_type()

    if equation_type == 3:
        break  # Выход из программы

    if equation_type == 1:
        # Выбор конкретного уравнения
        function = input_handler.choose_equation(predefined_functions)
        try:
            function.draw(-100, 100)  # Попытка построить график функции
        except Exception as e:
            print('(!) Не удалось построить график функции, ', e)

        # Выбор метода решения
        method_number = input_handler.choose_method_number(methods)

        while True:
            if method_number == 4:  # Метод Ньютона требует начального приближения
                left, epsilon, decimal_places = input_handler.read_initial_data_newton()
                right = 0  # Правая граница не требуется
            else:
                left, right, epsilon, decimal_places = input_handler.read_initial_data()

            # Инициализация метода
            method = methods[method_number](function, left, right, epsilon, decimal_places, ENABLE_LOGGING)
            try:
                verified, reason = method.check()  # Проверка корректности входных данных
            except TypeError as te:
                print('(!) Ошибка при вычислении значения функции, возможно она не определена на всем интервале.')
                continue
            if not verified:
                print('(!) Введенные исходные данные для метода некорректны: ', reason)
            break

        try:
            function.draw(left, right)  # Попытка построить график в указанном диапазоне
        except Exception as e:
            print('(!) Не удалось построить график функции, ', e)

        # Выбор формата вывода (в консоль или файл)
        output_file_name = input("Введите имя файла для вывода результата или пустую строку, чтобы вывести в консоль: ")

        try:
            if ENABLE_LOGGING:
                print('Процесс решения: ')
            result = method.solve()  # Запуск метода решения
        except Exception as e:
            print(e)
            print('(!) Что-то пошло не так при решении: ', e)
            continue

        input_handler.print_result(result, output_file_name)  # Вывод результата

        # Возможность повторного запуска
        if input('\nЕще раз? [y/n] ') != 'y':
            break
    else:
        equations_system.run()  # Запуск решения системы уравнений

print('Спасибо за использование программы!')
