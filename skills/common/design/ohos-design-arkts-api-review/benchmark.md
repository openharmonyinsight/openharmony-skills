# Benchmark Report: ArkTS SKILL (Iteration 3)

**Generated:** 2026-06-17T03:54:26.472569+00:00
**Total Evals:** 90
**Configuration:** with_skill vs without_skill

---

## Summary

| Metric | with_skill | without_skill | Delta |
|--------|-----------|---------------|-------|
| Mean Pass Rate | 100.0% | 62.2% | +0.38 |
| Std Dev | 0.000 | 0.485 | |
| Min Pass Rate | 100.0% | 0.0% | |
| Max Pass Rate | 100.0% | 100.0% | |
| Total Findings | 400 | 126 | +274 |
| Evals Run | 90 | 90 | |

---

## Per-Eval Results

| Eval | Type | with_skill Pass Rate | with_skill Findings | without_skill Pass Rate | without_skill Findings | Winner |
|------|------|---------------------|---------------------|------------------------|------------------------|--------|
| arkts-abbreviation-bad | negative | 100% | 12 | 100% | 2 | tie |
| arkts-abbreviation-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-antonym-bad | negative | 100% | 5 | 100% | 5 | tie |
| arkts-antonym-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-binary-encoding-bad | negative | 100% | 6 | 100% | 2 | tie |
| arkts-binary-encoding-ok | positive | 100% | 0 | 100% | 0 | tie |
| arkts-callback-bad | negative | 100% | 6 | 100% | 2 | tie |
| arkts-callback-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-capability-bad | negative | 100% | 3 | 100% | 2 | tie |
| arkts-capability-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-constraint-bad | negative | 100% | 8 | 100% | 2 | tie |
| arkts-constraint-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-controversial-bad | negative | 100% | 22 | 100% | 2 | tie |
| arkts-controversial-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-declarative-bad | negative | 100% | 10 | 100% | 2 | tie |
| arkts-declarative-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-emit-event-bad | negative | 100% | 3 | 100% | 1 | tie |
| arkts-emit-event-ok | positive | 100% | 0 | 100% | 0 | tie |
| arkts-empty-class-bad | negative | 100% | 13 | 100% | 2 | tie |
| arkts-empty-class-ok | positive | 100% | 0 | 0% | 2 | **with_skill** |
| arkts-empty-enum-bad | negative | 100% | 3 | 100% | 1 | tie |
| arkts-empty-enum-ok | positive | 100% | 0 | 100% | 0 | tie |
| arkts-empty-event-bad | negative | 100% | 8 | 100% | 2 | tie |
| arkts-empty-event-ok | positive | 100% | 0 | 0% | 2 | **with_skill** |
| arkts-empty-interface-bad | negative | 100% | 10 | 100% | 2 | tie |
| arkts-empty-interface-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-empty-method-bad | negative | 100% | 29 | 100% | 2 | tie |
| arkts-empty-method-ok | positive | 100% | 0 | 0% | 2 | **with_skill** |
| arkts-empty-property-bad | negative | 100% | 9 | 100% | 2 | tie |
| arkts-empty-property-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-english-only-bad | negative | 100% | 10 | 100% | 3 | tie |
| arkts-english-only-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-enum-bitwise-bad | negative | 100% | 4 | 100% | 1 | tie |
| arkts-enum-bitwise-ok | positive | 100% | 0 | 100% | 0 | tie |
| arkts-errcode-bad | negative | 100% | 5 | 100% | 2 | tie |
| arkts-errcode-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-error-complete-bad | negative | 100% | 11 | 100% | 2 | tie |
| arkts-error-complete-ok | positive | 100% | 0 | 100% | 0 | tie |
| arkts-exception-desc-bad | negative | 100% | 10 | 100% | 2 | tie |
| arkts-exception-desc-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-func-verb-bad | negative | 100% | 20 | 100% | 2 | tie |
| arkts-func-verb-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-grammar-bad | negative | 100% | 13 | 100% | 4 | tie |
| arkts-grammar-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-industry-sync-bad | negative | 100% | 8 | 100% | 2 | tie |
| arkts-industry-sync-ok | positive | 100% | 0 | 100% | 0 | tie |
| arkts-long-async-bad | negative | 100% | 9 | 100% | 2 | tie |
| arkts-long-async-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-module-bad | negative | 100% | 6 | 100% | 2 | tie |
| arkts-module-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-naming-bad | negative | 100% | 7 | 100% | 2 | tie |
| arkts-naming-ok | positive | 100% | 0 | 100% | 0 | tie |
| arkts-no-location-bad | negative | 100% | 6 | 100% | 1 | tie |
| arkts-no-location-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-no-personal-bad | negative | 100% | 8 | 100% | 2 | tie |
| arkts-no-personal-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-null-undefined-bad | negative | 100% | 3 | 100% | 1 | tie |
| arkts-null-undefined-ok | positive | 100% | 0 | 100% | 0 | tie |
| arkts-numeric-type-bad | negative | 100% | 7 | 100% | 2 | tie |
| arkts-numeric-type-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-off-event-bad | negative | 100% | 4 | 100% | 1 | tie |
| arkts-off-event-ok | positive | 100% | 0 | 100% | 0 | tie |
| arkts-on-event-bad | negative | 100% | 4 | 100% | 1 | tie |
| arkts-on-event-ok | positive | 100% | 0 | 100% | 0 | tie |
| arkts-once-event-bad | negative | 100% | 4 | 100% | 1 | tie |
| arkts-once-event-ok | positive | 100% | 0 | 0% | 2 | **with_skill** |
| arkts-param-encap-bad | negative | 100% | 5 | 100% | 2 | tie |
| arkts-param-encap-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-param-order-bad | negative | 100% | 17 | 100% | 2 | tie |
| arkts-param-order-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-param-spec-bad | negative | 100% | 7 | 100% | 2 | tie |
| arkts-param-spec-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-positive-expr-bad | negative | 100% | 7 | 100% | 2 | tie |
| arkts-positive-expr-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-promise-bad | negative | 100% | 5 | 100% | 2 | tie |
| arkts-promise-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-query-null-bad | negative | 100% | 5 | 100% | 2 | tie |
| arkts-query-null-ok | positive | 100% | 0 | 100% | 0 | tie |
| arkts-return-desc-bad | negative | 100% | 10 | 100% | 2 | tie |
| arkts-return-desc-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-singular-plural-bad | negative | 100% | 13 | 100% | 2 | tie |
| arkts-singular-plural-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-sync-return-bad | negative | 100% | 6 | 100% | 2 | tie |
| arkts-sync-return-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-type-noun-bad | negative | 100% | 18 | 100% | 2 | tie |
| arkts-type-noun-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-uncertain-async-bad | negative | 100% | 8 | 100% | 2 | tie |
| arkts-uncertain-async-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |
| arkts-usage-limit-bad | negative | 100% | 13 | 100% | 2 | tie |
| arkts-usage-limit-ok | positive | 100% | 0 | 0% | 1 | **with_skill** |

---

## Negative Cases (should detect issues)

| Eval | with_skill Findings | without_skill Findings | with_skill Pass | without_skill Pass |
|------|--------------------|-----------------------|-----------------|-------------------|
| arkts-abbreviation-bad | 12 | 2 | PASS | PASS |
| arkts-antonym-bad | 5 | 5 | PASS | PASS |
| arkts-binary-encoding-bad | 6 | 2 | PASS | PASS |
| arkts-callback-bad | 6 | 2 | PASS | PASS |
| arkts-capability-bad | 3 | 2 | PASS | PASS |
| arkts-constraint-bad | 8 | 2 | PASS | PASS |
| arkts-controversial-bad | 22 | 2 | PASS | PASS |
| arkts-declarative-bad | 10 | 2 | PASS | PASS |
| arkts-emit-event-bad | 3 | 1 | PASS | PASS |
| arkts-empty-class-bad | 13 | 2 | PASS | PASS |
| arkts-empty-enum-bad | 3 | 1 | PASS | PASS |
| arkts-empty-event-bad | 8 | 2 | PASS | PASS |
| arkts-empty-interface-bad | 10 | 2 | PASS | PASS |
| arkts-empty-method-bad | 29 | 2 | PASS | PASS |
| arkts-empty-property-bad | 9 | 2 | PASS | PASS |
| arkts-english-only-bad | 10 | 3 | PASS | PASS |
| arkts-enum-bitwise-bad | 4 | 1 | PASS | PASS |
| arkts-errcode-bad | 5 | 2 | PASS | PASS |
| arkts-error-complete-bad | 11 | 2 | PASS | PASS |
| arkts-exception-desc-bad | 10 | 2 | PASS | PASS |
| arkts-func-verb-bad | 20 | 2 | PASS | PASS |
| arkts-grammar-bad | 13 | 4 | PASS | PASS |
| arkts-industry-sync-bad | 8 | 2 | PASS | PASS |
| arkts-long-async-bad | 9 | 2 | PASS | PASS |
| arkts-module-bad | 6 | 2 | PASS | PASS |
| arkts-naming-bad | 7 | 2 | PASS | PASS |
| arkts-no-location-bad | 6 | 1 | PASS | PASS |
| arkts-no-personal-bad | 8 | 2 | PASS | PASS |
| arkts-null-undefined-bad | 3 | 1 | PASS | PASS |
| arkts-numeric-type-bad | 7 | 2 | PASS | PASS |
| arkts-off-event-bad | 4 | 1 | PASS | PASS |
| arkts-on-event-bad | 4 | 1 | PASS | PASS |
| arkts-once-event-bad | 4 | 1 | PASS | PASS |
| arkts-param-encap-bad | 5 | 2 | PASS | PASS |
| arkts-param-order-bad | 17 | 2 | PASS | PASS |
| arkts-param-spec-bad | 7 | 2 | PASS | PASS |
| arkts-positive-expr-bad | 7 | 2 | PASS | PASS |
| arkts-promise-bad | 5 | 2 | PASS | PASS |
| arkts-query-null-bad | 5 | 2 | PASS | PASS |
| arkts-return-desc-bad | 10 | 2 | PASS | PASS |
| arkts-singular-plural-bad | 13 | 2 | PASS | PASS |
| arkts-sync-return-bad | 6 | 2 | PASS | PASS |
| arkts-type-noun-bad | 18 | 2 | PASS | PASS |
| arkts-uncertain-async-bad | 8 | 2 | PASS | PASS |
| arkts-usage-limit-bad | 13 | 2 | PASS | PASS |

---

## Positive Cases (should NOT detect issues - false positive test)

| Eval | with_skill False Positives | without_skill False Positives |
|------|---------------------------|-------------------------------|
| arkts-abbreviation-ok | 0 (PASS) | 1 (FAIL) |
| arkts-antonym-ok | 0 (PASS) | 1 (FAIL) |
| arkts-binary-encoding-ok | 0 (PASS) | 0 (PASS) |
| arkts-callback-ok | 0 (PASS) | 1 (FAIL) |
| arkts-capability-ok | 0 (PASS) | 1 (FAIL) |
| arkts-constraint-ok | 0 (PASS) | 1 (FAIL) |
| arkts-controversial-ok | 0 (PASS) | 1 (FAIL) |
| arkts-declarative-ok | 0 (PASS) | 1 (FAIL) |
| arkts-emit-event-ok | 0 (PASS) | 0 (PASS) |
| arkts-empty-class-ok | 0 (PASS) | 2 (FAIL) |
| arkts-empty-enum-ok | 0 (PASS) | 0 (PASS) |
| arkts-empty-event-ok | 0 (PASS) | 2 (FAIL) |
| arkts-empty-interface-ok | 0 (PASS) | 1 (FAIL) |
| arkts-empty-method-ok | 0 (PASS) | 2 (FAIL) |
| arkts-empty-property-ok | 0 (PASS) | 1 (FAIL) |
| arkts-english-only-ok | 0 (PASS) | 1 (FAIL) |
| arkts-enum-bitwise-ok | 0 (PASS) | 0 (PASS) |
| arkts-errcode-ok | 0 (PASS) | 1 (FAIL) |
| arkts-error-complete-ok | 0 (PASS) | 0 (PASS) |
| arkts-exception-desc-ok | 0 (PASS) | 1 (FAIL) |
| arkts-func-verb-ok | 0 (PASS) | 1 (FAIL) |
| arkts-grammar-ok | 0 (PASS) | 1 (FAIL) |
| arkts-industry-sync-ok | 0 (PASS) | 0 (PASS) |
| arkts-long-async-ok | 0 (PASS) | 1 (FAIL) |
| arkts-module-ok | 0 (PASS) | 1 (FAIL) |
| arkts-naming-ok | 0 (PASS) | 0 (PASS) |
| arkts-no-location-ok | 0 (PASS) | 1 (FAIL) |
| arkts-no-personal-ok | 0 (PASS) | 1 (FAIL) |
| arkts-null-undefined-ok | 0 (PASS) | 0 (PASS) |
| arkts-numeric-type-ok | 0 (PASS) | 1 (FAIL) |
| arkts-off-event-ok | 0 (PASS) | 0 (PASS) |
| arkts-on-event-ok | 0 (PASS) | 0 (PASS) |
| arkts-once-event-ok | 0 (PASS) | 2 (FAIL) |
| arkts-param-encap-ok | 0 (PASS) | 1 (FAIL) |
| arkts-param-order-ok | 0 (PASS) | 1 (FAIL) |
| arkts-param-spec-ok | 0 (PASS) | 1 (FAIL) |
| arkts-positive-expr-ok | 0 (PASS) | 1 (FAIL) |
| arkts-promise-ok | 0 (PASS) | 1 (FAIL) |
| arkts-query-null-ok | 0 (PASS) | 0 (PASS) |
| arkts-return-desc-ok | 0 (PASS) | 1 (FAIL) |
| arkts-singular-plural-ok | 0 (PASS) | 1 (FAIL) |
| arkts-sync-return-ok | 0 (PASS) | 1 (FAIL) |
| arkts-type-noun-ok | 0 (PASS) | 1 (FAIL) |
| arkts-uncertain-async-ok | 0 (PASS) | 1 (FAIL) |
| arkts-usage-limit-ok | 0 (PASS) | 1 (FAIL) |
