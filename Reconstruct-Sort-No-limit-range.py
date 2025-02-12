import random
import time

# Deconstruction sort algorithm (In-place Sorting)
def inplace_sorting(lst, max_val):
    n = len(lst)
    for num in lst:
        if not (0 <= num <= max_val):  # Ensure the numbers are within the range
            raise ValueError(f"All numbers must be in the range [0, {max_val}]")

    # Perform the frequency counting using the "in-place" technique
    for i in range(n):
        index = lst[i] % (max_val + 1)  # Generate the index within a valid range
        if index < n:
            lst[index] += n  # Add n to mark the value without overwriting the list

    pos = 0
    temp = [0] * n
    for i in range(n):
        freq = lst[i] // (max_val + 1)  # Get the frequency
        for _ in range(freq):
            temp[pos] = i
            pos += 1
    for i in range(n):
        lst[i] = temp[i]
    return lst

if __name__ == "__main__":
    # Generate a random list with values up to 1 million
    max_val = 1000000
    size = 10000  # List size (you can change it)
    my_list = [random.randint(0, max_val) for _ in range(size)]

    # Sort the list using Counting Sort 2
    start_time = time.time()
    sorted_list = inplace_sorting(my_list, max_val)
    print(f"List sorted in {time.time() - start_time} seconds.")
