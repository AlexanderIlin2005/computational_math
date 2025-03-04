from typing import Tuple
import decimal

from dto.equation import Equation


def choose_equation_type():
    """
    Запрашивает у пользователя выбор типа программы.

    Возвращает:
        int: Номер выбранного типа (1 - нелинейное уравнение, 2 - система нелинейных уравнений, 3 - выход)
    """
    print("Выберите тип программы:")
    print('1: Нелинейное уравнение')
    print('2: Система нелинейных уравнений')
    print('3: Выход')

    try:
        equation_type_number = int(input("Введите номер типа: "))
    except ValueError:
        print('(!) Вы ввели не число')
        return choose_equation_type()

    if equation_type_number not in [1, 2, 3]:
        print("(!) Такого номера нет.")
        return choose_equation_type()

    return equation_type_number


def choose_equation(functions) -> Equation:
    """
    Запрашивает у пользователя выбор уравнения из предложенного списка.

    Аргументы:
        functions (dict): Словарь с номерами и уравнениями.

    Возвращает:
        Equation: Выбранное уравнение.
    """
    print("Выберите уравнение:")
    for num, func in functions.items():
        print(str(num) + ': ' + func.text)

    try:
        equation_number = int(input("Введите номер уравнения: "))
    except ValueError:
        print('(!) Вы ввели не число')
        return choose_equation(functions)

    if equation_number < 1 or equation_number > len(functions):
        print("(!) Такого номера нет.")
        return choose_equation(functions)

    return functions[equation_number]


def choose_method_number(methods) -> int:
    """
    Запрашивает у пользователя выбор метода решения.

    Аргументы:
        methods (dict): Словарь с номерами и методами.

    Возвращает:
        int: Номер выбранного метода.
    """
    print("Выберите метод:")
    for num, mtd in methods.items():
        print(str(num) + ': ' + mtd.name)

    try:
        method_number = int(input("Введите номер метода: "))
    except ValueError:
        print('(!) Вы ввели не число')
        return choose_method_number(methods)

    if method_number < 1 or method_number > len(methods):
        print("(!) Такого номера нет.")
        return choose_method_number(methods)

    return method_number


def print_result(result, output_file_name):
    """
    Выводит результат на экран или записывает в файл.

    Аргументы:
        result (any): Результат вычислений.
        output_file_name (str): Имя файла для сохранения результата (если пусто, выводится в консоль).
    """
    if output_file_name == '':
        print('\n' + str(result))
    else:
        with open(output_file_name, "w") as f:
            f.write(str(result))
        print('Результат записан в файл.')


def read_initial_data() -> Tuple[float, float, float, int]:
    """
    Считывает исходные данные и интервал либо из файла, либо запрашивает у пользователя.

    Возвращает:
        Tuple[float, float, float, int]: Левая и правая границы интервала, погрешность, количество знаков после запятой.
    """
    while True:
        filename = input("Введите имя файла для загрузки исходных данных и интервала "
                         "или пустую строку, чтобы ввести вручную: ")
        if filename == '':
            left = float(input('Введите левую границу интервала: '))
            right = float(input('Введите правую границу интервала: '))
            epsilon = input('Введите погрешность вычисления: ')
            break
        else:
            try:
                with open(filename, "r") as f:
                    left = float(f.readline())
                    right = float(f.readline())
                    epsilon = f.readline().strip()
                print(f'Считано из файла: Лeвая граница: {left}, правая: {right}, погрешность: {epsilon}')
                break
            except FileNotFoundError:
                print('(!) Файл для загрузки исходных данных не найден.')

    decimal_places = abs(decimal.Decimal(epsilon).as_tuple().exponent)
    epsilon = float(epsilon)

    return left, right, epsilon, decimal_places


def read_initial_data_newton() -> Tuple[float, float, int]:
    """
    Считывает исходные данные для метода Ньютона (начальное приближение и погрешность) из файла или с ввода.

    Возвращает:
        Tuple[float, float, int]: Начальное приближение, погрешность, количество знаков после запятой.
    """
    while True:
        filename = input("Введите имя файла для загрузки исходных данных и интервала "
                         "или пустую строку, чтобы ввести вручную: ")
        if filename == '':
            x0 = float(input('Введите начальное приближение: '))
            epsilon = input('Введите погрешность вычисления: ')
            break
        else:
            try:
                with open(filename, "r") as f:
                    x0 = float(f.readline())
                    epsilon = f.readline().strip()
                print(f'Считано из файла: Начальное приближение: {x0}, погрешность: {epsilon}')
                break
            except FileNotFoundError:
                print('(!) Файл для загрузки исходных данных не найден.')

    decimal_places = abs(decimal.Decimal(epsilon).as_tuple().exponent)
    epsilon = float(epsilon)

    return x0, epsilon, decimal_places
