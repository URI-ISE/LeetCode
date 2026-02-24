/**
 * Definition for singly-linked list node.
 */
struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};

/**
 * Floyd's Cycle-Finding Algorithm (Tortoise and Hare)
 * 
 * Time Complexity: O(n)
 * Space Complexity: O(1)
 * 
 * @param head - const pointer to the head of the linked list
 * @return const pointer to the node where cycle begins, or nullptr if no cycle
 */
const ListNode* detectCycle(const ListNode *head) {
    if (!head || !head->next) {
        return nullptr;
    }
    
    // Phase 1: Detect if cycle exists using slow and fast pointers
    const ListNode *slow = head;
    const ListNode *fast = head;
    
    while (fast && fast->next) {
        slow = slow->next;           // Move 1 step
        fast = fast->next->next;     // Move 2 steps
        
        if (slow == fast) {
            // Cycle detected, proceed to Phase 2
            break;
        }
    }
    
    // If no cycle found
    if (!fast || !fast->next) {
        return nullptr;
    }
    
    // Phase 2: Find the start of the cycle
    // Move slow to head, keep fast at meeting point
    // Move both 1 step at a time until they meet
    slow = head;
    while (slow != fast) {
        slow = slow->next;
        fast = fast->next;
    }
    
    return slow;  // Return the node where cycle begins
}