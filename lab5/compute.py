import threading
from functools import reduce
from math import factorial
import numpy as np
from matplotlib import pyplot as plt


def lagrange_polynomial(xs, ys, n):
    return lambda x: sum([
        ys[i] * reduce(
            lambda a, b: a * b,
            [(x - xs[j]) / (xs[i] - xs[j]) for j in range(n) if i != j]
        ) for i in range(n)
    ])


def divided_differences(x, y):
    n = len(y)
    coef = np.copy(y).astype(float)
    for j in range(1, n):
        for i in range(n-1, j-1, -1):
            coef[i] = (coef[i] - coef[i-1]) / (x[i] - x[i-j])
    return coef


def newton_divided_difference_polynomial(xs, ys, n):
    coef = divided_differences(xs, ys)
    return lambda x: ys[0] + sum([
        coef[k] * reduce(lambda a, b: a * b, [x - xs[j] for j in range(k)]) for k in range(1, n)
    ])


def finite_differences(y):
    n = len(y)
    delta_y = np.zeros((n, n))
    delta_y[:, 0] = y
    for j in range(1, n):
        for i in range(n - j):
            delta_y[i, j] = delta_y[i + 1, j - 1] - delta_y[i, j - 1]
    return delta_y


def print_finite_differences_table(delta_y):
    n = delta_y.shape[0]
    print("Таблица конечных разностей:")
    for i in range(n):
        row = [f"{delta_y[i, j]:.4f}" if i + j < n else "" for j in range(n)]
        print("\t".join(row))


def newton_finite_difference_polynomial(xs, ys, n):
    h = xs[1] - xs[0]
    delta_y = finite_differences(ys)
    return lambda x: ys[0] + sum([
        reduce(lambda a, b: a * b, [(x - xs[0]) / h - j for j in range(k)]) * delta_y[k, 0] / factorial(k) for k in range(1, n)
    ])


def gauss_polynomial(xs, ys, n):
    n = len(xs) - 1
    alpha_ind = n // 2
    fin_difs = [ys[:]]

    for k in range(1, n + 1):
        last = fin_difs[-1][:]
        fin_difs.append(
            [last[i + 1] - last[i] for i in range(n - k + 1)])

    h = xs[1] - xs[0]
    dts1 = [0, -1, 1, -2, 2, -3, 3, -4, 4]

    f1 = lambda x: ys[alpha_ind] + sum([
        reduce(lambda a, b: a * b,
               [(x - xs[alpha_ind]) / h + dts1[j] for j in range(k)])
        * fin_difs[k][len(fin_difs[k]) // 2] / factorial(k)
        for k in range(1, n + 1)])

    f2 = lambda x: ys[alpha_ind] + sum([
        reduce(lambda a, b: a * b,
               [(x - xs[alpha_ind]) / h - dts1[j] for j in range(k)])
        * fin_difs[k][len(fin_difs[k]) // 2 - (1 - len(fin_difs[k]) % 2)] / factorial(k)
        for k in range(1, n + 1)])

    return lambda x: f1(x) if x > xs[alpha_ind] else f2(x)


def stirling_polynomial(xs, ys, n):
    n = len(xs) - 1
    alpha_ind = n // 2
    fin_difs = [ys[:]]

    for k in range(1, n + 1):
        last = fin_difs[-1][:]
        fin_difs.append(
            [last[i + 1] - last[i] for i in range(n - k + 1)])

    h = xs[1] - xs[0]
    dts1 = [0, -1, 1, -2, 2, -3, 3, -4, 4]

    f1 = lambda x: ys[alpha_ind] + sum([
        reduce(lambda a, b: a * b,
               [(x - xs[alpha_ind]) / h + dts1[j] for j in range(k)])
        * fin_difs[k][len(fin_difs[k]) // 2] / factorial(k)
        for k in range(1, n + 1)])

    f2 = lambda x: ys[alpha_ind] + sum([
        reduce(lambda a, b: a * b,
               [(x - xs[alpha_ind]) / h - dts1[j] for j in range(k)])
        * fin_difs[k][len(fin_difs[k]) // 2 - (1 - len(fin_difs[k]) % 2)] / factorial(k)
        for k in range(1, n + 1)])

    return lambda x: (f1(x) + f2(x)) / 2


def bessel_polynomial(xs, ys, n):
    n = len(xs) - 1
    alpha_ind = n // 2
    fin_difs = [ys[:]]

    for k in range(1, n + 1):
        last = fin_difs[-1][:]
        fin_difs.append(
            [last[i + 1] - last[i] for i in range(n - k + 1)])

    h = xs[1] - xs[0]
    dts1 = [0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5]

    return lambda x: (ys[alpha_ind] + ys[alpha_ind]) / 2 + sum([
        reduce(lambda a, b: a * b,
               [(x - xs[alpha_ind]) / h + dts1[j] for j in range(k)])
        * fin_difs[k][len(fin_difs[k]) // 2] / factorial(2 * k) +

        ((x - xs[alpha_ind]) / h - 1 / 2) *
        reduce(lambda a, b: a * b,
               [(x - xs[alpha_ind]) / h + dts1[j] for j in range(k)])
        * fin_difs[k][len(fin_difs[k]) // 2] / factorial(2 * k + 1)

        for k in range(1, n + 1)])


def plot_with_nodes_and_function(a, b, interp_func, nodes_x, nodes_y, interp_name, dx=0.001):
    xs = np.arange(a, b + dx, dx)
    ys_interp = [interp_func(x) for x in xs]

    plt.figure(figsize=(10, 6))

    
    plt.plot(xs, ys_interp, label=interp_name, color='blue')

    plt.scatter(nodes_x, nodes_y, color='red', label='Узлы интерполяции', zorder=5)

    plt.title(f"{interp_name}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.show()


def compute(xs, ys, x, n):
    delta_y = finite_differences(ys)
    print_finite_differences_table(delta_y)

    methods = [
        ("Многочлен Лагранжа", lagrange_polynomial),
        ("Многочлен Ньютона с разделенными разностями", newton_divided_difference_polynomial),
        ("Многочлен Ньютона с конечными разностями", newton_finite_difference_polynomial),
        ("Многочлен Гаусса", gauss_polynomial),
        ("Многочлен Стирлинга", stirling_polynomial),
        ("Многочлен Бесселя", bessel_polynomial)
    ]

    for name, method in methods:
        print(name)
        P = method(xs, ys, n)
        print(f'P({x}) = {P(x)}')

        plot_with_nodes_and_function(xs[0], xs[-1], P, xs, ys, name)
