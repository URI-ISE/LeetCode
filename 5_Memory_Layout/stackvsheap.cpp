#include <iostream>
#include <chrono>

int main() {
    const int iterations = 100'000'000;
    
    // Stack allocation test
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < iterations; ++i) {
        int x = 42;  // Stack allocation
        (void)x;     // Use variable to prevent optimization
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto stack_duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "Stack allocation time: " << stack_duration.count() << " ms\n";
    
    // Heap allocation test
    start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < iterations; ++i) {
        int* x = new int(42);  // Heap allocation
        delete x;              // Immediate deallocation
    }
    end = std::chrono::high_resolution_clock::now();
    auto heap_duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "Heap allocation time: " << heap_duration.count() << " ms\n";
    std::cout << "Heap is " << (double)heap_duration.count() / stack_duration.count() 
              << "x slower\n";
    
    return 0;
}