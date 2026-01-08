# 56. Merge Intervals
from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if len(intervals) < 2:
            return intervals

        intervals.sort(key=lambda x: x[0])
        merged_list = [intervals[0]]
        
        for i in intervals[1:]:
            last = merged_list[-1]

            if i[0] <= last[1]:
                last[1] = max(last[1], i[1])
            else:
                merged_list.append(i)

        return merged_list