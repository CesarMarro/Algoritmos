from memory_profiler import profile


@profile
def bubble_sort(arr):
    for i in range(0, len(arr)):
        for j in range(0, len(arr) - 1):

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


@profile
def bubble_sort_optimized(arr):
    for i in range(0, len(arr)):
        sorted = True
        for j in range(0, len(arr) - 1 - i):

            if arr[j] > arr[j + 1]:
                sorted = False
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
        if sorted:
            return
    return arr
