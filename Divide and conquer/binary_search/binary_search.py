def binary_search(arr, target):
    """
    Realiza una búsqueda binaria en una lista ordenada.

    :param arr: Lista ordenada de elementos.
    :param target: Elemento a buscar.
    :return: Índice del elemento si se encuentra, de lo contrario -1.
    """
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2
        mid_val = arr[mid]

        if mid_val == target:
            return mid
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
