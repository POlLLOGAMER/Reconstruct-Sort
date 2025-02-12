import time
import random

def inplace_sorting(list):
    n = len(list)

    # Check that all elements are in the range [0, n)
    # (If they are not, these cases should be handled separately)
    for num in list:
        if not (0 <= num < n):
            raise ValueError("All numbers must be in the range [0, n)")

    # -------------------------------
    # Step 1: Count frequencies in-place
    # -------------------------------
    for i in range(n):
        # Get the original value (in case it has already been modified)
        index = list[i] % n
        # Increment the corresponding position by n
        list[index] += n

    # -------------------------------
    # Step 2: Rebuild the sorted list (in-place)
    # -------------------------------
    pos = 0  # position in the list to write
    temp = [0] * n  # Use an auxiliary variable to help with sorting

    # Rebuild the sorted list without overwriting values
    for i in range(n):
        freq = list[i] // n  # how many times the number i appears
        for _ in range(freq):
            temp[pos] = i
            pos += 1

    # Copy the content of the auxiliary list to the original list
    for i in range(n):
        list[i] = temp[i]

    return list

# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    my_list = [random.randint(0, 999) for _ in range(1000)]  # All are in [0, 10) and n = 10
    print("List before sorting:", my_list [:10])

    start = time.time()
    inplace_sorting(my_list)
    end = time.time()

    print("List after sorting:", my_list [:10])
    print("Execution time: {:.6f} seconds".format(end - start))
