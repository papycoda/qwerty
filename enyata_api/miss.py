def findFirstMissingPositive(arr):
    n = len(arr)

    # If the array is empty, return 1
    if n == 0:
        return 1

    for i in range(n):
        while 1 <= arr[i] <= n and arr[arr[i] - 1] != arr[i]:

            arr[arr[i] - 1], arr[i] = arr[i], arr[arr[i] - 1]

    for i in range(n):
        if arr[i] != i + 1:
            return i + 1

    return n + 1
