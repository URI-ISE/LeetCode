#include <iostream>
#include <memory>

class Node {
public:
    int id;
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> weak_next;

    Node(int id) : id(id) {
        std::cout << "Node " << id << " constructed" << std::endl;
    }

    ~Node() {
        std::cout << "Node " << id << " destructed" << std::endl;
    }
};

void demonstrate_cycle_with_shared_ptr() {
    std::cout << "\n=== CYCLE WITH shared_ptr (LEAK) ===" << std::endl;
    
    auto node1 = std::make_shared<Node>(1);
    auto node2 = std::make_shared<Node>(2);
    
    std::cout << "node1 use_count: " << node1.use_count() << std::endl;
    std::cout << "node2 use_count: " << node2.use_count() << std::endl;
    
    // Create cycle: 1 -> 2 -> 1
    node1->next = node2;
    node2->next = node1;
    
    std::cout << "After creating cycle:" << std::endl;
    std::cout << "node1 use_count: " << node1.use_count() << std::endl;
    std::cout << "node2 use_count: " << node2.use_count() << std::endl;
    
    std::cout << "Exiting scope..." << std::endl;
    // node1 and node2 go out of scope, but destructors won't be called!
    // node1 is referenced by node2->next (refcount = 1)
    // node2 is referenced by node1->next (refcount = 1)
    // MEMORY LEAK!
}

void demonstrate_cycle_with_weak_ptr() {
    std::cout << "\n=== CYCLE WITH weak_ptr (NO LEAK) ===" << std::endl;
    
    auto node1 = std::make_shared<Node>(1);
    auto node2 = std::make_shared<Node>(2);
    
    std::cout << "node1 use_count: " << node1.use_count() << std::endl;
    std::cout << "node2 use_count: " << node2.use_count() << std::endl;
    
    // Create cycle with weak_ptr: breaks the circular dependency
    node1->next = node2;
    node2->weak_next = node1;  // Use weak_ptr for back-edge
    
    std::cout << "After creating cycle (with weak_ptr):" << std::endl;
    std::cout << "node1 use_count: " << node1.use_count() << std::endl;
    std::cout << "node2 use_count: " << node2.use_count() << std::endl;
    
    std::cout << "Exiting scope..." << std::endl;
    // Both nodes properly destroyed because weak_ptr doesn't hold ownership
}

int main() {
    demonstrate_cycle_with_shared_ptr();
    std::cout << "\n[LEAK: Destructors above were NOT called]\n" << std::endl;
    
    demonstrate_cycle_with_weak_ptr();
    std::cout << "\n[SUCCESS: Both destructors called above]\n" << std::endl;
    
    return 0;
}