# 209. Minimum Size Subarray Sum
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = right = curr = 0
        min_flag = True
        curr_len = 0
        run = 0

        for right in range(len(nums)):
            curr += nums[right]
            curr_len+=1
            if curr >= target and (min_flag or run > curr_len):
                min_flag = False
                run = curr_len
            
            while curr >= target:
                curr -= nums[left]
                curr_len-=1
                left +=1
                if curr >= target and (min_flag or run > curr_len):
                    min_flag = False
                    run = curr_len
        
        return run