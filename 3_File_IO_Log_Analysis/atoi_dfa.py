import sys
from typing import List

"""
Day 3: String to Integer (atoi) via DFA
Constraints:
- Do NOT use int(); perform ASCII arithmetic
- Detect overflow before it happens; clamp to 32-bit signed range
- Implement as a deterministic finite automaton (Start -> Sign -> Digit -> End)
"""

INT_MIN = -(2**31)
INT_MAX = 2**31 - 1

class State:
    START = 0
    SIGN = 1
    DIGIT = 2
    END = 3


def atoi_dfa(s: str) -> int:
    state = State.START
    sign = 1
    acc = 0

    i = 0
    n = len(s)

    while i < n and state != State.END:
        c = s[i]
        if state == State.START:
            if c == ' ':
                i += 1
                continue
            elif c == '+' or c == '-':
                sign = -1 if c == '-' else 1
                state = State.SIGN
                i += 1
                continue
            elif '0' <= c <= '9':
                state = State.DIGIT
            else:
                state = State.END
                break
        if state == State.SIGN:
            if '0' <= c <= '9':
                state = State.DIGIT
            else:
                state = State.END
                break
        if state == State.DIGIT:
            if '0' <= c <= '9':
                d = ord(c) - ord('0')
                # Overflow check: acc*10 + d with sign
                if sign == 1:
                    if acc > (INT_MAX - d) // 10:
                        return INT_MAX
                else:
                    if -acc < (INT_MIN + d) // 10:  # rearranged to avoid int()
                        return INT_MIN
                acc = acc * 10 + d
                i += 1
                continue
            else:
                state = State.END
                break
        # Transition handled; proceed
        i += 0  # no-op to centralize control
    return sign * acc


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("Usage: python3 Day3_atoi_dfa.py \"   -42  \"")
        return 2
    s = argv[1]
    print(atoi_dfa(s))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
