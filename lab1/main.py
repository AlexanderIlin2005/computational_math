class IterativeMethod:
    def __init__(self, matrix, vector_b, tolerance):
        """
        Инициализация метода с матрицей коэффициентов, вектором свободных членов и точностью.
        :param matrix: Матрица коэффициентов системы.
        :param vector_b: Вектор свободных членов.
        :param tolerance: Точность решения.
        """
        self.matrix = matrix
        self.vector_b = vector_b
        self.tolerance = tolerance
        self.n = len(matrix)  # Размерность системы

    def check_diagonal_dominance(self):
        """
        Проверка диагонального преобладания. Если оно отсутствует, пытаемся сделать перестановку.
        """
        for i in range(self.n):
            row_sum = sum(abs(self.matrix[i][j]) for j in range(self.n)) - abs(self.matrix[i][i])
            if abs(self.matrix[i][i]) <= row_sum:
                return False
        return True

    def make_diagonal_dominance(self):
        """
        Попытка перестановки строк для достижения диагонального преобладания.
        """
        for i in range(self.n):
            # Ищем строку с максимальным элементом в i-й колонке для перестановки
            max_row = max(range(i, self.n), key=lambda r: abs(self.matrix[r][i]))
            if max_row != i:
                # Перестановка строк
                self.matrix[i], self.matrix[max_row] = self.matrix[max_row], self.matrix[i]
                self.vector_b[i], self.vector_b[max_row] = self.vector_b[max_row], self.vector_b[i]

    def scale_matrix_and_vector(self):
        """
        Масштабирование матрицы и вектора b, чтобы привести их к одинаковому масштабу.
        """
        # Находим максимальные элементы в каждой строке
        row_scales = [max(abs(self.matrix[i][j]) for j in range(self.n)) for i in range(self.n)]
        max_b = max(abs(b) for b in self.vector_b)

        # Масштабируем строки матрицы и вектор b
        for i in range(self.n):
            if row_scales[i] != 0:
                scale_factor = 1 / row_scales[i]
                self.matrix[i] = [self.matrix[i][j] * scale_factor for j in range(self.n)]
                self.vector_b[i] *= scale_factor

        if max_b != 0:
            b_scale_factor = 1 / max_b
            self.vector_b = [b * b_scale_factor for b in self.vector_b]

    def norm(self, vector):
        """
        Вычисление нормы вектора (по методу максимума - L∞).
        :param vector: Вектор для расчета нормы.
        :return: Норма вектора.
        """
        return max(abs(x) for x in vector)

    def iterate(self):
        """
        Метод простых итераций для решения системы.
        """
        # Начальные значения (все элементы вектора x инициализируем нулями)
        x_old = [0] * self.n
        x_new = [0] * self.n
        iterations = 0
        epsilons = []  # Список для погрешностей на каждом шаге
        solution_history = []  # История решений для вывода

        while True:
            iterations += 1
            # Для каждой переменной вычисляем новое значение по формуле метода простых итераций
            for i in range(self.n):
                sum_terms = sum(self.matrix[i][j] * x_old[j] for j in range(self.n) if i != j)
                x_new[i] = (self.vector_b[i] - sum_terms) / self.matrix[i][i]

            # Вычисляем погрешности
            errors = [abs(x_new[i] - x_old[i]) for i in range(self.n)]
            epsilons.append(errors)  # Добавляем погрешности в историю

            solution_history.append(x_new[:])  # Сохраняем текущее решение для вывода

            # Если погрешность меньше заданной точности, выходим из цикла
            if self.norm(errors) < self.tolerance:
                break

            # Обновляем старое решение для следующей итерации
            x_old = x_new[:]

        return solution_history, epsilons, iterations

    def solve(self):
        """
        Решение системы уравнений.
        """
        # Проверка на диагональное преобладание
        if not self.check_diagonal_dominance():
            self.make_diagonal_dominance()

        # Масштабируем матрицу и вектор b
        self.scale_matrix_and_vector()

        # Решаем методом простых итераций
        solution_history, epsilons, iterations = self.iterate()

        # Выводим результаты
        print("№  | x1        | x2        | x3       | eps1        | eps2       | eps3       |")
        for i in range(iterations):
            row = f"{i} | " + " | ".join(f"{val: .6f}" for val in solution_history[i]) + " | " + " | ".join(f"{eps: .6f}" for eps in epsilons[i])
            print(row)

        # Вывод решения
        print("\nРешение системы:")
        for i, sol in enumerate(solution_history[-1]):
            print(f"[{i + 1}] = {sol:.25f}")

        # Вывод вектора невязки (разница между матрицей A и вектором b)
        residuals = [sum(self.matrix[i][j] * solution_history[-1][j] for j in range(self.n)) - self.vector_b[i] for i in range(self.n)]
        print("\nВектор невязки:")
        for i, res in enumerate(residuals):
            print(f"[{i + 1}] = {res:.12f}")


def input_matrix_and_tolerance_from_console():
    """
    Ввод матрицы и точности с клавиатуры с проверками на корректность.
    :return: Матрица и точность.
    """
    while True:
        try:
            n = int(input("Введите размерность системы (n <= 20): "))
            if n <= 0 or n > 20:
                raise ValueError("Размерность должна быть положительным числом, не превышающим 20.")
            break
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте снова.")

    matrix = []
    vector_b = []  # Инициализируем вектор свободных членов

    print(
        "Введите элементы матрицы A и вектора свободных членов (каждый элемент строки через пробел, свободный член - последний):")
    for i in range(n):
        while True:
            try:
                row = list(map(float, input(f"Введите {i + 1}-ю строку матрицы через пробел: ").split()))
                if len(row) != n + 1:
                    raise ValueError(
                        f"Количество элементов в строке должно быть {n + 1} (для матрицы и свободного члена).")
                matrix.append(row[:-1])  # Все элементы, кроме последнего, идут в матрицу
                vector_b.append(row[-1])  # Последний элемент строки - свободный член
                break
            except ValueError as e:
                print(f"Ошибка: {e}. Попробуйте снова.")

    while True:
        try:
            tolerance = float(input("Введите точность: "))
            if tolerance <= 0:
                raise ValueError("Точность должна быть положительным числом.")
            break
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте снова.")

    return matrix, vector_b, tolerance


def input_matrix_and_tolerance_from_file(filename):
    """
    Ввод матрицы и точности из файла с проверками на корректность.
    :param filename: Путь к файлу с данными.
    :return: Матрица и точность.
    """
    matrix = []
    vector_b = []

    try:
        with open(filename, 'r') as file:
            n = int(file.readline().strip())
            if n <= 0 or n > 20:
                raise ValueError("Размерность системы должна быть положительным числом, не превышающим 20.")

            for i in range(n):
                row = list(map(float, file.readline().strip().split()))
                if len(row) != n + 1:
                    raise ValueError(
                        f"Количество элементов в строке должно быть {n + 1} (для матрицы и свободного члена).")
                matrix.append(row[:-1])  # Все элементы, кроме последнего, идут в матрицу
                vector_b.append(row[-1])  # Последний элемент строки - свободный член

            tolerance = float(file.readline().strip())
            if tolerance <= 0:
                raise ValueError("Точность должна быть положительным числом.")

    except (ValueError, IndexError, FileNotFoundError) as e:
        print(f"Ошибка при чтении файла: {e}. Проверьте файл и попробуйте снова.")
        return None, None, None

    return matrix, vector_b, tolerance


def main():
    """
    Основная функция, которая запускает программу.
    """
    while True:  # Бесконечный цикл для перезапуска в случае неверного выбора
        # Выбор источника ввода
        choice = input("Вы хотите ввести данные из файла или с консоли? (file/console/exit): ").strip().lower()

        if choice == "file":
            filename = input("Введите имя файла: ").strip()
            matrix, vector_b, tolerance = input_matrix_and_tolerance_from_file(filename)
            if matrix is None:  # Если произошла ошибка при чтении файла, перезапускаем
                continue
            # Создаем объект метода
            method = IterativeMethod(matrix, vector_b, tolerance)
            # Запускаем решение
            method.solve()
            #break  # Выход из цикла после успешного решения

        elif choice == "console":
            matrix, vector_b, tolerance = input_matrix_and_tolerance_from_console()
            # Создаем объект метода
            method = IterativeMethod(matrix, vector_b, tolerance)
            # Запускаем решение
            method.solve()
            #break  # Выход из цикла после успешного решения

        elif choice == "exit":
            print("Выход из программы.")
            break  # Завершаем выполнение программы

        else:
            print("Неверный выбор, пожалуйста, выберите 'file', 'console' или 'exit'.")


if __name__ == "__main__":
    main()
