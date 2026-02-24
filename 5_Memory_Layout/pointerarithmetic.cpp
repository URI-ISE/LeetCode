/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    // Iterative approach: O(1) space, safe for large lists
    ListNode* reverseListIterative(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* curr = head;
        
        while (curr) {
            ListNode* nextTemp = curr->next;  // Save next node
            curr->next = prev;                // Reverse the link
            prev = curr;                      // Move prev forward
            curr = nextTemp;                  // Move curr forward
        }
        
        return prev;
    }
    
    // Recursive approach: O(N) stack space, risk of stack overflow for large lists
    ListNode* reverseListRecursive(ListNode* head) {
        // Base case: empty list or single node
        if (!head || !head->next) {
            return head;
        }
        
        // Recursively reverse the rest of the list
        ListNode* newHead = reverseListRecursive(head->next);
        
        // Reverse the link: make head->next point back to head
        head->next->next = head;
        head->next = nullptr;
        
        return newHead;
    }
    
    // Main solution - use iterative approach for safety
    ListNode* reverseList(ListNode* head) {
        return reverseListIterative(head);
    }
};