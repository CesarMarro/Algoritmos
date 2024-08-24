from bubble_sort import bubble_sort_optimized
import time
import random


print("-------------------------INICIO--------------------")
print()
print()
print()
print()

# Se hacen 5 iteraciones, sumando 2500 a los arrays cada vez. Asi se tienen 5 puntos de referencia
n = 5000
increment = 2500
iterations = 5

for _ in range(iterations + 1):
    print("-------------------------NEW ITERATION--------------------")
    print()
    print()

    # El best case se da cuando un array ya está ordenado
    best_case = list(i for i in range(n))

    # El caso promedio se da cuando un array está desordenado aleatoreamente
    average_case = list(i for i in random.sample(range(n), n))

    # El worst case se da cuando un array está inversamente ordenado
    worst_case = list(i for i in range(n - 1, -1, -1))

    # Contar el tiempo y correr el best case
    start_time = time.time()
    bubble_sort_optimized(best_case)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Best case with n={n}: {elapsed_time:.6f} seconds")

    # Contar el tiempo y correr el worst case
    start_time = time.time()
    bubble_sort_optimized(worst_case)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Worst case with n={n}: {elapsed_time:.6f} seconds")

    # Contar el tiempo y correr el avg case
    start_time = time.time()
    bubble_sort_optimized(average_case)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Average case with n={n}: {elapsed_time:.6f} seconds")

    print()

    # Se le suma el increment al array
    n += increment
