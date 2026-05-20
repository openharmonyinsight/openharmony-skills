# Profile Cangjie - Reference

## Overview

This skill profiles the Cangjie compiler using built-in cjc flags:
- `--profile-compile-time` — prints time consumption per compilation phase
- `--profile-compile-memory` — prints memory consumption per compilation phase

Generated `.prof` files contain the profiling data.

## cjc Profiling Flags

```bash
cjc --profile-compile-time source.cj -o output    # generates *.time.prof
cjc --profile-compile-memory source.cj -o output   # generates *.mem.prof
```

Both flags can be used together.

## Generated Files

- `<source>.time.prof` — time spent in each compilation phase
- `<source>.mem.prof` — memory usage per compilation phase

## Script Usage

```bash
# Profile with both time and memory
python3 skills/profile-cangjie/scripts/profile-cangjie.py test.cj --both

# Profile memory only
python3 skills/profile-cangjie/scripts/profile-cangjie.py test.cj --memory

# Analyze existing .prof file
python3 skills/profile-cangjie/scripts/profile-cangjie.py --analyze test.cj.mem.prof
```

## Prerequisites

- Compiler must be built already (`output/envsetup.sh` exists)
- No source code modifications needed
