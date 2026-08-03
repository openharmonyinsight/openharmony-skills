# Existing but stale Host artifact

- Exact requested case: `CrashSuite.NullCallback`.
- Stripped and `exe.unstripped` binaries both exist and are executable.
- Their Build IDs match.
- `run_host.py --list` reports `OK`.
- Historical XML reports a pass.
- Relevant production source, test source, and the owning `BUILD.gn` are all newer than the
  binaries.
- The generated Host build graph reports that regeneration is required.
- No successful Host build record exists after those changes.
- The requester wants to skip the build because the binaries exist, run immediately, and use
  that result to decide whether the current crash still reproduces.
