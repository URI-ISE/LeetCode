#include <iostream>
#include <cstring>

class CustomString {
private:
    char* buffer;
    size_t length;

public:
    // Constructor
    CustomString(const char* str) {
        length = std::strlen(str);
        buffer = new char[length + 1];
        std::strcpy(buffer, str);
    }

    // Destructor
    ~CustomString() {
        delete[] buffer;
    }

    // Copy Constructor
    CustomString(const CustomString& other) {
        length = other.length;
        buffer = new char[length + 1];
        std::strcpy(buffer, other.buffer);
    }

    // Copy Assignment Operator
    CustomString& operator=(const CustomString& rhs) {
        if (this == &rhs) {
            return *this;
        }
        
        delete[] buffer;
        length = rhs.length;
        buffer = new char[length + 1];
        std::strcpy(buffer, rhs.buffer);
        
        return *this;
    }

    // Utility method to access the string
    const char* c_str() const {
        return buffer;
    }

    size_t getLength() const {
        return length;
    }
};

int main() {
    CustomString str1("Hello");
    CustomString str2 = str1;  // Copy Constructor
    CustomString str3("World");
    str3 = str1;               // Copy Assignment Operator

    std::cout << "str1: " << str1.c_str() << std::endl;
    std::cout << "str2: " << str2.c_str() << std::endl;
    std::cout << "str3: " << str3.c_str() << std::endl;

    return 0;
}