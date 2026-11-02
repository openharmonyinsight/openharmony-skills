# OpenSpec native state and ODK projection

OpenSpec owns its selected native workspace, artifact graph, delta specifications
and tracked task file. ODK owns its delivery documents and final validation.
Never redirect a native OpenSpec write into codespec or rename its tasks.md.
The strict/passthrough/merge choice applies only to the ODK projection.

1. Read existing ODK and native documents first, following document-updates.md.
   Resolve the selected OpenSpec root/store with its CLI. Keep the same project,
   change and optional `--store` selection on every native command. Reuse an
   existing change; do not run `new change` over an existing one. If CLI/project
   initialization is unavailable, report fallback to ODK base skills explicitly.
2. In an initialized project, install/select the shipped `ohos-spec-driven`
   schema through OpenSpec's supported custom-schema mechanism; preserve an
   existing schema/config and edit only the requested setting. Verify the
   selected `schemaName` with `openspec status --change NAME --json`. The schema
   preserves native proposal.md, specs/**/*.md, design.md and tasks.md paths.
   It requires standard/critical delivery; lite uses the ODK base flow to avoid
   inventing a native schema that can omit the design artifact.
3. Propose revises/creates artifacts **at the native CLI-returned paths**.
   Apply obtains `openspec instructions apply --change NAME --json`, respects
   its blocked state, and updates tasks at their returned sourcePath/line.
   Read existing native target contents before each edit. Refresh instructions
   after each completion so native progress remains authoritative.
4. Run the packaged `lib/odk_openspec.py` with the existing ODK change directory,
   `--project PROJECT --change NAME` and `--store ID` when selected. In a source
   checkout the executable is `scripts/lib/odk_openspec.py`. The helper calls
   native status/apply instructions, captures the CLI-returned source files as
   immutable evidence, and updates openspec-binding.json without replacing ODK
   documents. CLI failure is not a successful synchronization. Preserve binding
   task_map and unknown fields; a different change/store requires resolving the
   existing binding explicitly.
5. Read the captured source and **reconcile** existing ODK documents against it.
   For strict mode use the effective ODK contract; retain ODK-only decisions and
   stable AC/Task IDs. Keep a task_map in openspec-binding.json from each native
   task number to its ODK Task ID. Record the native source path/task number in
   each projected Task. Update ODK task status, actual files and verification
   evidence from the same native task; never infer test success from a checkbox.
   Report ambiguities instead of replacing either document or renumbering IDs.
6. Recapture native state after apply and reconcile the changed projection before
   ODK review/validation. A blocked/incomplete native task must remain pending in
   ODK. Only native `all_done` plus reconciled ODK evidence permits handoff.
   Native completion alone does not mean ODK validation passed.

OpenSpec archive and main-spec merge remain native operations and require their
own user authorization. Before archiving a native change, capture its final
state, reconcile ODK and retain the immutable snapshot. Do not delete native
delta specs merely because an ODK spec.md was produced. ODK design-docs
publication remains separate and does not publish the native workspace.

The adapter depends on CLI JSON capabilities (status plus apply instructions,
contextFiles and state); an unsupported response stops capture explicitly.
Snapshots normalize paths relative to the CLI-selected native root; the binding's
project path is relative to the ODK change directory. A checkout relocation does
not change the snapshot hash. A selected store may live outside the implementation
checkout. Captures hold a per-change file lock and publish the binding through a
same-directory temporary file and atomic replacement; existing task_map and notes
remain intact. Old absolute bindings migrate only when they identify this project.

OpenSpec 1.16.0 was exercised with the shipped ohos-spec-driven schema: project-local
blocked → ready → all_done capture, plus an external selected store via --store.
Protocol tests also use deterministic CLI fixtures for failures and preservation.
Other upstream versions and every possible store topology remain unverified.
