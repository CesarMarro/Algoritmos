from memory_profiler import profile


@profile
def counting_sort(arr):

    k = max(arr) + 1

    c = [0] * k

    for i in range(len(arr)):
        c[arr[i]] += 1

    for i in range(1, k):
        c[i] = c[i] + c[i - 1]

    B = [None] * len(arr)

    for i in range(len(arr) - 1, -1, -1):
        c[arr[i]] -= 1
        B[c[arr[i]]] = arr[i]

    return B


# Example usage:
arr = [4, 2, 2, 8, 3, 3, 1]

print("Sorted array:", counting_sort(arr))
