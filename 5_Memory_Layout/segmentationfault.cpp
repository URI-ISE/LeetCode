#include <iostream>
#include <cstring>

using namespace std;

// Function 1: Cause Segfault by writing to null pointer
void causeNullPointerSegfault() {
    cout << "--- Test 1: Null Pointer Segfault ---" << endl;
    int* nullPtr = nullptr;
    *nullPtr = 42;  // LINE 11: SEGFAULT HERE - writing to null pointer
    cout << "This won't print" << endl;
}

// Function 2: Cause Heap Corruption via double-free
void causeDoubleFree() {
    cout << "--- Test 2: Double Free ---" << endl;
    int* arr = new int[10];
    arr[0] = 100;
    cout << "Allocated array, arr[0] = " << arr[0] << endl;
    
    delete[] arr;  // First free
    cout << "First delete[] called" << endl;
    
    delete[] arr;  // LINE 24: HEAP CORRUPTION HERE - double free
    cout << "This may crash or corrupts heap metadata" << endl;
}

// Function 3: Return pointer to local stack variable
int* returnLocalStackPointer() {
    int localVar = 999;
    return &localVar;  // LINE 30: Returning address of local variable
}

// Dummy function to overwrite the stack
void dummyFunction() {
    int dummy1 = 0xDEADBEEF;
    int dummy2 = 0xCAFEBABE;
    int dummy3 = 0x12345678;
    // This overwrites the stack where localVar was stored
}

void causeStackUse() {
    cout << "--- Test 3: Use After Free (Stack) ---" << endl;
    int* stackPtr = returnLocalStackPointer();
    cout << "Pointer obtained: " << (void*)stackPtr << endl;
    cout << "Value (may be stale): " << *stackPtr << " (garbage data)" << endl;
    
    dummyFunction();  // Overwrites stack
    
    cout << "After dummy function call: " << *stackPtr << " (different garbage!)" << endl;
}

int main() {
    cout << "=== Memory Debugging Drill ===" << endl << endl;
    
    // Uncomment one test at a time to run under gdb/valgrind
    
    // causeNullPointerSegfault();  // Run with: gdb ./a.out
    
    causeDoubleFree();  // Run with: valgrind ./a.out
    
    // causeStackUse();  // Run with: gdb ./a.out
    
    cout << "\nProgram ended" << endl;
    return 0;
}