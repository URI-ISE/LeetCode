import os
import sys
import time
from typing import List

"""
Day 4: Chunked File Copier using raw syscalls
Constraints:
- Do NOT use shutil, file.read(), or open()
- Use os.open, os.read, os.write
- Benchmark buffer sizes: 1B, 1KB, 4KB, 1MB
"""

O_RDONLY = os.O_RDONLY
O_WRONLY = os.O_WRONLY
O_CREAT = os.O_CREAT
O_TRUNC = os.O_TRUNC
MODE_644 = 0o644


def make_dummy_file(path: str, size_bytes: int) -> None:
    fd = os.open(path, O_WRONLY | O_CREAT | O_TRUNC, MODE_644)
    try:
        chunk = b"0" * (1024 * 1024)  # 1MB block of zeros
        written = 0
        while written < size_bytes:
            to_write = min(len(chunk), size_bytes - written)
            os.write(fd, chunk[:to_write])
            written += to_write
    finally:
        os.close(fd)


def copy_file(src: str, dst: str, buf_size: int) -> None:
    src_fd = os.open(src, O_RDONLY)
    dst_fd = os.open(dst, O_WRONLY | O_CREAT | O_TRUNC, MODE_644)
    try:
        while True:
            data = os.read(src_fd, buf_size)
            if not data:
                break
            os.write(dst_fd, data)
    finally:
        os.close(src_fd)
        os.close(dst_fd)


def benchmark(src: str, sizes: List[int]) -> None:
    for sz in sizes:
        dst = f"{src}.copy_{sz}"
        start = time.time()
        copy_file(src, dst, sz)
        elapsed = time.time() - start
        print(f"Buffer {sz} bytes: {elapsed:.3f}s")
        # Cleanup copied file to keep workspace tidy
        try:
            os.remove(dst)
        except OSError:
            pass


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("Usage: python3 Day4_chunked_copier.py /tmp/dummy.bin")
        print("If the file doesn't exist, it will be created (50MB).")
        return 2
    src = argv[1]
    if not os.path.isfile(src):
        print("Creating 50MB dummy file...")
        make_dummy_file(src, 50 * 1024 * 1024)
    print("Benchmarking chunked copy with raw syscalls...")
    sizes = [1, 1024, 4096, 1024 * 1024]
    benchmark(src, sizes)
    print("\nExplanation: 1-byte buffers cause excessive syscalls and context switches,\nwhich thrash I/O and dramatically increase overhead. 4KB (page size) amortizes\ntransition costs much better, and 1MB reduces call overhead further while staying\ncache-friendly for many systems.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
