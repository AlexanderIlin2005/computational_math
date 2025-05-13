def euler_method(func, x_values, y_initial, eps):
    y_values = [y_initial]
    step = x_values[1] - x_values[0]
    for i in range(len(x_values) - 1):
        y_next = y_values[i] + step * func(x_values[i], y_values[i])
        y_values.append(y_next)
    return y_values


def improved_euler_method(func, x_values, y_initial, eps):
    y_values = [y_initial]
    step = x_values[1] - x_values[0]
    for i in range(len(x_values) - 1):
        y_predict = func(x_values[i], y_values[i])
        y_correct = func(x_values[i] + step, y_values[i] + step * y_predict)
        y_next = y_values[i] + 0.5 * step * (y_predict + y_correct)
        y_values.append(y_next)
    return y_values


def milne_method(func, x_values, y_initial, eps):
    num_points = len(x_values)
    step = x_values[1] - x_values[0]
    y_values = [y_initial]

    # Начальные 3 точки по методу Рунге-Кутта
    for i in range(1, 4):
        k1 = step * func(x_values[i - 1], y_values[i - 1])
        k2 = step * func(x_values[i - 1] + step / 2, y_values[i - 1] + k1 / 2)
        k3 = step * func(x_values[i - 1] + step / 2, y_values[i - 1] + k2 / 2)
        k4 = step * func(x_values[i - 1] + step, y_values[i - 1] + k3)
        y_next = y_values[i - 1] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        y_values.append(y_next)

    # Метод Милна
    for i in range(4, num_points):
        y_predict = y_values[i - 4] + (4 * step / 3) * (
            2 * func(x_values[i - 3], y_values[i - 3]) -
            func(x_values[i - 2], y_values[i - 2]) +
            2 * func(x_values[i - 1], y_values[i - 1])
        )

        y_corrected = y_predict
        while True:
            y_correct_next = y_values[i - 2] + (step / 3) * (
                func(x_values[i - 2], y_values[i - 2]) +
                4 * func(x_values[i - 1], y_values[i - 1]) +
                func(x_values[i], y_corrected)
            )
            if abs(y_correct_next - y_corrected) < eps:
                y_corrected = y_correct_next
                break
            y_corrected = y_correct_next

        y_values.append(y_corrected)

    return y_values
