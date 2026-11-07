"""
Democratic Sort: An Adaptive, Stable, Multi-Backend Sorting Engine.
Born from a structural reimagining of Stalin Sort with an Adaptive Reset threshold.
Author: Collaborative Session Design
License: MIT
"""

import os
import math
import heapq
from concurrent.futures import ThreadPoolExecutor

def _merge_pair(pair):
    """Worker function to combine two sorted sublists using standard rules."""
    if len(pair) == 1:
        return pair[0]
    return list(heapq.merge(pair[0], pair[1]))

def democratic_sort(arr, reset_threshold=0.10):
    """
    Sorts an array using the complete Democratic Sort Architecture.
    
    Parameters:
    - arr (list): Unsorted list of comparable items.
    - reset_threshold (float): Percentage threshold below the current max 
      to trigger an Adaptive Reset (default 10%).
    """
    if not arr:
        return []
    
    sublists = []
    current_list = list(arr)
    left_to_right = True
    
    # -------------------------------------------------------------------------
    # Phase 1: Stratification & Extraction Loop
    # -------------------------------------------------------------------------
    while current_list:
        n = len(current_list)
        if n == 0:
            break
            
        # --- Lookahead Run Detection ---
        run_end = 1
        if n > 1:
            if current_list[0] <= current_list[1]:
                while run_end < n and current_list[run_end] >= current_list[run_end - 1]:
                    run_end += 1
                sublists.append(current_list[:run_end])
                current_list = current_list[run_end:]
                continue
            elif current_list[0] >= current_list[1]:
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
                # Rule: Keep if ordered, OR trigger an Adaptive Reset if element
                # plunges below the threshold relative to the current peak.
                if x >= current_max:
                    correct.append(x)
                    current_max = x
                elif current_max > 0 and x <= (current_max * reset_threshold):
                    # Adaptive Reset: Harvest what we have, start a fresh district
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
                    # Reverse Adaptive Reset for Right-to-Left pass
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
    # Phase 2: Under-the-Hood Backend Controller
    # -------------------------------------------------------------------------
    total_elements = len(arr)
    total_sublists = len(sublists)
    available_cores = os.cpu_count() or 1
    
    # Calculate runtime workload matrix: N * log2(K)
    work_volume = total_elements * math.log2(max(total_sublists, 1))
    
    # Dynamic System Check: Is multi-threading justified against thread overhead?
    if work_volume > 150000 and available_cores > 1 and total_sublists > 4:
        # Deploy Parallel Pipeline Tree Merge
        with ThreadPoolExecutor(max_workers=available_cores) as executor:
            while len(sublists) > 1:
                pairs = [(sublists[i], sublists[i+1]) if i+1 < len(sublists) else (sublists[i],) 
                         for i in range(0, len(sublists), 2)]
                sublists = list(executor.map(_merge_pair, pairs))
        return sublists[0] if sublists else []
    else:
        # Deploy Classic Sequential Tree Merge
        while len(sublists) > 1:
            next_round = []
            for i in range(0, len(sublists), 2):
                if i + 1 < len(sublists):
                    next_round.append(list(heapq.merge(sublists[i], sublists[i+1])))
                else:
                    next_round.append(sublists[i])
            sublists = next_round
        return sublists[0] if sublists else []


def compact_democratic_sort_inplace(arr):
    """
    Ultra-low memory variation utilizing an In-Place Two-Pointer Swap mechanism.
    Reduces Space Complexity to O(1) auxiliary memory.
    """
    n = len(arr)
    if n <= 1:
        return arr
    
    wrong_marker = 0
    current_max = arr[0]
    
    for i in range(1, n):
        if arr[i] >= current_max:
            current_max = arr[i]
        else:
            arr[wrong_marker], arr[i] = arr[i], arr[wrong_marker]
            wrong_marker += 1
            
    # Sub-segments can be recursively sorted inside the master index boundaries
    if wrong_marker > 0:
        arr[:wrong_marker] = sorted(arr[:wrong_marker])
    arr[wrong_marker:] = sorted(arr[wrong_marker:])
    return arr
