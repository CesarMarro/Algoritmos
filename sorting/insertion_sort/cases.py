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
iterations = 5

for _ in range(iterations + 1):
    print("-------------------------NEW ITERATION--------------------")
    print()
    print()
    best_case = list(range(n))
    average_case = [random.randint(0, n) for _ in range(n)]
    worst_case = list(range(n, 0, -1))

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
