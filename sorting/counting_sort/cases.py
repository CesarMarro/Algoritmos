from counting_sort import counting_sort
import time
import random


print("-------------------------INICIO--------------------")
print()
print()
print()
print()

n = 5000
increment = 2500
iterations = 5

for _ in range(iterations + 1):
    print("-------------------------NEW ITERATION--------------------")
    print()
    print()

    # El best case se da cuando el rango de numeros en una lista es pequeño, por eso solo hay numeros del 1 al 10
    best_case = list(random.randint(0, 10) for _ in range(n))

    # El average case se da cuando una lista está aleatoriamente ordenada con un rango regular
    average_case = list(random.randint(0, n) for _ in range(n))

    # El worst case se da cuando el rango de los numeros es muy alto, cuando se trabaja con numeros grandes
    worst_case = list(random.randint(0, 10 * n) for _ in range(n))

    # Best case
    start_time = time.time()
    counting_sort(best_case)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Best case with n={n}: {elapsed_time:.6f} seconds")

    # avg case
    start_time = time.time()
    counting_sort(average_case)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Average case with n={n}: {elapsed_time:.6f} seconds")

    # worst case
    start_time = time.time()
    counting_sort(worst_case)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Worst case with n={n}: {elapsed_time:.6f} seconds")

    print()

    n += increment
