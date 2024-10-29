import random
import time
from multiprocessing import Pool, cpu_count

# Generación del arreglo desordenado
arreglo_desordenado = random.sample(range(1, 10000001), 10000000)


def merge(left_arr, right_arr):
    merged = []
    i, j = 0, 0
    left_arr.append(float('inf'))
    right_arr.append(float('inf'))
    while left_arr[i] != float('inf') or right_arr[j] != float('inf'):
        if left_arr[i] < right_arr[j]:
            merged.append(left_arr[i])
            i += 1
        else:
            merged.append(right_arr[j])
            j += 1
    left_arr.pop()
    right_arr.pop()
    return merged


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

# Función de merge sort paralelo
def parallel_merge_sort(array):
    num_cores = cpu_count()
    sub_arrays = [array[i::num_cores] for i in range(num_cores)]
    start_time = time.time()
    with Pool(processes=num_cores) as pool:
        sorted_subarrays = pool.map(merge_sort, sub_arrays)
    result = sorted_subarrays[0]
    for sorted_subarray in sorted_subarrays[1:]:
        result = merge(result, sorted_subarray)
    end_time = time.time()
    print("Tiempo de ejecución del merge sort paralelo:", end_time - start_time, "segundos")
    return result

if __name__ == "__main__":
    # Ejecución del merge sort paralelo
    parallel_merge_sort(arreglo_desordenado)
