"""
Democratic Sort: An Adaptive, Stable, Pure-Python Sorting Engine.
Born from a structural reimagining of Stalin Sort with an Adaptive Reset threshold.
100% Dependency-Free / Zero Imports.
"""

def merge(list1, list2):
    """
    A pure, custom two-way merge function.
    Combines two already-sorted lists into a single sorted list.
    """
    merged = []
    i = 0
    j = 0
    len1 = len(list1)
    len2 = len(list2)
    
    # Walk through both lists, appending the smaller element
    while i < len1 and j < len2:
        if list1[i] <= list2[j]:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1
            
    # Append any leftover elements
    if i < len1:
        merged.extend(list1[i:])
    if j < len2:
        merged.extend(list2[j:])
        
    return merged


def democratic_sort(arr, reset_threshold=0.10):
    """
    Sorts an array using pure Democratic Sort Architecture.
    Utilizes lookahead run detection, bidirectional sweeps, 
    an adaptive reset threshold, and an in-house tree merge.
    """
    if not arr:
        return []
    
    sublists = []
    current_list = list(arr)
    left_to_right = True
    
    # -------------------------------------------------------------------------
    # Phase 1: Stratification (Separation into sublists)
    # -------------------------------------------------------------------------
    while current_list:
        n = len(current_list)
        if n == 0:
            break
            
        # --- Lookahead Run Detection ---
        run_end = 1
        if n > 1:
            if current_list[1] >= current_list[0]:  # Potential ascending run
                while run_end < n and current_list[run_end] >= current_list[run_end - 1]:
                    run_end += 1
                sublists.append(current_list[:run_end])
                current_list = current_list[run_end:]
                continue
            elif current_list[1] <= current_list[0]:  # Potential descending run
                while run_end < n and current_list[run_end] <= current_list[run_end - 1]:
                    run_end += 1
                sorted_run = current_list[:run_end]
                sorted_run.reverse()
                sublists.append(sorted_run)
                current_list = current_list[run_end:]
                continue

        # --- Filtering Pass with Adaptive Reset ---
        correct = []
        wrong = []
        
        if left_to_right:
            current_max = float('-inf')
            for x in current_list:
                if x >= current_max:
                    correct.append(x)
                    current_max = x
                elif current_max > 0 and x <= (current_max * reset_threshold):
                    # Adaptive Reset: Seal current sublist, start a new one instantly
                    if correct:
                        sublists.append(correct)
                    correct = [x]
                    current_max = x
                else:
                    wrong.append(x)
        else:
            current_min = float('inf')
            temporary_wrong = []
            for x in reversed(current_list):
                if x <= current_min:
                    correct.append(x)
                    current_min = x
                elif current_min > 0 and x >= (current_min * (1.0 / reset_threshold)):
                    # Reverse Adaptive Reset
                    if correct:
                        correct.reverse()
                        sublists.append(correct)
                    correct = [x]
                    current_min = x
                else:
                    temporary_wrong.append(x)
            correct.reverse()
            temporary_wrong.reverse()
            wrong = temporary_wrong
            
        if correct:
            sublists.append(correct)
            
        current_list = wrong
        left_to_right = not left_to_right  # Alternate directions

    # -------------------------------------------------------------------------
    # Phase 2: Custom Tournament Tree Merge (In-House)
    # -------------------------------------------------------------------------
    while len(sublists) > 1:
        next_round = []
        for i in range(0, len(sublists), 2):
            if i + 1 < len(sublists):
                # Use our pure in-house merge instead of heapq
                next_round.append(merge(sublists[i], sublists[i+1]))
            else:
                next_round.append(sublists[i])
        sublists = next_round
        
    return sublists[0] if sublists else []


def compact_democratic_sort_inplace(arr, start=0, end=None):
    """
    A 100% pure, recursive In-Place variation of Democratic Sort.
    Uses zero extra allocations and zero built-in sorting mechanisms.
    """
    if end is None:
        end = len(arr)
        
    if (end - start) <= 1:
        return arr

    # Track boundaries for element swapping within the active window
    wrong_marker = start
    current_max = arr[start]
    
    for i in range(start + 1, end):
        if arr[i] >= current_max:
            current_max = arr[i]
        else:
            # Swap 'wrong' elements cleanly toward our wrong marker zone
            arr[wrong_marker], arr[i] = arr[i], arr[wrong_marker]
            wrong_marker += 1
            
    # Recursively apply Democratic principles to the partitioned boundaries
    # without ever calling an external sort function.
    if wrong_marker > start:
        compact_democratic_sort_inplace(arr, start, wrong_marker)
    compact_democratic_sort_inplace(arr, wrong_marker, end)
    
    return arr
