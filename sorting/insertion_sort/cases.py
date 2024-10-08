from insertion_sort import insertion_sort
import time
import random


print("-------------------------INICIO--------------------")
print()
print()
print()
print()

n = 5000
increment = 2500
iterations = 4

for _ in range(iterations + 1):
    print("-------------------------NEW ITERATION--------------------")
    print()
    print()

    # El best case se da cuando la lista esta ordenada
    best_case = list(i for i in range(n))

    # Avg case es cuando la lista esta aleatoreamente ordenada
    average_case = list(random.randint(0, n) for _ in range(n))

    # worst_case es cuando la lista esta ordeanda inversamente
    worst_case = list(i for i in range(n - 1, -1, -1))

    start_time = time.time()
    insertion_sort(best_case)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Best case with n={n}: {elapsed_time:.6f} seconds")

    start_time = time.time()
    insertion_sort(average_case)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Average case with n={n}: {elapsed_time:.6f} seconds")

    start_time = time.time()
    insertion_sort(worst_case)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Worst case with n={n}: {elapsed_time:.6f} seconds")

    print()

    n += increment
