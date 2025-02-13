
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

# Below you will see a graph which reflects the time-operation relationship of this algorithm
![Texto alternativo](/Graph.png)

Here is the code I used to create the performance graph for this algorithm:

```
import time
import random
import matplotlib.pyplot as plt

def inplace_sorting(list):
    n = len(list)
    operations = 0  # Variable para contar las operaciones

    # Check that all elements are in the range [0, n)
    for num in list:
        if not (0 <= num < n):
            raise ValueError("All numbers must be in the range [0, n)")

    # Step 1: Count frequencies in-place
    for i in range(n):
        index = list[i] % n
        list[index] += n
        operations += 1  # Operación de incremento

    # Step 2: Rebuild the sorted list (in-place)
    pos = 0
    temp = [0] * n  # Auxiliary list to help with sorting

    for i in range(n):
        freq = list[i] // n
        for _ in range(freq):
            temp[pos] = i
            pos += 1
            operations += 1  # Operación de asignación
    for i in range(n):
        list[i] = temp[i]
        operations += 1  # Operación de copia

    return list, operations

# Function to plot graph
def plot_operations():
    sizes = range(100000, 10000001, 1000000)  # From 100000 to 10 million in steps of 1000000
    operations_list = []

    for size in sizes:
        my_list = [random.randint(0, size - 1) for _ in range(size)]
        
        # Measure the number of operations performed by inplace_sorting
        _, operations = inplace_sorting(my_list)

        operations_list.append(operations)
        print(f"Size: {size}, Operations: {operations}")

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, operations_list, label="Number of Operations")
    plt.xlabel('List Size')
    plt.ylabel('Number of Operations')
    plt.title('Number of Operations of In-place Sorting vs List Size')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    plot_operations()

```
# Below I will give the code so that you can view this algorithm in p5.js:
```

/*
  p5.js Sketch: In-Place Frequency Sorting Animation

  This sketch animates an algorithm that sorts an array of size n,
  where every element is in the range [0, n). The algorithm works in two phases:
  
  1. Frequency Counting (in-place):
     For each element, compute its "bucket" index as (value % n) and add n to that bucket.
  
  2. Rebuilding the Sorted Array:
     For each index i, the frequency is (arr[i] // n). The number i is then inserted into a temporary
     array as many times as it appears.
  
  Adjustable settings:
    - n: the size of the array (and the range of values)
    - speed: animation speed (in milliseconds per frame)
  
  Enjoy the dangerously quirky arithmetic acrobatics!
*/

let n = 100;        // Array size (and the range [0, n) for each element)
let speed = 1;  // Time (in milliseconds) between animation frames

let frames = [];   // Array to store each animation frame (state)
let currentFrame = 0;
let lastFrameTime = 0;

function setup() {
  createCanvas(800, 600);
  frameRate(60);  // 60 fps—though we manually advance frames using our "speed" setting
  
  // Precompute the frames for the entire algorithm animation
  frames = generateFrames(n);
  lastFrameTime = millis();
}

function draw() {
  background(240);

  // Advance to the next frame if enough time has passed
  if (millis() - lastFrameTime > speed && currentFrame < frames.length - 1) {
    currentFrame++;
    lastFrameTime = millis();
  }
  
  // Display the current frame
  displayFrame(frames[currentFrame]);
}

/*  
  generateFrames(n)
  -----------------
  Simulates the algorithm step-by-step and records "frames" containing:
    - phase: Which part of the algorithm is active
    - description: A humorous description of the step
    - arr: A copy of the main array’s current state
    - temp: A copy of the temporary (sorted) array (if applicable)
    - highlight: Object to mark indices or positions being processed
*/
function generateFrames(n) {
  let frames = [];
  
  // Create the initial array with random integers in [0, n)
  let arr = [];
  for (let i = 0; i < n; i++) {
    arr.push(Math.floor(random(n)));
  }
  
  // Frame 0: Initial state
  frames.push({
    phase: "init",
    description: "Initial array: [" + arr.join(", ") + "]\nWatch these numbers misbehave!",
    arr: arr.slice(),
    highlight: null,
    temp: null
  });
  
  // --------------------------
  // Phase 1: Frequency Counting
  // --------------------------
  // For each element, compute the target bucket (using modulo) and add n to that bucket.
  for (let i = 0; i < n; i++) {
    let bucketIndex = arr[i] % n;
    
    // Frame: Before processing index i
    frames.push({
      phase: "freq",
      description: `Processing arr[${i}] = ${arr[i]}: targeting bucket ${bucketIndex}`,
      arr: arr.slice(),
      highlight: { current: i, bucket: bucketIndex },
      temp: null
    });
    
    // Perform the in-place update: add n to the bucket at index bucketIndex
    arr[bucketIndex] += n;
    
    // Frame: After updating the bucket
    frames.push({
      phase: "freq",
      description: `Added ${n} to bucket ${bucketIndex}. New value: ${arr[bucketIndex]}`,
      arr: arr.slice(),
      highlight: { current: i, bucket: bucketIndex },
      temp: null
    });
  }
  
  // Frame: After frequency counting is complete
  frames.push({
    phase: "after_freq",
    description: "After frequency counting: [" + arr.join(", ") + "]\nBuckets are bulging with frequency!",
    arr: arr.slice(),
    highlight: null,
    temp: null
  });
  
  // -------------------------------
  // Phase 2: Rebuilding the Sorted Array
  // -------------------------------
  let temp = new Array(n).fill(0);
  let pos = 0;
  
  for (let i = 0; i < n; i++) {
    // Calculate frequency: how many times the number i appears
    let freq = Math.floor(arr[i] / n);
    frames.push({
      phase: "rebuild",
      description: `Number ${i} appears ${freq} time(s). Preparing to insert...`,
      arr: arr.slice(),
      highlight: { bucket: i },
      temp: temp.slice()
    });
    
    // Insert the number i, freq times into the temp (sorted) array
    for (let count = 0; count < freq; count++) {
      temp[pos] = i;
      frames.push({
        phase: "rebuild",
        description: `Inserting ${i} at sorted position ${pos}. Chaos, meet order!`,
        arr: arr.slice(),
        highlight: { bucket: i, pos: pos },
        temp: temp.slice()
      });
      pos++;
    }
  }
  
  // Final frame: Sorted array completed!
  frames.push({
    phase: "final",
    description: "Final sorted array: [" + temp.join(", ") + "]\nOrder restored... for now!",
    arr: arr.slice(),
    highlight: null,
    temp: temp.slice()
  });
  
  return frames;
}

/*
  displayFrame(frame)
  --------------------
  Draws the current state of the algorithm:
    - The description text at the top.
    - The main array as a series of bars.
    - If applicable, the temporary (sorted) array as bars below.
  
  The function also highlights the indices or positions currently in action.
*/
function displayFrame(frame) {
  // Display the description text (with dangerously silly commentary)
  fill(0);
  textSize(16);
  textAlign(LEFT, TOP);
  text(frame.description, 20, 20);
  
  let margin = 20;
  
  // ---------------------
  // Draw the Main Array
  // ---------------------
  if (frame.arr) {
    let arr = frame.arr;
    let arrY = 100;      // y-coordinate for main array display
    let arrHeight = 200; // maximum height for bars
    let barAreaWidth = width - 2 * margin;
    let barWidth = barAreaWidth / arr.length;
    let maxVal = Math.max(...arr);
    
    // Label for main array
    textSize(14);
    textAlign(LEFT, CENTER);
    text("Main Array", margin, arrY - 20);
    
    for (let i = 0; i < arr.length; i++) {
      let val = arr[i];
      let barHeight = map(val, 0, maxVal, 0, arrHeight);
      let x = margin + i * barWidth;
      let y = arrY + (arrHeight - barHeight);
      
      // Default color for main array bars
      let col = color(100, 149, 237);  // cornflower blue
      
      // Highlight the current index or bucket if indicated
      if (frame.highlight) {
        if (frame.highlight.current === i || frame.highlight.bucket === i) {
          col = color(220, 20, 60);  // crimson for dramatic effect
        }
      }
      
      fill(col);
      rect(x, y, barWidth - 2, barHeight);
      
      // Display the numerical value above each bar
      fill(0);
      textAlign(CENTER, BOTTOM);
      text(arr[i], x + barWidth / 2, y - 5);
    }
  }
  
  // -------------------------
  // Draw the Temp (Sorted) Array
  // -------------------------
  if (frame.temp) {
    let temp = frame.temp;
    let tempY = 350;     // y-coordinate for temp array display
    let tempHeight = 150; // maximum bar height for temp array
    let barAreaWidth = width - 2 * margin;
    let barWidth = barAreaWidth / temp.length;
    let maxVal = Math.max(...temp, 1);  // ensure non-zero maximum
    
    // Label for temp array
    textSize(14);
    textAlign(LEFT, CENTER);
    text("Temp Array", margin, tempY - 20);
    
    for (let i = 0; i < temp.length; i++) {
      let val = temp[i];
      let barHeight = map(val, 0, maxVal, 0, tempHeight);
      let x = margin + i * barWidth;
      let y = tempY + (tempHeight - barHeight);
      
      // Default color for temp array bars
      let col = color(34, 139, 34);  // forest green
      
      // Highlight the current insertion position if applicable
      if (frame.highlight && frame.highlight.pos === i) {
        col = color(255, 140, 0);    // dark orange
      }
      
      fill(col);
      rect(x, y, barWidth - 2, barHeight);
      
      // Display the numerical value above each temp bar
      fill(0);
      textAlign(CENTER, BOTTOM);
      text(temp[i], x + barWidth / 2, y - 5);
    }
  }
}
```

# As you can see, it has only 1 constraint that has to be a force between 1 and n, but we can remove this constraint by adding maximum value, and here is the code without that constraint:
```
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

```
# Benchmarks
As you can see when the k (range) is small, counting sort and Deconstruction sort (Counting sort 2) have the same performance but when we increase the range for example to 1 million, we clearly see the difference between these 2, because 1 is O(n+k) and another is O(n):
![](/1millonrage.png)
```
import random
import matplotlib.pyplot as plt

# In-place Sorting Algorithm (Counting Sort 2)
def inplace_sorting(lst, max_val):
    n = len(lst)
    operations = 0  # Operation counter
    for num in lst:
        if not (0 <= num <= max_val):  # Ensure numbers are within range
            raise ValueError(f"All numbers must be in the range [0, {max_val}]")

    # Perform frequency count using "in-place" technique
    for i in range(n):
        index = lst[i] % (max_val + 1)  # Generate index within a valid range
        if index < n:
            lst[index] += n  # Add n to mark the value without overwriting the list
        operations += 1  # Count operation

    pos = 0
    temp = [0] * n
    for i in range(n):
        freq = lst[i] // (max_val + 1)  # Get the frequency
        for _ in range(freq):
            temp[pos] = i
            pos += 1
        operations += 1  # Count operation
    for i in range(n):
        lst[i] = temp[i]
        operations += 1  # Count operation
    return lst, operations

# Classic Counting Sort Algorithm
def counting_sort(lst, max_val):
    operations = 0  # Operation counter
    count = [0] * (max_val + 1)  # Use max_val + 1
    output = [0] * len(lst)
    for num in lst:
        count[num] += 1
        operations += 1  # Count operation
    for i in range(1, max_val + 1):
        count[i] += count[i - 1]
        operations += 1  # Count operation
    for num in reversed(lst):
        output[count[num] - 1] = num
        count[num] -= 1
        operations += 1  # Count operation
    return output, operations

# Radix Sort Algorithm
def radix_sort(lst, max_val):
    operations = 0  # Operation counter
    RADIX = 10
    placement = 1
    while max_val // placement > 0:
        buckets = [list() for _ in range(RADIX)]
        for i in lst:
            buckets[i // placement % RADIX].append(i)
            operations += 1  # Count operation
        a = 0
        for bucket in buckets:
            for i in bucket:
                lst[a] = i
                a += 1
                operations += 1  # Count operation
        placement *= RADIX
    return lst, operations

# Function to plot operations
def plot_operations():
    max_val = 1000000  # Set k to 1 million
    sizes = range(1000, 10001, 1000)  # From 1k to 10k in steps of 1k
    inplace_ops = []
    counting_ops = []
    radix_ops = []

    for size in sizes:
        # Create a random list with values up to 1 million
        my_list = [random.randint(0, max_val) for _ in range(size)]

        # Measure operations for In-place Sorting (Counting Sort 2)
        _, inplace_ops_count = inplace_sorting(my_list[:], max_val)
        inplace_ops.append(inplace_ops_count)

        # Measure operations for Classic Counting Sort
        _, counting_ops_count = counting_sort(my_list[:], max_val)
        counting_ops.append(counting_ops_count)

        # Measure operations for Radix Sort
        _, radix_ops_count = radix_sort(my_list[:], max_val)
        radix_ops.append(radix_ops_count)

        print(f"Size: {size}, In-place Operations: {inplace_ops[-1]}, Counting Operations: {counting_ops[-1]}, Radix Operations: {radix_ops[-1]}")

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, inplace_ops, label="In-place Sorting (Counting Sort 2)", color='blue')
    plt.plot(sizes, counting_ops, label="Classic Counting Sort", color='green')
    plt.plot(sizes, radix_ops, label="Radix Sort", color='red')
    plt.xlabel('List Size')
    plt.ylabel('Operations Count')
    plt.title('Operations Count Comparison: Sorting Algorithms')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    plot_operations()
```
## Version 2
In version 2, which is the code you will see below, I removed the restriction that the max value always had to be less than the size of the list, here is the code:

```
import random
import time

def flexible_inplace_sort(lst, max_val):
    n = len(lst)
    
    # Validate that each number is in the range [0, max_val]
    for num in lst:
        if num < 0 or num > max_val:
            raise ValueError(f"All numbers must be in the range [0, {max_val}]")

    # Case 1: If max_val < n, use the optimized O(n) version
    if max_val < n:
        multiplier = n  # n is greater than any value in the list
        # Count frequencies using the same list
        for i in range(n):
            index = lst[i] % multiplier
            lst[index] += n
        
        # Reconstruct the sorted list
        pos = 0
        temp = [0] * n
        for i in range(max_val + 1):
            freq = lst[i] // multiplier
            for _ in range(freq):
                temp[pos] = i
                pos += 1
        for i in range(n):
            lst[i] = temp[i]
        return lst

    # Case 2: If max_val >= n, use the "original" Deconstruction Sort version
    else:
        # Perform frequency counting using the "in-place" technique
        for i in range(n):
            index = lst[i] % (max_val + 1)
            if index < n:
                lst[index] += n  # Mark the frequency by adding n
        
        pos = 0
        temp = [0] * n
        for i in range(n):
            freq = lst[i] // (max_val + 1)
            for _ in range(freq):
                temp[pos] = i
                pos += 1
        for i in range(n):
            lst[i] = temp[i]
        
        return lst


# Example usage:
if __name__ == "__main__":
    # You can test with different sizes and ranges
    max_val = 10000**10000  # Test with a giant max_val
    size = 10000        # List size
    my_list = [random.randint(0, max_val) for _ in range(size)]

    start_time = time.time()
    sorted_list = flexible_inplace_sort(my_list, max_val)
    print(f"Sorted list in {time.time() - start_time} seconds.")

```
Here is the version that measures the operations:

```
import random
import time

def flexible_inplace_sort(lst, max_val):
    n = len(lst)
    operations = 0  # Variable to count operations
    
    # Validate that each number is in the range [0, max_val]
    for num in lst:
        if num < 0 or num > max_val:
            raise ValueError(f"All numbers must be in the range [0, {max_val}]")
        operations += 1  # Validation operation

    # Case 1: If max_val < n, we use the optimized O(n) version
    if max_val < n:
        multiplier = n  # n is greater than any value in the list
        # Count frequencies using the same list
        for i in range(n):
            index = lst[i] % multiplier
            lst[index] += n
            operations += 1  # Loop operation

        # Rebuild the sorted list
        pos = 0
        temp = [0] * n
        for i in range(max_val + 1):
            freq = lst[i] // multiplier
            for _ in range(freq):
                temp[pos] = i
                pos += 1
                operations += 1  # Loop operation
        for i in range(n):
            lst[i] = temp[i]
            operations += 1  # Loop operation
        return lst, operations

    # Case 2: If max_val >= n, we use the "original" Deconstruction Sort version
    else:
        # Perform frequency counting using the "in-place" technique
        for i in range(n):
            index = lst[i] % (max_val + 1)
            if index < n:
                lst[index] += n  # Mark the frequency by adding n
            operations += 1  # Loop operation
        
        pos = 0
        temp = [0] * n
        for i in range(n):
            freq = lst[i] // (max_val + 1)
            for _ in range(freq):
                temp[pos] = i
                pos += 1
                operations += 1  # Loop operation
        for i in range(n):
            lst[i] = temp[i]
            operations += 1  # Loop operation
        
        return lst, operations


# Example usage:
if __name__ == "__main__":
    max_val = 10000**10000  # Test with a giant max_val
    size = 10000        # List size
    my_list = [random.randint(0, max_val) for _ in range(size)]

    start_time = time.time()
    sorted_list, operations = flexible_inplace_sort(my_list, max_val)
    end_time = time.time()

    print(f"Sorted list in {end_time - start_time} seconds.")
    print(f"Operations performed: {operations}")
```
