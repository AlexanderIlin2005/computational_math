from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import det

def a(xy):
    """ Система уравнений """
    x, y = xy
    return np.array([
        x**2 + y**2 - 1,
        x**2 - y - 0.5
    ])

def jacobian(xy):
    """ Матрица Якоби """
    x, y = xy
    return np.array([
        [2*x, 2*y],
        [2*x, -1]
    ])

def newton_method(a, jacobian, x0, epsilon=1e-6, max_iterations=100):
    """ Метод Ньютона """
    x = np.array(x0, dtype=float)

    for iteration in range(max_iterations):
        J = jacobian(x)
        F = a(x)

        try:
            delta_x = np.linalg.solve(J, -F)  # Решаем J * Δx = -F
        except np.linalg.LinAlgError:
            print(f"(!) Метод Ньютона не работает при начальном приближении x=0. Матрица Якоби вырождена (определитель = 0).")
            print("Попробуйте выбрать другое начальное приближение gо x(строго не равное нулю(может быть близким к нему))")
            return None, None

        x_next = x + delta_x

        print(f"{iteration}. x = ({x_next[0]:.6f}, {x_next[1]:.6f}), ||dx|| = {np.linalg.norm(delta_x):.2e}")

        if np.linalg.norm(delta_x) < epsilon:
            return x_next, iteration + 1

        x = x_next

    print("Метод Ньютона не сошелся!")
    return None, None

def plot_system(system):
    """ Построение графиков уравнений """
    x = np.linspace(-2, 2, 400)
    y = np.linspace(-2, 2, 400)
    X, Y = np.meshgrid(x, y)

    Z1 = np.array([system([x_, y_])[0] for x_, y_ in zip(np.ravel(X), np.ravel(Y))]).reshape(X.shape)
    Z2 = np.array([system([x_, y_])[1] for x_, y_ in zip(np.ravel(X), np.ravel(Y))]).reshape(X.shape)

    if input("Показать график системы(y - да, любой другой символ или пустая строка - нет):") == "y":
        plt.contour(X, Y, Z1, levels=[0], colors='r')
        plt.contour(X, Y, Z2, levels=[0], colors='b')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
        plt.show()

def run():
    plot_system(a)

    x0, y0 = map(float, input("Введите начальные приближения x0, y0: ").split())
    epsilon = float(input('Введите погрешность вычисления: '))

    xy_solution, iterations = newton_method(a, jacobian, (x0, y0), epsilon)

    if xy_solution is not None:
        print(f"\nРешение: x = {xy_solution[0]:.6f}, y = {xy_solution[1]:.6f}")
        print(f"Количество итераций: {iterations}")
        print(f'Невязка: {a(xy_solution)[0]:.2e}, {a(xy_solution)[1]:.2e}')
