#include <iostream>
#include <list>
#include <unordered_map>
#include <utility>

template <typename Key, typename Value>
class LRUCache {
private:
    int capacity;
    // List stores (key, value) pairs; most recent at back, least recent at front
    std::list<std::pair<Key, Value>> cache;
    // Map: key -> iterator to list node
    std::unordered_map<Key, typename std::list<std::pair<Key, Value>>::iterator> keyToIter;

    void moveToBack(const Key& key) {
        auto iter = keyToIter[key];
        cache.erase(iter);
        cache.push_back({key, iter->second});
        keyToIter[key] = std::prev(cache.end());
    }

public:
    LRUCache(int cap) : capacity(cap) {}

    Value get(const Key& key) {
        if (keyToIter.find(key) == keyToIter.end()) {
            throw std::out_of_range("Key not found");
        }
        moveToBack(key);
        return keyToIter[key]->second;
    }

    void put(const Key& key, const Value& value) {
        if (keyToIter.find(key) != keyToIter.end()) {
            // Key exists: update and move to back
            auto iter = keyToIter[key];
            iter->second = value;
            moveToBack(key);
        } else {
            // New key
            if (static_cast<int>(cache.size()) >= capacity) {
                // Evict least recently used (front node)
                Key lruKey = cache.front().first;
                cache.pop_front();
                keyToIter.erase(lruKey);
            }
            cache.push_back({key, value});
            keyToIter[key] = std::prev(cache.end());
        }
    }
};

int main() {
    LRUCache<int, std::string> lru(3);

    lru.put(1, "one");
    lru.put(2, "two");
    lru.put(3, "three");

    std::cout << lru.get(1) << std::endl;  // "one", moves to back
    lru.put(4, "four");                    // Evicts key 2 (least recently used)

    try {
        std::cout << lru.get(2) << std::endl;
    } catch (const std::out_of_range& e) {
        std::cout << "Key 2 evicted: " << e.what() << std::endl;
    }

    return 0;
}