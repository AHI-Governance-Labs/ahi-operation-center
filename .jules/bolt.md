## 2025-05-23 - Optimization of Log Compaction
**Learning:** Python built-in functions (`sum`, `min`, `max`) are fast, but multiple passes over large data + intermediate list creation can be slower than a single Python loop, especially when multiple aggregates are needed. In `ICEWLogger._compact_logs`, replacing 5+ list iterations and a large list allocation with a single loop yielded a ~1.6x speedup.
**Action:** When calculating multiple aggregates (sum, min, max, count conditions) from a large collection, prefer a single pass loop over multiple list comprehensions and built-in function calls.

## 2025-05-24 - Optimization of Variance Calculation
**Learning:** Calculating variance on a small sliding window (`deque`, N=100) using the standard definition (`sum((x-mean)**2)`) requires iterating twice or creating an intermediate list. Using the batch formula `Var(X) = E[X^2] - (E[X])^2` allows for a single-pass calculation without list allocation, yielding a ~3x speedup.
**Action:** For calculating mean and variance on small collections in hot paths, use the single-pass sum and sum-of-squares approach to avoid allocation and redundant iteration, ensuring to clamp variance to 0 for numerical stability.
