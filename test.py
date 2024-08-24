import time

from sorting.bubble_sort import bubble_sort, bubble_sort_optimized

arr = [5, 2, 4, 6, 1, -7, 3, -100, 99, -97, 98]

n = 100000
test_arr = [i for i in range(n, 0, -1)]

start_time = time.time()
bubble_sort(test_arr)
end_time = time.time()

total_time = end_time - start_time
print("sorted array: ", test_arr)
print("Time taken: ", total_time)
