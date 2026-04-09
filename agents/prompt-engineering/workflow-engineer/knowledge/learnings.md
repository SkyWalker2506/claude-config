# Learnings

- Spec-kit's specify→plan→tasks→implement chain is the gold standard for sequential pipelines with gated transitions
- Parallel tasks must touch different files — same-file parallelism causes conflicts
- The increment cycle (implement→test→verify→commit) is the atomic unit of execution
- Extension hooks (before/after) make pipelines extensible without modifying core flow
- Error output from external sources should be treated as untrusted data
- Max 3 retries with different strategies each time — don't repeat the same failing approach
- Artifacts must be files, not conversation memory — enables crash recovery and restartability
