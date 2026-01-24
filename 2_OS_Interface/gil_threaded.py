import threading
import time

def fibonacci(n):
    """Calculate Fibonacci number recursively (CPU-intensive)"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def worker(n, results, index):
    """Worker function to calculate Fibonacci"""
    result = fibonacci(n)
    results[index] = result
    print(f"Thread {index}: fibonacci({n}) = {result}")

# Main execution
if __name__ == "__main__":
    n = 35  # Large enough to be CPU-intensive
    results = [None, None]
    
    print("=== Threaded Version (with GIL) ===")
    print(f"Calculating fibonacci({n}) using 2 threads...")
    
    start_time = time.time()
    
    # Create 2 threads
    thread1 = threading.Thread(target=worker, args=(n, results, 0))
    thread2 = threading.Thread(target=worker, args=(n, results, 1))
    
    # Start both threads
    thread1.start()
    thread2.start()
    
    # Wait for both threads to complete
    thread1.join()
    thread2.join()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\n✓ Total time with 2 threads: {elapsed_time:.2f} seconds")
    print(f"Note: Due to the GIL, threads run mostly sequentially for CPU-bound tasks.")
