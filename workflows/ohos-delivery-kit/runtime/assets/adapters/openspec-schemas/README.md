# OpenSpec Schemas — ODK Alignment

This directory contains OpenSpec schemas customized for the ODK (ohos-delivery-kit) delivery workflow.

## ohos-spec-driven

An OpenSpec schema that aligns with ODK's artifact templates. It preserves OpenSpec's native structure while adding ODK-required sections to each artifact.

### ODK-Required Sections Added

| Artifact | OpenSpec Native Sections | ODK-Added Sections |
|----------|--------------------------|--------------------|
| proposal.md | Why, What Changes, Capabilities, Impact | target_release frontmatter, non-goals, 1+8 device variation, 外部依赖, success criteria table, 8-dimension N/A table |
| design.md | Context, Goals, Decisions, Risks | module impact table, verification approach table |
| spec.md | ADDED/MODIFIED/REMOVED deltas | AC-X.Y numbering, compatibility declaration, verification mapping table |
| tasks.md | Checkbox format (X.Y) | AC-Task traceability table, code scope per task, completion criteria |

### Installation

The schema and its templates are passive adapter assets, distributed with both
native plugins and neutral packages. From the installed asset root (or `core/`
in the source checkout), copy the complete directory to the business repository:

```bash
cp -r adapters/openspec-schemas/ohos-spec-driven/ <business-repo>/openspec/schemas/ohos-spec-driven/
```

### Configuration

In the business repository's `openspec/config.yaml`, set:

```yaml
schema: ohos-spec-driven
```

### Usage with ODK Bridge Skills

When using ODK bridge skills (`odk-ops-propose`, `odk-ops-apply`), verify the
selected schema through the OpenSpec CLI. Native artifacts stay under the selected
OpenSpec root: do not redirect `openspec/changes/`, rename tasks.md, or flatten
native delta specs. OpenSpec owns task progress and main-spec merging.

The packaged `lib/odk_openspec.py` captures native status and apply instructions,
with immutable source snapshots. The agent then reads existing ODK artifacts and
reconciles the delivery projection in place. Output modes affect that projection
only. See `../../contracts/skill-guides/router/openspec-state.md`, relative to
this README, for the complete lifecycle. Lite delivery uses ODK base commands.

Integration was checked against OpenSpec 1.16.0 with the shipped schema:
project-local blocked/ready/all_done transitions and an external `--store` capture.
Snapshots use paths relative to the selected OpenSpec root and bindings use a
project path relative to the ODK change directory. Binding replacement is atomic
and captures are serialized. Other CLI versions and store topologies need their
own verification; deterministic protocol fixtures do not replace that check.
