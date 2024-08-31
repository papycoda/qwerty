def findFirstMissingPositive(arr):
    n = len(arr)
    
    # If the array is empty, return 1
    if n == 0:
        return 1

    # Rearrange the elements in the array
    for i in range(n):
        while 1 <= arr[i] <= n and arr[arr[i] - 1] != arr[i]:
            # Swap the elements
            arr[arr[i] - 1], arr[i] = arr[i], arr[arr[i] - 1]
    
    # Find the first missing positive
    for i in range(n):
        if arr[i] != i + 1:
            return i + 1

    return n + 1


