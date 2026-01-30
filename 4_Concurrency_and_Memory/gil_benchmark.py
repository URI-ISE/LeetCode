import time
import threading
import multiprocessing

def compute_heavy() -> int:
    """Calculate the sum of squares from 1 to 10,000,000."""
    return sum(i**2 for i in range(1, 10000001))

def worker(results, index):
    """Worker function for multiprocessing."""
    results[index] = compute_heavy()

def run_sequential():
    """Case A: Run compute_heavy twice sequentially."""
    print("=== Case A: Sequential ===")
    start = time.time()
    result1 = compute_heavy()
    result2 = compute_heavy()
    end = time.time()
    elapsed = end - start
    print(f"Results: {result1}, {result2}")
    print(f"Time: {elapsed:.2f}s")
    return elapsed

def run_threaded():
    """Case B: Run compute_heavy twice using threads."""
    print("\n=== Case B: Threaded ===")
    results = [None, None]

    def worker(index):
        results[index] = compute_heavy()

    start = time.time()
    t1 = threading.Thread(target=worker, args=(0,))
    t2 = threading.Thread(target=worker, args=(1,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    end = time.time()
    elapsed = end - start
    print(f"Results: {results[0]}, {results[1]}")
    print(f"Time: {elapsed:.2f}s")
    return elapsed

def run_multiprocess():
    """Case C: Run compute_heavy twice using processes."""
    print("\n=== Case C: Multiprocess ===")
    manager = multiprocessing.Manager()
    results = manager.list([None, None])

    start = time.time()
    p1 = multiprocessing.Process(target=worker, args=(results, 0))
    p2 = multiprocessing.Process(target=worker, args=(results, 1))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end = time.time()
    elapsed = end - start
    print(f"Results: {results[0]}, {results[1]}")
    print(f"Time: {elapsed:.2f}s")
    return elapsed

def main():
    seq_time = run_sequential()
    thread_time = run_threaded()
    proc_time = run_multiprocess()

if __name__ == "__main__":
    main()