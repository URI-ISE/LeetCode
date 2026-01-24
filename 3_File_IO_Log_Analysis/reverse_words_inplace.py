import sys
from typing import List

"""
Day 2: Reverse Words In-Place (LC 151)
Constraints:
- Do NOT use split(), reverse(), or re
- Convert string to char buffer (list) and operate in-place
- Algorithm: reverse entire buffer, then reverse each word, then compact spaces
- O(1) extra space beyond the buffer itself
"""


def reverse_range(buf: List[str], i: int, j: int) -> None:
    while i < j:
        buf[i], buf[j] = buf[j], buf[i]
        i += 1
        j -= 1


def compact_spaces(buf: List[str]) -> List[str]:
    # Remove leading/trailing and collapse multiple spaces to single
    n = len(buf)
    write = 0
    i = 0
    # Skip leading spaces
    while i < n and buf[i] == ' ':
        i += 1
    while i < n:
        if buf[i] != ' ':
            buf[write] = buf[i]
            write += 1
        else:
            # write a single space if previous char isn't a space
            if write > 0 and buf[write-1] != ' ':
                buf[write] = ' '
                write += 1
        i += 1
    # Remove trailing space
    if write > 0 and buf[write-1] == ' ':
        write -= 1
    return buf[:write]


def reverse_words_inplace(s: str) -> str:
    buf = list(s)
    if not buf:
        return ""
    # Pass 1: reverse entire buffer
    reverse_range(buf, 0, len(buf)-1)

    # Pass 2: reverse each word back
    i = 0
    n = len(buf)
    while i < n:
        if buf[i] == ' ':
            i += 1
            continue
        j = i
        while j < n and buf[j] != ' ':
            j += 1
        reverse_range(buf, i, j-1)
        i = j

    # Pass 3: compact spaces
    compacted = compact_spaces(buf)
    return ''.join(compacted)


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("Usage: python3 Day2_reverse_words_inplace.py \"  hello   world  \"")
        return 2
    s = argv[1]
    print(reverse_words_inplace(s))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
