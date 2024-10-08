import time
import xlsxwriter
from fibonacci_dynamic import fibonacci as dynamic
from fibonacci_recursive import fibonacci as recursive

n_values = []
recursive_times = []
dynamic_times = []


def measure_times(n):
    # Medir tiempo para Fibonacci dinámico
    start_dynamic = time.perf_counter()
    dynamic(n)
    end_dynamic = time.perf_counter()
    dynamic_time = end_dynamic - start_dynamic

    # Medir tiempo para Fibonacci recursivo
    start_recursive = time.perf_counter()
    recursive(n)
    end_recursive = time.perf_counter()
    recursive_time = end_recursive - start_recursive

    return dynamic_time, recursive_time


time_difference = 0
n = 1

# Bucle hasta 30 minutos de diferencia
while time_difference < 1800:

    dynamic_time, recursive_time = measure_times(n)

    n_values.append(n)
    dynamic_times.append(dynamic_time)
    recursive_times.append(recursive_time)

    time_difference = recursive_time - dynamic_time

    n += 1


workbook = xlsxwriter.Workbook("fibonacci_time_comparison.xlsx")
worksheet = workbook.add_worksheet()

# cabeceras
worksheet.write(0, 0, "N")
worksheet.write(0, 1, "Fibonacci Recursivo")
worksheet.write(0, 2, "Fibonacci Dinámico")


for i in range(len(n_values)):
    worksheet.write(i + 1, 0, n_values[i])
    worksheet.write(i + 1, 1, recursive_times[i])
    worksheet.write(i + 1, 2, dynamic_times[i])


workbook.close()

print("Archivo Excel 'fibonacci_time_comparison.xlsx' generado exitosamente.")
