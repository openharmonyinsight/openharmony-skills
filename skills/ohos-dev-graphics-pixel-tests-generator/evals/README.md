# OpenHarmony Graphics Pixel Tests Generator Skill Evals

Use [`evals.json`](evals.json) as the seed set for the first benchmark iteration.

## Default flow

1. Snapshot the current skill if you need an `old_skill` baseline.
2. Create a sibling workspace `ohos-dev-graphics-pixel-tests-generator-workspace/iteration-1/`.
3. For each eval, create a descriptive directory such as `eval-0-property-display-test/`.
4. Save per-run outputs under `with_skill/outputs/` and `old_skill/outputs/` or `without_skill/outputs/`.
5. Add `eval_metadata.json`, `timing.json`, and `grading.json` for each run.
6. Aggregate the iteration with the `skill-creator` benchmark script and generate the review viewer.

## Minimum success criteria

- At least one eval checks canonical CONTENT_DISPLAY_TEST generation (fixture, node lifecycle with `RegisterNode`, deterministic pixels, `BUILD.gn` source array).
- At least one eval checks `RegisterNode` lifecycle correctness (every `AddChild` / `AddChildToSubWindow` node is registered; parent/child trees register both).
- At least one eval checks the blank-screenshot diagnosis (missing `RegisterNode` causes node early release → empty capture) and its fix.
- At least one eval checks macro selection: `GRAPHIC_TEST` for independent screenshots vs `GRAPHIC_TESTS` for grid aggregation in one PNG.
- At least one eval checks parameter-matrix grid layout (compute `sizeX`/`sizeY`/`x`/`y` from `screenWidth`/`screenHeight`, cover boundary values -1/0/0.5/1/2).
- At least one eval checks manual capture (`GRAPHIC_N_TEST` + `FlushImplicitTransaction` + `usleep` + `TestCaseCapture` using `DisplayManager::GetScreenshot`).
- At least one eval checks sub-window tests (`CreateSubWindow` + `AddChildToSubWindow` + `RegisterNode`, framework auto-switches to display capture).
- At least one eval checks `BUILD.gn` update rules (insert into correct `*_sources` array, no new `ohos_unittest` target, preserve local formatting).
- At least one eval checks flush discipline: a plain auto test must NOT add `FlushImplicitTransaction` / sleep, and only adds it for manual capture / immediate query / neighbor convention.
- At least one eval checks `Drawing::Canvas` local style (`BeginRecording`/`FinishRecording`, `Brush`/`Pen` + `AttachBrush`/`DetachBrush`) and rejects invented helpers (`paintSetColor`).
- At least one eval checks animation tests (`ANIMATION_TEST`, `RSNode::Animate` + `RSAnimationTimingProtocol`/`Curve`, `RSUIContext`).
- At least one eval checks effect feature tests (`EFFECT_TEST`, `SetUpNodeBgImage`, border/blur/effect API, `rs_graphic_test_img.h`).
- At least one eval checks open-capability / PixelMap tests (reuse existing `/data/local/tmp` path or generate PixelMap in code; never use an unverified resource path).
- At least one eval checks surface/PixelMap query tests (flush + wait before `CreatePixelMapFromSurfaceId`, register surviving surface/node).
- At least one eval checks the test taxonomy mapping (directory ↔ `RSGraphicTestType`: `CONTENT_DISPLAY_TEST`, `ANIMATION_TEST`, `EFFECT_TEST`, `GPU_COMPOSER_TEST`, `HYBRID_RENDER_TEST`).
- At least one eval checks fixture/casing conventions (`namespace OHOS::Rosen`, Apache copyright header, `@tc.name/@tc.desc/@tc.type` comments when neighbors have them).
- Negative cases are present in nearly every eval: the generated test must NOT misuse `GRAPHIC_TESTS`, invent Drawing helpers / RenderService APIs, create `ohos_unittest` targets, add unnecessary flush/sleep, or skip `RegisterNode`.
- Assertions measure pixel-test-specific deltas (correct macro, correct source array, `RegisterNode` presence, deterministic layout, real API usage) rather than generic code-review quality.

## Current coverage map

- `0`: canonical CONTENT_DISPLAY_TEST (RSCanvasNode background color), full pipeline — fixture, node lifecycle with `RegisterNode`, deterministic pixels, `BUILD.gn` update, no new `ohos_unittest`, Apache header + namespace.
- `1`: animation test (`ANIMATION_TEST`) in `rs_display_effect/animation`, modifier + `RSNode::Animate` + timing protocol/curve, `RSUIContext`, registered nodes.
- `2`: effect feature test (`EFFECT_TEST`) in `rs_effect_feature`, `SetUpNodeBgImage` with reused `/data/local/tmp` path, border/blur/effect API, `rs_graphic_test_img.h`.
- `3`: parameter-matrix grid in a single `GRAPHIC_TEST` covering `SetAlpha` boundary values (-1/0/0.5/1/2), grid layout math, registered nodes; must NOT split into independent tests when grid is requested.
- `4`: `GRAPHIC_TESTS` grid aggregation (multiple test functions → one PNG, shared `SetScreenSize`, filename omits single test name) and the negative case — independent screenshots must use `GRAPHIC_TEST` instead.
- `5`: manual capture (`GRAPHIC_N_TEST`) — `FlushImplicitTransaction` + `usleep(SLEEP_TIME_FOR_PROXY)` + `TestCaseCapture` using `DisplayManager::GetScreenshot` + `WriteToPngWithPixelMap`, correct includes/constants.
- `6`: sub-window test — `CreateSubWindow` + `AddChildToSubWindow` + `RegisterNode`, framework auto-switches to display capture (no manual `SetCaptureScope` needed).
- `7`: `BUILD.gn` update focus — insert relative path into the correct `*_sources` array, no new `ohos_unittest` target, preserve local indentation/formatting.
- `8`: blank-screenshot diagnosis — identify missing `RegisterNode` as the cause and fix it; parent/child node trees register both levels (negative case: correct code already registers).
- `9`: `Drawing::Canvas` local style — `BeginRecording`/`FinishRecording`, `Brush`/`Pen` + `AttachBrush`/`DetachBrush`; reject invented `paintSetColor` helper and generalized Drawing signatures.
- `10`: open-capability PixelMap test — reuse existing `/data/local/tmp` path or generate PixelMap data in code; must NOT use an unverified resource path.
- `11`: surface/PixelMap query test — `GRAPHIC_N_TEST`, flush + wait before `CreatePixelMapFromSurfaceId`, register surviving surface/node.
- `12`: flush discipline — plain auto test must NOT add `FlushImplicitTransaction`/sleep (TearDown flushes); only manual capture / immediate query / neighbor convention justify it; do not include `transaction/rs_interfaces.h` when no flush is needed.
- `13`: taxonomy mapping — choose directory + `RSGraphicTestType` for five distinct scenarios (`CONTENT_DISPLAY_TEST`, `ANIMATION_TEST`, `EFFECT_TEST`, `GPU_COMPOSER_TEST`, `HYBRID_RENDER_TEST`).

## Dimension coverage summary

| Skill dimension | Eval IDs | Coverage |
|-----------------|----------|----------|
| Test categorization (directory ↔ type) | 0, 1, 2, 7, 10, 13 | covered |
| Macro selection (GRAPHIC_TEST / TESTS / N_TEST / D_TEST) | 0, 3, 4, 5, 11, 12 | covered |
| RegisterNode lifecycle | 0, 3, 6, 8, 11 | covered |
| Fixture structure (RSGraphicTest, BeforeEach, SetScreenSize) | 0, 1, 2, 3, 4 | covered |
| Deterministic pixel output (grid, boundary values) | 0, 3, 4 | covered |
| BUILD.gn update rules | 0, 7 | covered |
| Flush discipline | 5, 11, 12 | covered |
| Resource path safety | 2, 10 | covered |
| Drawing::Canvas style | 9 | covered |
| Sub-window tests | 6 | covered |
| Manual capture | 5 | covered |
| Animation tests | 1 | covered |
| Effect feature tests | 2 | covered |
| Open capability / PixelMap | 10 | covered |
| Surface/PixelMap query | 11 | covered |
| Negative cases (must-NOT) | all | covered |

See [`../SKILL.md`](../SKILL.md) for the full generation rules and [`../references/test-taxonomy-build.md`](../references/test-taxonomy-build.md) for the directory/type mapping and source-array rules.
