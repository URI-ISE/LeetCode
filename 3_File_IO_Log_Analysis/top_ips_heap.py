import os
import sys
import heapq
import tempfile
import shutil
from typing import Iterator, List, Tuple

"""
Parse a large Apache log file to find the top 10 IP addresses.
Constraints:
- Do NOT use readlines(); stream lines via a generator
- Use a dict to count frequencies
- Use heapq.nlargest to find the top 10
- Keep memory bounded by bucketizing IPs to temporary files
"""


def line_stream(path: str) -> Iterator[str]:
    """Yield lines from the file one by one without loading entire file."""
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            yield line


def extract_ip(line: str) -> str:
    """Extract the leading IP (first token) from an Apache log line."""
    # Common Log Format starts with the client IP
    # We avoid regex for speed; split once.
    if not line:
        return ""
    # Split on whitespace and take first token as IP
    ip = line.split(' ', 1)[0].strip()
    return ip


def bucket_index(ip: str, buckets: int = 1024) -> int:
    """Map an IP to a bucket index. Works for IPv4/IPv6 and malformed tokens."""
    if not ip:
        return 0
    return hash(ip) % buckets


def bucketize_ips(log_path: str, buckets: int = 1024) -> List[str]:
    """Stream log lines, write IPs to bucket files, return list of bucket paths."""
    temp_dir = tempfile.mkdtemp(prefix="log_buckets_")
    bucket_paths = [os.path.join(temp_dir, f"bucket_{i}.txt") for i in range(buckets)]
    # Pre-open all bucket files for append to minimize reopen cost
    files = [open(p, 'a', encoding='utf-8') for p in bucket_paths]
    try:
        for line in line_stream(log_path):
            ip = extract_ip(line)
            idx = bucket_index(ip, buckets)
            files[idx].write(ip + "\n")
    finally:
        for fh in files:
            fh.close()
    return bucket_paths


def top10_from_bucket(bucket_path: str) -> List[Tuple[str, int]]:
    """Count IPs in a single bucket using a dict, then return its top 10."""
    counts: dict[str, int] = {}
    with open(bucket_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            ip = line.rstrip('\n')
            if ip:
                counts[ip] = counts.get(ip, 0) + 1
    # Use heapq.nlargest to get top 10 in this bucket
    return heapq.nlargest(10, counts.items(), key=lambda kv: kv[1])


def compute_top10(log_path: str, buckets: int = 1024) -> List[Tuple[str, int]]:
    """
    Compute global top 10 by:
    1) Bucketizing IPs to temporary files (streaming input)
    2) Computing per-bucket top 10 with a dict and heapq.nlargest
    3) Merging all candidates to final global top 10 via heapq.nlargest
    This approach keeps memory bounded since we never hold all counts at once.
    """
    bucket_paths = bucketize_ips(log_path, buckets=buckets)
    candidates: List[Tuple[str, int]] = []
    try:
        for bp in bucket_paths:
            top10_bucket = top10_from_bucket(bp)
            candidates.extend(top10_bucket)
        # Final global top 10 from union of bucket top 10s
        return heapq.nlargest(10, candidates, key=lambda kv: kv[1])
    finally:
        # Clean up bucket files and directory
        if bucket_paths:
            shutil.rmtree(os.path.dirname(bucket_paths[0]), ignore_errors=True)


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("Usage: python3 top_ips_heap.py /path/to/access.log")
        return 2
    log_path = argv[1]
    if not os.path.isfile(log_path):
        print(f"Error: File not found: {log_path}")
        return 2

    print("Streaming and bucketizing log... (this may take time for large files)")
    top10 = compute_top10(log_path, buckets=1024)
    print("\nTop 10 IP addresses:")
    for rank, (ip, count) in enumerate(top10, start=1):
        print(f"{rank:2d}. {ip} -> {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
