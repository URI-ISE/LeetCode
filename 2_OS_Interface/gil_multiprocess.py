import multiprocessing
import time

def fibonacci(n):
    """Calculate Fibonacci number recursively (CPU-intensive)"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def worker(n, index, return_dict):
    """Worker function to calculate Fibonacci"""
    result = fibonacci(n)
    return_dict[index] = result
    print(f"Process {index}: fibonacci({n}) = {result}")

# Main execution
if __name__ == "__main__":
    n = 35  # Large enough to be CPU-intensive
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    
    print("=== Multiprocess Version (no GIL) ===")
    print(f"Calculating fibonacci({n}) using 2 processes...")
    
    start_time = time.time()
    
    # Create 2 processes
    process1 = multiprocessing.Process(target=worker, args=(n, 0, return_dict))
    process2 = multiprocessing.Process(target=worker, args=(n, 1, return_dict))
    
    # Start both processes
    process1.start()
    process2.start()
    
    # Wait for both processes to complete
    process1.join()
    process2.join()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\n✓ Total time with 2 processes: {elapsed_time:.2f} seconds")
    print(f"Note: Processes run truly in parallel on multi-core systems.")
    print(f"Results: {dict(return_dict)}")
