# 347. Top K Frequent Elements

from typing import List
import heapq
from collections import Counter

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        if k == len(nums):
            return nums
        
        count = Counter(nums)
        
        return heapq.nlargest(k, count.keys(), key=count.get)