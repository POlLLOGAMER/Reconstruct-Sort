
# README.md: In-Place Integer Sorting Algorithm (Reconstruct-Sort or Counting Sort 2)


## Overview

The code sorts a list of integers with the following critical conditions:

*   **Limited Range:**  All numbers in the list must be in the range `[0, n)`, where `n` is the length of the list.  This constraint is *essential* for the algorithm's functionality. The `inplace_sorting` function checks this at the beginning:

    ```python
    for num in list:
        if not (0 <= num < n):
            raise ValueError("All numbers must be in the range [0, n)")
    ```

    If any number falls outside this range, a `ValueError` is raised.

*   **In-Place Sorting:** The algorithm modifies the original list directly, minimizing the need for extra memory.

## Core Idea: Using the List as a Hash Table (Counter)

The central concept is using the input list itself to count the frequencies of each number. Instead of a dictionary or hash table, the list cleverly serves as a "makeshift" counter.

### Step 1: Counting Frequencies (In-Place)

```python
for i in range(n):
    index = list[i] % n
    list[index] += n
```

*   `index = list[i] % n`:  This is the core trick.  It takes the current value of `list[i]` and calculates the remainder when divided by `n`.  Since all original numbers are in the range `[0, n)`, the result of `% n` will always be a valid index within the list (i.e., a number between 0 and n-1).  Essentially, we're using the *original* value of `list[i]` (modulo n) as the key in our "hash table."

*   `list[index] += n`:  This is where we "count." We increment the value at the `index` position by `n`.  Why `n`?  Because we need a way to distinguish between the original value that might have been at `list[index]` and the "count" we're adding.  By adding `n`, we ensure the "count" is in the "tens," "hundreds," etc. place (if we think of `n` as the base of a number system), while the original value (which is always less than `n`) is in the "ones" place.

*   **Example:**  Suppose `n = 10` and `list = [2, 0, 1, 2, 3, 0, 0, 4, 9, 7]`.  Let's see how the list is modified in this step:

    *   `i = 0`: `list[0] = 2`. `index = 2 % 10 = 2`. `list[2] += 10`, so `list[2]` becomes `1 + 10 = 11`.

    *   `i = 1`: `list[1] = 0`. `index = 0 % 10 = 0`. `list[0] += 10`, so `list[0]` becomes `2 + 10 = 12`.

    *   `i = 2`: `list[2] = 11`. `index = 11 % 10 = 1`. `list[1] += 10`, so `list[1]` becomes `0 + 10 = 10`.

    *   `i = 3`: `list[3] = 2`. `index = 2 % 10 = 2`. `list[2] += 10`, so `list[2]` becomes `11 + 10 = 21`.

    *   ...and so on.

    At the end, the list will be something like `[32, 10, 21, 13, 14, 0, 0, 17, 0, 19]`.

### Step 2: Reconstructing the Sorted List (In-Place)

```python
pos = 0
temp = [0] * n

for i in range(n):
    freq = list[i] // n
    for _ in range(freq):
        temp[pos] = i
        pos += 1

for i in range(n):
    list[i] = temp[i]
```

*   `freq = list[i] // n`: Here, we retrieve the frequency of each number. We use integer division (`//`) by `n`.  Remember that in step 1, we added `n` to `list[index]` for each occurrence of the number `index`.  Therefore, dividing by `n` gives us how many times we added `n`, which is precisely the frequency of the number `i`.  In the example above, `list[0] = 32`, so `freq = 32 // 10 = 3`.  This means the number 0 appeared 3 times in the original list.

*   **Inner Loop:** The inner loop (`for _ in range(freq):`) executes `freq` times. In each iteration, it places the number `i` in the correct position in the `temp` list. `pos` is used as an index to know where to place the next number. `temp` is used as an auxiliary list to avoid overwriting important values in the original list prematurely.

*   **Final Copy:** After reconstructing the sorted list in `temp`, it's copied back to `list` to store the result in the original list.

## Considerations and Limitations

*   **Time Complexity:** The time complexity is O(n). Both the counting and reconstruction steps iterate through the list a constant number of times.

*   **Space Complexity:** The space complexity is O(1), nearly. The auxiliary list `temp` of the same size as the input is used; however, the complexity is considered O(1) since the original list is modified in place. This is what makes the algorithm "in-place."

*   **Range Limitation:** The restriction of the range `[0, n)` is fundamental. If the numbers were larger than `n`, the `% n` technique wouldn't work, and data would be overwritten. If the numbers were negative, it also wouldn't work correctly.

*   **Integers Only:** The algorithm works with integers. It wouldn't work directly with floating-point numbers, for example.

## Complete Example

Let's use the input `my_list = [2, 0, 1, 2, 3, 0, 0, 4, 9, 7]` and `n = 10`.

### Counting Frequencies:

*   **Initially:** `[2, 0, 1, 2, 3, 0, 0, 4, 9, 7]`

*   **After Iterating:** `[32, 10, 21, 13, 14, 0, 0, 17, 0, 19]` (as explained before)

### Reconstructing the List:

*   `i = 0`: `freq = 32 // 10 = 3`. `temp` becomes `[0, 0, 0, ...]`. `pos = 3`.

*   `i = 1`: `freq = 10 // 10 = 1`. `temp` becomes `[0, 0, 0, 1, ...]`. `pos = 4`.

*   `i = 2`: `freq = 21 // 10 = 2`. `temp` becomes `[0, 0, 0, 1, 2, 2, ...]`. `pos = 6`.

*   `i = 3`: `freq = 13 // 10 = 1`. `temp` becomes `[0, 0, 0, 1, 2, 2, 3, ...]`. `pos = 7`.

*   ...

*   `i = 9`: `freq = 19 // 10 = 1`. `temp` becomes `[0, 0, 0, 1, 2, 2, 3, 4, 7, 9]`. `pos = 10`.

Finally, `temp` is copied to `my_list`.

Here is the code of Deconstruct Sort:

```
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
```

# A continuacion veran una grafica el cual refleja la relacion tiempo-operacion de este algoritmo
![Texto alternativo](/Graph.png)
