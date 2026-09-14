# Resolving Circular Dependencies

Guidance for breaking circular dependencies between C/C++ modules.

## Understanding the Problem

A circular dependency occurs when:
- Module A includes headers from Module B
- Module B (directly or through chain) includes headers from Module A

This creates a cycle that complicates compilation, testing, and maintenance.

## Common Patterns

### Simple Two-Way Cycle

```
audio/ → includes → utils/
utils/ → includes → audio/
```

**Solution**: Extract shared code to a separate module:

```
audio/ → includes → common/
utils/ → includes → common/
```

### Three-Way Cycle

```
network/ → includes → crypto/
crypto/ → includes → storage/
storage/ → includes → network/
```

**Solutions**:
1. Introduce interfaces in a separate `interfaces/` module
2. Extract common dependencies to a shared `core/` module
3. Use dependency injection with forward declarations

## Resolution Strategies

### 1. Extract Common Code

Move code needed by both modules to a new shared module:

```cpp
// BEFORE: audio/player.h includes utils/logger.h
//        and utils/logger.h includes audio/types.h

// AFTER: Create common/types.h that both can include
// audio/player.h includes common/types.h
// utils/logger.h includes common/types.h
```

### 2. Use Forward Declarations

Replace includes with forward declarations where possible:

```cpp
// BEFORE
#include "AudioEngine.h"  // Creates dependency

class Player {
    AudioEngine* engine;
};

// AFTER
class AudioEngine;  // Forward declaration

class Player {
    AudioEngine* engine;
};
// Include in .cpp file
#include "AudioEngine.h"
```

### 3. Interface Segregation

Create pure interfaces in a separate module:

```cpp
// interfaces/i_audio.h
class IAudioEngine {
    virtual void play() = 0;
    virtual ~IAudioEngine() = default;
};

// audio/engine.h
class AudioEngine : public IAudioEngine { ... };

// utils/logger.cpp can include IAudioEngine without
// depending on the full AudioEngine implementation
```

### 4. Dependency Injection

Pass dependencies via constructors or setters:

```cpp
// BEFORE: Class constructs its own dependencies
class Player {
    Player() : engine(new AudioEngine()) {}
};

// AFTER: Dependencies injected
class Player {
    Player(IAudioEngine* e) : engine(e) {}
};
```

## Detecting the Source

When a cycle is reported, check:

1. **Which files create the dependency?** - The report shows specific include lines
2. **Is the include necessary?** - Some includes are remnants of refactoring
3. **Can it be a forward declaration?** - If only used as pointer/reference, yes
4. **Is the dependency conceptual?** - Maybe modules should be merged

## Validation After Fixing

After restructuring:
1. Re-run the circular dependency check
2. Verify compilation succeeds
3. Check for new warnings about undefined symbols
4. Ensure all tests still pass
