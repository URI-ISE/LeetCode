#include <atomic>
#include <utility>

template <typename T>
class SharedPtr {
private:
    struct ControlBlock {
        T* ptr;
        std::atomic<int> refCount;
        
        ControlBlock(T* p) : ptr(p), refCount(1) {}
    };
    
    ControlBlock* block;
    
public:
    // Constructor
    explicit SharedPtr(T* ptr = nullptr) {
        if (ptr) {
            block = new ControlBlock(ptr);
        } else {
            block = nullptr;
        }
    }
    
    // Copy Constructor
    SharedPtr(const SharedPtr& other) : block(other.block) {
        if (block) {
            block->refCount.fetch_add(1, std::memory_order_relaxed);
        }
    }
    
    // Move Constructor
    SharedPtr(SharedPtr&& other) noexcept : block(other.block) {
        other.block = nullptr;
    }
    
    // Destructor
    ~SharedPtr() {
        if (block) {
            int prevCount = block->refCount.fetch_sub(1, std::memory_order_acq_rel);
            if (prevCount == 1) {
                delete block->ptr;
                delete block;
            }
        }
    }
    
    // Copy Assignment
    SharedPtr& operator=(const SharedPtr& other) {
        if (this != &other) {
            SharedPtr temp(other);
            std::swap(block, temp.block);
        }
        return *this;
    }
    
    // Dereference Operators
    T& operator*() const { return *block->ptr; }
    T* operator->() const { return block->ptr; }
    T* get() const { return block ? block->ptr : nullptr; }
    
    // Reference Count
    int use_count() const {
        return block ? block->refCount.load(std::memory_order_acquire) : 0;
    }
};