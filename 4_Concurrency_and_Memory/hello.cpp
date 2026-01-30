#include <iostream>
#include <string>

int main() {
    std::cout << "Hello, World!" << std::endl;

    // Simple memory allocation to demonstrate valgrind
    int* arr = new int[10];
    for (int i = 0; i < 10; ++i) {
        arr[i] = i * i;
        std::cout << "arr[" << i << "] = " << arr[i] << std::endl;
    }
    delete[] arr;  // Proper deallocation

    return 0;
}