from math import sin, sqrt
from compute import compute


def read_from_file(filename):
    try:
        with open(filename, 'r') as file:
            x, xs, ys = None, [], []
            x_read = False
            for line in file:
                line = line.strip()
                if not x_read:
                    try:
                        x = float(line)
                        x_read = True
                    except ValueError:
                        print(f"Ошибка: Невозможно преобразовать строку '{line}' в число для точки интерполяции.")
                        return None, None, None, "! Неверный формат данных в файле."
                else:
                    point = line.split()
                    if len(point) == 2:
                        try:
                            xs.append(float(point[0]))
                            ys.append(float(point[1]))
                        except ValueError:
                            print(f"Ошибка: Невозможно преобразовать строку '{line}' в числа для узлов.")
                            return None, None, None, "! Неверный формат данных в файле."
                    else:
                        print(f"Предупреждение: Пропущена строка '{line}', так как она не содержит два значения.")
            if x is None or not xs or not ys:
                return None, None, None, "! Файл пуст или данные в файле некорректны."
            return x, xs, ys, None
    except IOError as err:
        return None, None, None, f"! Невозможно прочитать файл {filename}: {err}"
    except Exception as e:
        return None, None, None, f"! Произошла ошибка при обработке файла: {e}"


def read_from_input():
    while True:
        try:
            x = float(input("Введите точку интерполяции: "))
            break
        except ValueError:
            print("Ошибка: Введено некорректное значение. Попробуйте снова.")

    xs, ys = [], []
    print("Введите 'quit', чтобы закончить ввод.")
    print("Введите узлы интерполяции (формат: x y):")
    while True:
        str_input = input()
        if str_input.strip().lower() == 'quit':
            break
        point = str_input.strip().split()
        if len(point) == 2:
            try:
                xs.append(float(point[0]))
                ys.append(float(point[1]))
            except ValueError:
                print("Ошибка: Невозможно преобразовать введенные значения в числа. Попробуйте снова.")
        else:
            print("Ошибка: Введена неверная точка. Ожидаются два числа, разделенные пробелом.")

    if not xs or not ys:
        print("Ошибка: Не было введено ни одного узла интерполяции.")
        return None, None, None
    return x, xs, ys


def read_from_function():
    print('Выберите одну из доступных функций:')
    print('1. sin(x)')
    print('2. sqrt(x)')
    print('3. x^5')
    print('4. 2*x^2 - 5*x')

    func_map = {
        1: lambda x: sin(x),
        2: lambda x: sqrt(x),
        3: lambda x: x ** 5,
        4: lambda x: 2 * x ** 2 - 5 * x,
    }

    while True:
        try:
            input_func = int(input('Выберите функцию [1/2/3/4]: '))
            if input_func in func_map:
                f = func_map[input_func]
                break
            else:
                print("Ошибка: Некорректный выбор функции. Попробуйте снова.")
        except ValueError:
            print("Ошибка: Введено некорректное значение. Попробуйте снова.")

    while True:
        try:
            n = int(input("Введите число узлов: "))
            if n <= 1:
                print("Ошибка: Количество узлов должно быть больше 1. Попробуйте снова.")
            else:
                break
        except ValueError:
            print("Ошибка: Введено некорректное значение. Попробуйте снова.")

    while True:
        try:
            x0 = float(input('Введите x0: '))
            xn = float(input('Введите xn: '))
            if xn <= x0:
                print("Ошибка: xn должно быть больше x0. Попробуйте снова.")
            else:
                break
        except ValueError:
            print("Ошибка: Введено некорректное значение. Попробуйте снова.")

    h = (xn - x0) / (n - 1)
    xs = [x0 + h * i for i in range(n)]
    ys = list(map(f, xs))

    while True:
        try:
            x = float(input('Введите точку интерполяции: '))
            if x < x0 or x > xn:
                print(f"Ошибка: Точка интерполяции {x} должна быть в интервале [{x0}, {xn}]. Попробуйте снова.")
            else:
                break
        except ValueError:
            print("Ошибка: Введено некорректное значение. Попробуйте снова.")

    return x, xs, ys


def main():
    while True:
        while True:
            print("Введите:\n  - 'fi' для ввода из файла;\n  - 't' для ввода с терминала;\n  - 'fu' для задания функции.")
            option = input("Ваш ввод: ")
            if option == 'fi':
                while True:
                    filename = input("Введите имя файла: ")
                    x, xs, ys, error = read_from_file(filename)
                    if error:
                        print(error)
                        one_more_time = input("Попробовать другое имя файла? [y/n]: ")
                        if one_more_time == 'y':
                            continue
                        else:
                            x, xs, ys = read_from_input()
                            break
                    else:
                        break
                n = len(xs)
                break
            elif option == 't':
                x, xs, ys = read_from_input()
                n = len(xs)
                break
            elif option == 'fu':
                x, xs, ys = read_from_function()
                n = len(xs)
                break
            else:
                print("! Некорректный ввод. Попробуйте еще раз\n")

        if len(set(xs)) != len(xs):
            print('! Узлы интерполяции не должны совпадать. Введите еще раз.')
        elif xs != sorted(xs):
            print('! X интерполяции должны быть отсортированы. Введите еще раз.')
        else:
            break

    compute(xs, ys, x, n)


def main_loop():
    while True:
        inp = input("Введите 'q' для выхода, или Enter для продолжения: ")
        if inp == "q":
            break
        main()


if __name__ == "__main__":
    main_loop()
