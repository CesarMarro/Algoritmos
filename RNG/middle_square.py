import numpy as np  # Asegúrate de importar numpy


def middle_square(n, seed=1234):
    """
    Genera una secuencia de números pseudoaleatorios utilizando el método del Cuadrado Medio.

    :param n: Número de números aleatorios a generar.
    :param seed: Semilla inicial (número entero).
    :return: Numpy array de números aleatorios normalizados entre 0 y 1.
    """
    rand_nums = []
    x = seed

    for _ in range(n):
        square = x * x
        square_str = str(square).zfill(8)  # Asegura que tenga al menos 8 dígitos
        middle_digits = square_str[2:6]  # Extrae los dígitos centrales
        x = int(middle_digits)
        if x == 0:
            x = seed  # Reinicia con la semilla si x es 0 para evitar ciclos de ceros
        rand_nums.append(x)

    return np.array(rand_nums) / 10000.0  # Normaliza los números entre 0 y 1
