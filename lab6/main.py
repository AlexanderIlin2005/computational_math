from math import sin, cos, exp, log, inf
import matplotlib.pyplot as plt
import os, signal

from methods import euler_method, improved_euler_method, milne_method

MAX_ITERS = 20


def user_input(prompt):
    s = input(prompt)
    if s.lower() == 'q':
        print("! Выход из программы.")
        os.kill(os.getpid(), signal.SIGINT)
    return s


def select_equation():
    equations = {
        1: {
            'desc': "y + (1 + x)*y^2",
            'func': lambda x, y: y + (1 + x) * y ** 2,
            'exact': lambda x, x0, y0: -exp(x) / (x * exp(x) - (x0 * exp(x0) * y0 + exp(x0)) / y0)
        },
        2: {
            'desc': "x + y",
            'func': lambda x, y: x + y,
            'exact': lambda x, x0, y0: exp(x - x0) * (y0 + x0 + 1) - x - 1
        },
        3: {
            'desc': "sin(x) - y",
            'func': lambda x, y: sin(x) - y,
            'exact': lambda x, x0, y0: (2 * exp(x0) * y0 - exp(x0) * sin(x0) + exp(x0) * cos(x0)) / (2 * exp(x)) + sin(x) / 2 - cos(x) / 2
        },
        4: {
            'desc': "y / x",
            'func': lambda x, y: y / x,
            'exact': lambda x, x0, y0: (x * y0) / x0
        },
        5: {
            'desc': "e^x",
            'func': lambda x, y: exp(x),
            'exact': lambda x, x0, y0: y0 - exp(x0) + exp(x)
        },
        6: {
            'desc': "cos(x)",
            'func': lambda x, y: cos(x),
            'exact': lambda x, x0, y0: y0 + sin(x) - sin(x0)
        },
        7: {
            'desc': "x * y",
            'func': lambda x, y: x * y,
            'exact': lambda x, x0, y0: y0 * exp(0.5 * (x**2 - x0**2))
        },
        8: {
            'desc': "y * cos(x)",
            'func': lambda x, y: y * cos(x),
            'exact': lambda x, x0, y0: y0 * exp(sin(x) - sin(x0))
        },
        9: {
            'desc': "ln(x)",
            'func': lambda x, y: log(x),
            'exact': lambda x, x0, y0: y0 + x * log(x) - x - x0 * log(x0) + x0
        }
    }

    print("Выберите ОДУ (введите номер, 'q' — выход):")
    for idx, item in equations.items():
        print(f"{idx}. y' = {item['desc']}")
    print()

    while True:
        try:
            choice = int(user_input("> Номер уравнения: "))
            if choice in equations:
                return equations[choice]['func'], equations[choice]['exact'], equations[choice]['desc'], choice
            else:
                print("! Неверный номер. Повторите ввод.")
        except ValueError:
            print("! Введите число (номер уравнения).")


def draw_exact_plot(x_start, x_end, exact_func, x0, y0, dx=0.01):
    """Построение точного графика"""
    xs, ys = [], []
    x = x_start - dx
    while x <= x_end + dx:
        try:
            y = exact_func(x, x0, y0)
            xs.append(x)
            ys.append(y)
        except:
            xs.append(x)
            ys.append(None)
        x += dx
    plt.plot(xs, ys, 'g')


def solve_equation(func, x0, x_end, num_points, y0, exact_func, epsilon, eq_desc, eq_id):
    methods = [
        ("Метод Эйлера", euler_method),
        ("Усовершенствованный метод Эйлера", improved_euler_method),
        ("Метод Милна", milne_method)
    ]

    for method_name, method_func in methods:
        print(f"\n{method_name}:\n")
        try:
            iterations = 0
            n = num_points
            xs = [x0 + i * (x_end - x0) / n for i in range(n)]
            ys = method_func(func, xs, y0, epsilon)
            error = inf

            while error > epsilon:
                if iterations >= MAX_ITERS:
                    print(f"! Достигнуто максимальное число итераций ({MAX_ITERS})")
                    break
                iterations += 1
                n *= 2
                xs = [x0 + i * (x_end - x0) / n for i in range(n)]
                new_ys = method_func(func, xs, y0, epsilon)

                if method_func is milne_method or exact_func is None:
                    error = max(abs(exact_func(x, x0, y0) - y) for x, y in zip(xs, new_ys)) if exact_func else inf
                else:
                    order = 2 if method_func is improved_euler_method else 1
                    error = abs(new_ys[-1] - ys[-1]) / (2**order - 1)

                ys = new_ys.copy()

            h = round((x_end - x0) / n, 6)
            print(f"Достигнута точность eps={epsilon} при n={n}, шаг h={h}")

            if len(xs) <= 100:
                print("y:\t[", *map(lambda val: round(val, 5), ys), "]")
                if exact_func:
                    print("y_точн:\t[", *map(lambda x: round(exact_func(x, x0, y0), 5), xs), "]")
            else:
                show_all = user_input("Результатов > 100. Показать все? [y/n]: ").lower()
                if show_all == 'y':
                    print("y:\t[", *map(lambda val: round(val, 5), ys), "]")
                    if exact_func:
                        print("y_точн:\t[", *map(lambda x: round(exact_func(x, x0, y0), 5), xs), "]")

            if exact_func:
                print(f"Погрешность: {error}")
            else:
                print("Точное решение отсутствует. Погрешность не вычисляется.")

            show_plot = user_input("Выводить график? [y/n]: ").lower()
            if show_plot == 'y':
                print("\nПостроение графика...")
                plt.title(f"{method_name} — {eq_desc}")
                if exact_func:
                    draw_exact_plot(xs[0], xs[-1], exact_func, x0, y0)
                plt.scatter(xs, ys, c='r', s=10)
                plt.xlabel("x")
                plt.ylabel("y")
                plt.grid(True)
                plt.show()
            else:
                print("График не выведен.")


        except OverflowError:
            print("! Ошибка: переполнение (возможно, слишком маленький шаг или слишком большая точность).")
        except ZeroDivisionError:
            print("! Деление на ноль — некорректный x для выбранного уравнения.")
        except ValueError:
            print("! Некорректное значение — возможно, логарифм от неположительного числа.")


def main():
    while True:
        func, exact_func, eq_desc, eq_id = select_equation()

        while True:
            try:
                x0 = float(user_input("> Введите начальное значение x0: "))
                x_end = float(user_input("> Введите конечное значение x: "))
                if x_end <= x0:
                    print("! x должно быть больше x0.")
                    continue

                if eq_id == 9 and (x0 <= 0 or x_end <= 0):
                    print("! Для ln(x) x0 и x должны быть > 0.")
                    continue

                n = int(user_input("> Введите начальное количество шагов n (целое > 1): "))
                if n <= 1:
                    print("! n должно быть больше 1.")
                    continue

                y0 = float(user_input("> Введите начальное значение y0: "))
                eps = float(user_input("> Введите точность eps (> 0): "))
                if eps <= 0:
                    print("! eps должно быть положительным.")
                    continue

                break
            except ValueError:
                print("! Ошибка ввода. Попробуйте ещё раз.\n")

        solve_equation(func, x0, x_end, n, y0, exact_func, eps, eq_desc, eq_id)

        again = input("\nРешить другую задачу? [y/n]: ").strip().lower()
        if again != 'y':
            print("Завершение программы.")
            break


if __name__ == "__main__":
    main()
