## 2025-05-23 - Optimization of Log Compaction
**Learning:** Python built-in functions (`sum`, `min`, `max`) are fast, but multiple passes over large data + intermediate list creation can be slower than a single Python loop, especially when multiple aggregates are needed. In `ICEWLogger._compact_logs`, replacing 5+ list iterations and a large list allocation with a single loop yielded a ~1.6x speedup.
**Action:** When calculating multiple aggregates (sum, min, max, count conditions) from a large collection, prefer a single pass loop over multiple list comprehensions and built-in function calls.

## 2025-05-24 - Optimization of Variance Calculation
**Learning:** Calculating variance on a small sliding window (`deque`, N=100) using the standard definition (`sum((x-mean)**2)`) requires iterating twice or creating an intermediate list. Using the batch formula `Var(X) = E[X^2] - (E[X])^2` allows for a single-pass calculation without list allocation, yielding a ~3x speedup.
**Action:** For calculating mean and variance on small collections in hot paths, use the single-pass sum and sum-of-squares approach to avoid allocation and redundant iteration, ensuring to clamp variance to 0 for numerical stability.

## 2025-05-24 - Optimization of Log Compaction (O(N) to O(1))
**Learning:** Iterating over a large list (N=100,000) to calculate aggregates creates a latency spike (jitter) even if the average throughput is high. By maintaining incremental statistics (sum, min, max, counts) on every insertion (O(1)), the compaction step becomes O(1), eliminating the spike.
**Action:** For large rolling logs where summaries are needed, favor incremental updates of statistics over batch processing at the end, provided the update overhead is negligible (using instance attributes instead of dictionary keys reduces overhead).

## 2025-05-24 - Optimization of MEBA Metric Calculation (O(N) to O(1))
**Learning:** Caching aggregates is insufficient for high-frequency interleaved read/write workloads (O(N) on cache miss). Incremental updates provide consistent O(1) performance regardless of usage pattern.
**Action:** Prefer incremental counters over lazy evaluation + caching for cumulative metrics.

## 2025-05-24 - Optimization of Sliding Window Variance (O(N) to O(1))
**Learning:** Replacing an O(N) loop (N=100) with O(1) incremental updates for variance calculation yielded a ~8.5% speedup in `ICEWLogger.process_event`. The gain was limited by the dominant overhead of UUID generation and object allocation in the logging step, proving that Amdahl's Law applies heavily here.
**Action:** When optimizing hot paths involving heavy I/O or logging, purely algorithmic optimizations (like O(N) -> O(1) math) may have diminishing returns unless the dominant overhead (logging) is also addressed.

## 2025-05-25 - Optimization of UUID Generation
**Learning:** `uuid.uuid4()` involves a syscall (`os.urandom`) and string formatting, which dominates latency in tight loops (~35µs/op total). For high-frequency event logging, generating a fresh UUID per event is unnecessary overhead.
**Action:** When generating unique IDs for high-volume local events, use a cached random prefix (generated once) combined with a simple incrementing counter. This maintains uniqueness and format while eliminating the syscall overhead, yielding a ~20% speedup.
