# Benchmark Report: C SKILL (Iteration 3)

**Generated:** 2026-06-17T03:54:26.479263+00:00
**Total Evals:** 60
**Configuration:** with_skill vs without_skill

---

## Summary

> 注：Iteration 3 跑分后，已根据评审反馈对 evals.json 的 `rule_name` 断言做对齐（3 处 C，仅修正字符串使其与 SKILL.md 标题一致，规则语义未变），不重新跑分。

| Metric | with_skill | without_skill | Delta |
|--------|-----------|---------------|-------|
| Mean Pass Rate | 100.0% | 50.0% | +0.50 |
| Std Dev | 0.000 | 0.500 | |
| Min Pass Rate | 100.0% | 0.0% | |
| Max Pass Rate | 100.0% | 100.0% | |
| Total Findings | 204 | 90 | +114 |
| Evals Run | 60 | 60 | |

---

## Per-Eval Results

| Eval | Type | with_skill Pass Rate | with_skill Findings | without_skill Pass Rate | without_skill Findings | Winner |
|------|------|---------------------|---------------------|------------------------|------------------------|--------|
| c-api-coord-bad | negative | 100% | 5 | 100% | 2 | tie |
| c-api-coord-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-binary-encoding-bad | negative | 100% | 6 | 100% | 2 | tie |
| c-binary-encoding-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-c-buffer-bad | negative | 100% | 7 | 100% | 2 | tie |
| c-c-buffer-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-callback-timing-bad | negative | 100% | 5 | 100% | 2 | tie |
| c-callback-timing-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-capability-bad | negative | 100% | 3 | 100% | 1 | tie |
| c-capability-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-comment-accuracy-bad | negative | 100% | 9 | 100% | 2 | tie |
| c-comment-accuracy-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-comment-audience-bad | negative | 100% | 10 | 100% | 2 | tie |
| c-comment-audience-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-comment-concise-bad | negative | 100% | 8 | 100% | 2 | tie |
| c-comment-concise-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-comment-wrap-bad | negative | 100% | 4 | 100% | 2 | tie |
| c-comment-wrap-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-constraint-bad | negative | 100% | 7 | 100% | 2 | tie |
| c-constraint-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-constraint-violation-bad | negative | 100% | 6 | 100% | 2 | tie |
| c-constraint-violation-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-cross-lang-errcode-bad | negative | 100% | 5 | 100% | 2 | tie |
| c-cross-lang-errcode-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-empty-enum-bad | negative | 100% | 4 | 100% | 1 | tie |
| c-empty-enum-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-empty-method-bad | negative | 100% | 8 | 100% | 2 | tie |
| c-empty-method-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-empty-property-bad | negative | 100% | 9 | 100% | 2 | tie |
| c-empty-property-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-enum-bitwise-bad | negative | 100% | 7 | 100% | 2 | tie |
| c-enum-bitwise-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-enum-equiv-bad | negative | 100% | 6 | 100% | 2 | tie |
| c-enum-equiv-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-errcode-consist-bad | negative | 100% | 5 | 100% | 2 | tie |
| c-errcode-consist-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-no-location-bad | negative | 100% | 5 | 100% | 2 | tie |
| c-no-location-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-no-personal-bad | negative | 100% | 7 | 100% | 2 | tie |
| c-no-personal-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-numeric-type-bad | negative | 100% | 7 | 100% | 2 | tie |
| c-numeric-type-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-numeric-unit-bad | negative | 100% | 6 | 100% | 2 | tie |
| c-numeric-unit-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-optional-default-bad | negative | 100% | 8 | 100% | 2 | tie |
| c-optional-default-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-param-encap-bad | negative | 100% | 6 | 100% | 2 | tie |
| c-param-encap-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-param-order-bad | negative | 100% | 15 | 100% | 2 | tie |
| c-param-order-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-param-spec-bad | negative | 100% | 6 | 100% | 2 | tie |
| c-param-spec-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-pointer-array-bad | negative | 100% | 8 | 100% | 2 | tie |
| c-pointer-array-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-positive-expr-bad | negative | 100% | 11 | 100% | 2 | tie |
| c-positive-expr-ok | positive | 100% | 0 | 0% | 3 | **with_skill** |
| c-prerequisite-bad | negative | 100% | 5 | 100% | 2 | tie |
| c-prerequisite-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| c-string-format-bad | negative | 100% | 6 | 100% | 2 | tie |
| c-string-format-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |

---

## Negative Cases (should detect issues)

| Eval | with_skill Findings | without_skill Findings | with_skill Pass | without_skill Pass |
|------|--------------------|-----------------------|-----------------|-------------------|
| c-api-coord-bad | 5 | 2 | PASS | PASS |
| c-binary-encoding-bad | 6 | 2 | PASS | PASS |
| c-c-buffer-bad | 7 | 2 | PASS | PASS |
| c-callback-timing-bad | 5 | 2 | PASS | PASS |
| c-capability-bad | 3 | 1 | PASS | PASS |
| c-comment-accuracy-bad | 9 | 2 | PASS | PASS |
| c-comment-audience-bad | 10 | 2 | PASS | PASS |
| c-comment-concise-bad | 8 | 2 | PASS | PASS |
| c-comment-wrap-bad | 4 | 2 | PASS | PASS |
| c-constraint-bad | 7 | 2 | PASS | PASS |
| c-constraint-violation-bad | 6 | 2 | PASS | PASS |
| c-cross-lang-errcode-bad | 5 | 2 | PASS | PASS |
| c-empty-enum-bad | 4 | 1 | PASS | PASS |
| c-empty-method-bad | 8 | 2 | PASS | PASS |
| c-empty-property-bad | 9 | 2 | PASS | PASS |
| c-enum-bitwise-bad | 7 | 2 | PASS | PASS |
| c-enum-equiv-bad | 6 | 2 | PASS | PASS |
| c-errcode-consist-bad | 5 | 2 | PASS | PASS |
| c-no-location-bad | 5 | 2 | PASS | PASS |
| c-no-personal-bad | 7 | 2 | PASS | PASS |
| c-numeric-type-bad | 7 | 2 | PASS | PASS |
| c-numeric-unit-bad | 6 | 2 | PASS | PASS |
| c-optional-default-bad | 8 | 2 | PASS | PASS |
| c-param-encap-bad | 6 | 2 | PASS | PASS |
| c-param-order-bad | 15 | 2 | PASS | PASS |
| c-param-spec-bad | 6 | 2 | PASS | PASS |
| c-pointer-array-bad | 8 | 2 | PASS | PASS |
| c-positive-expr-bad | 11 | 2 | PASS | PASS |
| c-prerequisite-bad | 5 | 2 | PASS | PASS |
| c-string-format-bad | 6 | 2 | PASS | PASS |

---

## Positive Cases (should NOT detect issues - false positive test)

| Eval | with_skill False Positives | without_skill False Positives |
|------|---------------------------|-------------------------------|
| c-api-coord-ok | 0 (PASS) | 1 (FAIL) |
| c-binary-encoding-ok | 0 (PASS) | 1 (FAIL) |
| c-c-buffer-ok | 0 (PASS) | 1 (FAIL) |
| c-callback-timing-ok | 0 (PASS) | 1 (FAIL) |
| c-capability-ok | 0 (PASS) | 1 (FAIL) |
| c-comment-accuracy-ok | 0 (PASS) | 1 (FAIL) |
| c-comment-audience-ok | 0 (PASS) | 1 (FAIL) |
| c-comment-concise-ok | 0 (PASS) | 1 (FAIL) |
| c-comment-wrap-ok | 0 (PASS) | 1 (FAIL) |
| c-constraint-ok | 0 (PASS) | 1 (FAIL) |
| c-constraint-violation-ok | 0 (PASS) | 1 (FAIL) |
| c-cross-lang-errcode-ok | 0 (PASS) | 1 (FAIL) |
| c-empty-enum-ok | 0 (PASS) | 1 (FAIL) |
| c-empty-method-ok | 0 (PASS) | 1 (FAIL) |
| c-empty-property-ok | 0 (PASS) | 1 (FAIL) |
| c-enum-bitwise-ok | 0 (PASS) | 1 (FAIL) |
| c-enum-equiv-ok | 0 (PASS) | 1 (FAIL) |
| c-errcode-consist-ok | 0 (PASS) | 1 (FAIL) |
| c-no-location-ok | 0 (PASS) | 1 (FAIL) |
| c-no-personal-ok | 0 (PASS) | 1 (FAIL) |
| c-numeric-type-ok | 0 (PASS) | 1 (FAIL) |
| c-numeric-unit-ok | 0 (PASS) | 1 (FAIL) |
| c-optional-default-ok | 0 (PASS) | 1 (FAIL) |
| c-param-encap-ok | 0 (PASS) | 1 (FAIL) |
| c-param-order-ok | 0 (PASS) | 1 (FAIL) |
| c-param-spec-ok | 0 (PASS) | 1 (FAIL) |
| c-pointer-array-ok | 0 (PASS) | 1 (FAIL) |
| c-positive-expr-ok | 0 (PASS) | 3 (FAIL) |
| c-prerequisite-ok | 0 (PASS) | 1 (FAIL) |
| c-string-format-ok | 0 (PASS) | 1 (FAIL) |
