# LeetCode Roadmap

## Overview
This repository documents a rigorous 18-week transition roadmap from scripting to high-performance systems architecture. It treats algorithmic challenges not as isolated puzzles, but as filters for understanding low-level system execution, memory locality, and thread safety across multiple environments (Python, C++, Java, Node.js).

## Core Objectives
1.  **The "Metal" First:** Mapping high-level code to hardware execution (e.g., analyzing stack vs. heap allocation).
2.  **System Translation:** Connecting algorithmic patterns to real-world components (e.g., Sliding Window $\to$ TCP Flow Control).
3.  **Resource Efficiency:** Prioritizing space/time complexity ($O(N)$) and memory hygiene over syntactic sugar.

## Roadmap Structure

| Phase | Focus | Language | Key Technical Themes |
| :--- | :--- | :--- | :--- |
| **I** | **Algorithmic Patterns** | Python | Sliding Window, Two Pointers, Cycle Detection, Interval Merging. |
| **II** | **Systems Automator** | Python | OS Interface (`sys`/`os`), Stream Processing, Log Analysis, GIL limitations. |
| **III** | **The Metal** | C++ | Manual Memory Management, Pointers/References, RAII, Low-level Concurrency. |
| **IV** | **Enterprise Scalability** | Java | JVM Internals, Garbage Collection, Thread Pools, Java Memory Model. |
| **V** | **Async Model** | Node.js | Event Loop, Non-blocking I/O, `libuv`, Streams & Buffers. |
| **VI** | **Data Persistence** | SQL | Storage Engines (InnoDB), Indexing (B-Trees), Transaction Isolation. |
| **VII** | **System Design** | Mixed | Designing Rate Limiters, KV Stores, and URL Shorteners. |
