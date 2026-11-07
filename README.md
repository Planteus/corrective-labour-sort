# 🏆 Democratic Sort

**Democratic Sort** is an adaptive, highly stable, bidirectional sorting algorithm born out of a structural engineering solution to the joke algorithm *Stalin Sort*.

While standard Stalin Sort achieves O(N) efficiency by permanently "purging" (deleting) any element that is out of order, **Democratic Sort** operates on a strict zero-exile policy. Disordered elements are moved into independent groupings, optimized via a breakthrough **Adaptive Reset** logic, and combined through a balanced tournament-style merge tree.

---

## 🧬 Novel Architecture Features

### 1. The Adaptive Reset Threshold
Most filters drop elements into a "wrong list" blindly. Democratic Sort implements a **10% Threshold Reset**. If a filtering sweep encounters a value that plunges below 10% of the current established peak, the algorithm adapts: it seals the current group, resets the local boundary, and instantly begins a fresh run from that point. This massively decreases the volume of out-of-order spillover and minimizes the total sublist count.

### 2. Alternating Bidirectional Sweeps
The algorithm processes left-to-right to harvest ascending peaks, then turns right-to-left to collect escalating valleys. This dual-action dynamic strips away external extremes from random data distributions in half the time.

### 3. Lookahead Run Detection
Before firing an extraction pass, a scanner verifies if the upcoming array chunk is already naturally sorted or perfectly reversed. If found, it is harvested instantly, bypassing execution logic entirely to guarantee immediate \(\mathcal{O}(N)\) performance on structured data.

### 4. Tournament-Style Tree Merge
Instead of appending small lists to a single inflating master array (which creates heavy \(\mathcal{O}(N^2)\) tracking overhead), elements are paired off systematically in balanced rounds: `(1+2), (3+4)`. This enforces an explicit runtime ceiling of \(\mathcal{O}(N \log N)\).

---

## 🎛️ Flavors and System Variations

Democratic Sort features a built-in controller that measures data entropy under the hood to deploy three optional engines:

1. **Classic Backend (Structural):** Allocates decoupled structural lists to ensure thread isolation and full immutability compatibility.
2. **Parallel Backend (Multi-Threaded):** Dynamically deploys an OS `ThreadPoolExecutor` if the matrix volume (\(N \cdot \log_2 K\)) crosses the runtime coordination threshold, running parallel tournament brackets across distinct CPU cores.
3. **Compact Backend (In-Place / O(1) Memory):** Uses a Two-Pointer element swap structure inside a single memory block for extreme, low-RAM computing profiles.

---

## 📊 Complexity Analysis

| State | Time Complexity | Memory Space |
| :--- | :--- | :--- |
| **Best Case (Pre-Sorted)** | \(\mathcal{O}(N)\) | \(\mathcal{O}(N)\) |
| **Ideal Case (Perfectly Reversed)** | \(\mathcal{O}(N)\) | \(\mathcal{O}(N)\) |
| **Worst Case (Pure Random Chaos)** | \(\mathcal{O}(N \log N)\) | \(\mathcal{O}(N)\) |
| **Compact Variant Profile** | \(\mathcal{O}(N \log N)\) | \(\mathcal{O}(1)\) |

---

## 🛠️ Usage Example

```python
from democratic_sort import democratic_sort

# Unsorted high-entropy sample
data = [5, 1, 99, 2, 8, 4, 3, 0.5, 88, 7]

# Executing structural auto-switching sort
sorted_data = democratic_sort(data)
print(sorted_data)
# Output: [0.5, 1, 2, 3, 4, 5, 7, 8, 88, 99]
```

## 📜 License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it in your open-source repositories.
    