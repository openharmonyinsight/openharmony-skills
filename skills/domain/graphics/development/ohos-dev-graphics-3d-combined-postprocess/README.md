# OpenHarmony Graphics3D Combined Post-Process Implementation

## Overview

This skill guides implementation of single-pass post-processing effects in OpenHarmony Graphics3D (LumeRender/Lume3D/LumeScene).

## Applicable Scenarios

- Implementing single-pass fullscreen shader post-processing effects (tone mapping, color grading, vignette, etc.)
- Adding effects to the Combined post-process system
- When users mention "Combined post-process" or "post-processing"

## Not Applicable Scenarios

- Effects requiring multiple render passes (bloom with blur passes, depth-of-field, motion blur, etc.)

## Module Dependencies

```
LumeRender → Lume3D → LumeScene
```

## Implementation Workflow

- LumeRender: 8 steps (configuration structure → shader constants → render pipeline integration)
- Lume3D: 5 steps (flag bits → component properties → render system integration)
- LumeScene: 9 steps (interface definition → API wrapper → build file updates)

## File Structure

```
ohos-dev-graphics3d-combined-postprocess/
├── SKILL.md              # Skill main file
├── README.md             # This documentation
└── references/
    └── implementation_guide.md  # Detailed implementation guide (with examples)
```

## Reference Documentation

- [implementation_guide.md](references/implementation_guide.md): Complete implementation examples for Tone and ColorConversion effects, data flow diagrams, file reference tables, and implementation checklists

## Maintenance Notes

This skill belongs to the OpenHarmony Graphics3D domain and should be referenced by developers working with the rendering engine.