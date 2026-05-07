# ohos-test-graphics3d-static-api-unit-test

## Skill Overview

This skill provides comprehensive guidance for generating unit tests for ETS/ArkTS static API classes in OpenHarmony graphic_3d module using GTest framework.

## Skill Metadata

| Field | Value |
|-------|-------|
| name | ohos-test-graphics3d-static-api-unit-test |
| display_name | Graphics 3D API Unit Test Generator |
| scope | domain |
| stage | testing |
| domain | graphics3d |
| capability | static-api-unit-test |
| version | 0.1.0 |
| status | trial |

## Target Domain

OpenHarmony graphic_3d module - ETS binding layer unit testing

## Key Features

- Complete test generation workflow
- Naming conventions for test classes, cases, and files
- GTest-based test fixture setup (EtsTest)
- BUILD.gn configuration guidance
- Common mistakes and solutions

## Use Cases

1. Adding unit tests for new ETS wrapper classes (CameraETS, MaterialETS, SceneETS)
2. Extending existing test coverage
3. Setting up new test modules
4. Ensuring OpenHarmony testing standards compliance

## Scope Classification

This skill is classified as **domain** skill because:
- Strong dependency on graphic_3d subsystem
- Only effective in graphics domain scenarios
- Requires domain-specific APIs (ETS wrapper classes)
- Requires domain-specific test framework (EtsTest fixture)

## Relation to Common Skills

This skill complements common testing skills but focuses on graphics domain specifics:
- Common skill: `ohos-test-ut-generation` (general UT generation)
- This skill: Graphics domain specialization with EtsTest fixture

## Domain Naming Note

This skill uses `graphics3d` as domain (instead of `graphics`) because:

- Strong dependency on **graphic_3d** subsystem (AGP 3D engine)
- Differentiates from potential future **graphics_2d** related skills
- Domain namespace directory remains `graphics/` per OpenHarmony skill specification
- Domain field can be specialized when justified (spec allows this with README explanation)

Reference: [OpenHarmony Skills Namespace & Placement Spec](../../../standard/openharmony-skills-namespace-and-placement-spec.md) - Section 6, Line 138

## Directory Structure

```
ohos-test-graphics3d-static-api-unit-test/
├── SKILL.md              # Main skill file for agent consumption
├── README.md             # This documentation
└── references/
    └── UNITTEST_GUIDE.md # Complete testing guide (581 lines)
```

## Future Enhancements

- [ ] Add test templates for different ETS wrapper patterns
- [ ] Include performance test examples
- [ ] Add coverage analysis guidance
- [ ] Create evals/ for test case evaluation

## Maintenance

- **Maintainer**: Graphics domain team
- **Last Updated**: 2025-01-29
- **Update Frequency**: As graphic_3d test framework evolves

## References

- [UNITTEST_GUIDE.md](references/UNITTEST_GUIDE.md) - Complete testing guide (engine lifecycle, BUILD.gn template, environment setup)
- Related skill: Future `ohos-test-ut-generation` (common)
- OpenHarmony testing standards