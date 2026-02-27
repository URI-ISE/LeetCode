#include <iostream>
#include <memory>

// Function that accepts ownership of the buffer
std::unique_ptr<int[]> processBuffer(std::unique_ptr<int[]> buffer) {
    // Process the buffer
    for (int i = 0; i < 1024; ++i) {
        buffer[i] = i * 2;
    }
    return buffer;
}

int main() {
    // Allocate a large buffer using unique_ptr
    std::unique_ptr<int[]> myBuffer = std::make_unique<int[]>(1024);
    
    std::cout << "Before move:" << std::endl;
    std::cout << "  myBuffer pointer: " << myBuffer.get() << std::endl;
    std::cout << "  myBuffer[0]: " << myBuffer[0] << std::endl;
    
    // Pass the buffer to the function using std::move
    myBuffer = processBuffer(std::move(myBuffer));
    
    std::cout << "\nAfter move:" << std::endl;
    std::cout << "  myBuffer pointer: " << myBuffer.get() << std::endl;
    std::cout << "  myBuffer[5]: " << myBuffer[5] << std::endl;
    std::cout << "  myBuffer[10]: " << myBuffer[10] << std::endl;
    
    return 0;
}