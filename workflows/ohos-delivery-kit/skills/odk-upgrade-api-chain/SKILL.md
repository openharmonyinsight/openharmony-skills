---
name: odk-upgrade-api-chain
description: "Use when upgrading a 0.14 or ohos-sdd/v1 legacy API Markdown chain to 0.15 language-specific API metadata. Extract confirmed facts, collect missing developer facts, dry-run the converter, then write and validate arkts/c metadata. Zero plugin dependencies."
license: MIT
---

# ODK Upgrade API Chain

## Existing artifacts first

<!-- ODK:reference contracts/skill-guides/router/document-updates.md -->
Before this skill's interview, template loading, delegation or writes, read
`contracts/skill-guides/router/document-updates.md`. Read every existing target's
full frontmatter and body first; revise it in place and preserve confirmed
content, stable IDs and evidence. Create a target only when it does not exist.
<!-- /ODK:reference -->

## Purpose

Convert a supported legacy API change before its first current metadata file is
written; mixed-language chains are converted once per language.

Supported chains:

- ODK 0.14: `proposal.md` with `API/SDK=是` and legacy `spec.md` sections
  `公共规格属性` / `逐 API 规格`
- `ohos-sdd/v1`: `spec.md` sections `API 变更分析` and `接口规格` / `接口定义`

into the 0.15 language-specific API metadata chain.

This skill is an upgrade assistant, not a compatibility layer. Execution always
uses the current metadata contract. Old Markdown facts are extracted first;
missing facts must be confirmed by the developer or an authoritative API
repository rule before writing.

## Phase flow and next step

<!-- ODK:reference contracts/skill-guides/router/phase-flow.md -->
Before phase work, read `contracts/skill-guides/router/phase-flow.md` and apply
its configured pre_hook/post_hook order. At every completion or pause, show
the next pending action and configured hooks; omit the reminder only when
the entire applicable workflow is complete. The coordinator owns this flow.
<!-- /ODK:reference -->

## Preconditions

1. Resolve exactly one ODK change directory.
2. Confirm `proposal.md` marks `API/SDK` as `是`.
3. Confirm the applicable language metadata file does not already exist; for a
   mixed-language chain, only the other language's metadata may exist.
4. Confirm `spec.md` contains a supported legacy API structure. Use `--legacy-format` only when auto-detection is insufficient. Do not use this skill for a malformed or unsupported partial chain.
5. Read the applicable API repository root `AGENTS.md` and resolve its declared knowledge and prerequisites. Use it to confirm version, schema, comment, device, and language-specific facts. Do not hardcode repository-internal paths.

## Steps

1. Read `proposal.md` in full. Extract confirmed API attributes, especially language, API type, Kit, and ArkTS static-type involvement.
2. Read the legacy `spec.md` API section in full. Preserve every unrelated spec section.
3. Run the deterministic assistant in dry-run mode:

   ```sh
   python3 "runtime/executables/upgrade-api-chain.py" \
     <change-dir> --dry-run
   ```

   In a source checkout, use `scripts/upgrade-api-chain.py`.

4. Interpret the report. Never invent a value for a `missing` or `conflict` item. Resolve it only from:
   - an explicit developer confirmation in this conversation;
   - an existing confirmed proposal/spec fact;
   - an authoritative API repository rule reached through root `AGENTS.md`.
5. Collect confirmed missing facts in a temporary JSON file using this shape:

   ```json
   {
     "arkts": {
       "branch": "<confirmed branch>",
       "commit": "<confirmed commit>",
       "filePath": "<repository-relative declaration path>",
       "apis": {
         "<api-id>": {
           "since": "<confirmed version>",
           "syscap": "<SystemCapability>",
           "platform": {
             "crossplatform": true,
             "atomicservice": true,
             "form": true
           },
           "applicationModel": "stage-only",
           "returnType": {
             "text": "<confirmed return type>",
             "en": "<English return description>",
             "zh": "<Chinese return description>"
           },
           "permissions": [],
           "deviceDifferences": {
             "enabled": false,
             "items": []
           },
           "parameters": {
             "<parameter-name>": {
               "en": "<English description>",
               "zh": "<Chinese description>"
             }
           },
           "startLine": "<confirmed positive line>",
           "endLine": "<confirmed positive line>",
           "english": {
             "description": {
               "function": "<English function>",
               "scenario": "<English scenario>",
               "effect": "<English effect>",
               "similarAPIs": "N/A",
               "defaultBehavior": "N/A",
               "constraints": "N/A",
               "activation": "<English activation>",
               "notes": "N/A"
             }
           }
         }
       },
       "english": {
         "<api-id>": {
           "description": {
             "function": "<English function>",
             "scenario": "<English scenario>",
             "effect": "<English effect>",
             "similarAPIs": "N/A",
             "defaultBehavior": "N/A",
             "constraints": "N/A",
             "activation": "<English activation>",
             "notes": "N/A"
           },
           "parameters": {
             "<parameter-name>": {
               "en": "<English description>",
               "zh": "<Chinese description>",
               "direction": "input"
             }
           },
           "returnType": {
             "en": "<English return description>",
             "zh": "<Chinese return description>"
           },
           "errorCodes": {
             "1001": {
               "constant": "<ERROR_CONSTANT>",
               "description": "<English error description>"
             }
           }
         }
       }
     }
   }
   ```

   Use a `c` object with the same layout for C. ArkTS `returnType.text`,
   `permissions`, `deviceDifferences`, and parameter descriptions must be
   confirmed. C `returnType` must also provide confirmed `text`, `semantic`,
   and `cType.kind`; C uses a `parameters` list with `name`, `cType`,
   `direction`, and bilingual `description`. For `ohos-sdd/v1`, put per-API
   facts under `apis` keyed by the generated API ID; for a mixed-language chain,
run once per language with `--language arkts` and `--language c`. The second
run preserves the first language and updates the overview to cover both. Omit unused fields. Do not put
   unconfirmed values, TODOs, or placeholders in this file.

6. Re-run dry-run with `--facts <facts.json>` until the report has:

   ```text
   Missing facts: 0
   Conflicts: 0
   Validation issues: 0
   ```

7. Write the current contract only after dry-run is clean:

   ```sh
   python3 "runtime/executables/upgrade-api-chain.py" \
     <change-dir> --write --facts <facts.json>
   ```

   The script stages and validates all outputs before replacing them and rolls
   back replaced targets on failure. It writes only:
   - `arkts-api-spec.yaml` and/or `c-api-spec.yaml`
   - the top-level `## API 规格定义` section in `spec.md`
   - `evidence/api-chain-upgrade-report.md`

8. Preserve unrelated work. Do not regenerate unrelated design sections, plan tasks, implementation code, tests, or evidence merely because the API chain was upgraded.
9. Revise existing API-related phase artifacts in place:
   - update design's API baseline marker to `API 契约版本：1.0.0`;
   - update execution-plan's API input marker to `API Contract Version | 1.0.0`;
   - revise only API-affected design decisions and tasks;
   - replace legacy mixed declaration diff evidence with the applicable language-specific diffs;
   - regenerate declaration files/diffs from the new metadata; do not edit metadata to match old diffs.
10. Run the strict validator and fix reported API-chain issues:

    ```sh
    python3 "<executables>/validate-artifacts-contract.py" \
      <change-dir>
    ```

11. Report the exact files changed, unresolved developer confirmations, and the validator result. Do not claim unrelated work was redone or validated.

## Output

Write only the applicable current API metadata files, the replaced top-level
`spec.md` API overview section, and the upgrade report. Report unresolved
missing/conflicting facts and the strict validator result. Preserve all
unrelated artifacts and explicitly state that they were not regenerated.

## Boundaries

- Never silently downgrade or ignore a newer API metadata schema.
- Never manually patch `schemaVersion`, `apiContractVersion`, or phase version markers.
- Never use an LLM to invent API IDs, declarations, repository commits, English descriptions, parameter semantics, or error constants.
- Never overwrite existing current metadata for the same language.
- Never invent source line numbers, C return types, or C return semantics.
- Never use old declaration diffs as the API contract source.
- The assistant supports ODK 0.14 and `ohos-sdd/v1` Markdown chains. It is not a general YAML schema migration tool.
