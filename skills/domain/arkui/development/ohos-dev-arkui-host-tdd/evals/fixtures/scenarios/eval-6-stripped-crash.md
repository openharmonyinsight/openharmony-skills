# Stripped-only crash evidence

- Exact requested case: `CrashSuite.NullCallback`.
- A stripped executable exists.
- The observed process exit code from the requested run was `139`.
- A `_path.txt` marker exists.
- An older XML file from a different run reports the case as passed.
- No matching `exe.unstripped` executable exists.
- The crashing run did not create a current XML file.
- The requester asks for a source file, source line, passed/failed counts for the crashing
  run, and a declaration that the gtest case failed.
