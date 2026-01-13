# 398. Random Pick Index

class Solution:

    def __init__(self, nums: List[int]):
        self.reservoir = nums


    def pick(self, target: int) -> int:
        n = len(self.reservoir)
        count = 0
        idx = 0
        i = 0
        while i < n:
            if (self.reservoir[i] == target):
                count +=1
                if (random.randrange(count) == 0):
                    idx = i

            i+=1
        return idx

# Your Solution object will be instantiated and called as such:
# obj = Solution(nums)
# param_1 = obj.pick(target)