from bubble_sort import bubble_sort_optimized
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
    best_case = list(i for i in range(n))
    average_case = list(i for i in random.sample(range(n), n))
    worst_case = list(i for i in range(n - 1, -1, -1))

    start_time = time.time()
    bubble_sort_optimized(best_case)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Best case with n={n}: {elapsed_time:.6f} seconds")

    start_time = time.time()
    bubble_sort_optimized(worst_case)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Worst case with n={n}: {elapsed_time:.6f} seconds")

    start_time = time.time()
    bubble_sort_optimized(average_case)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Average case with n={n}: {elapsed_time:.6f} seconds")

    print()

    n += increment
