# Check for an ODK update before work

This procedure belongs to `using-odk`, `odk-init` and `odk-propose`. It runs before
resource checks, phase questions or document mutations. Loading `using-odk` for
ordinary coding or when ODK is disabled does not activate it.

## Locate the installation

Identify the current client (`codex`, `claude` or `opencode`), the installed
scope (`user` or `project`) and the installation that owns the loaded SKILL.md.
Follow symlinks to identify the installation; do not reread the skill file to
infer what this conversation already loaded.

Match that installation to the current client's host entry in the user registry
`~/.oh-skillhub/registry.json` or the business repository's
`.oh-skillhub/registry.json`. Resolve project scope at the repository root and
run subsequent commands there. If both scopes contain the plugin, use the
loaded skill's projection/store path to identify the owner. If ownership is
ambiguous, do not select or overwrite either installation.

Use `plugins.ohos-delivery-kit.hosts[agent]` for this client's installed version,
store and source. Older schema-2 records without per-host fields inherit the
plugin-level fields; those shared fields alone do not describe another client's
version after a single-client update. Never remove another client's record or
upgrade it as part of this request.

For a source checkout or installation not managed by oh-skillhub (including
OpenClaw), report the unsupported update path and continue without migrating it.

## Use the version in the loaded content

Rendered skills carry a `PLUGIN_LOAD_SNAPSHOT` block **in their body**, containing
JSON `plugin`, `version` and `skill` fields. Obtain `loaded-version` from the
matching block already present in the skill content or bootstrap supplied to this
conversation, not from a new file/tool read. Only use a snapshot whose `plugin`
is `ohos-delivery-kit` and whose installation matches the selected scope.

Keep the router/bootstrap's original snapshot for that installation for the
client session. It remains authoritative if a later init/propose load supplies a
newer snapshot from a replaced projection. With no router/bootstrap, use the
direct entry skill's snapshot and retain it for that session. A new request,
cleared resource self-check, changed disk file or newer registry entry does not
replace the session's loaded version. Do not combine snapshots from other scopes.

An installed `plugin.yaml`, `.codex-plugin/plugin.json`,
`.claude-plugin/plugin.json`, or OpenCode's plugin-root `package.json` describes
the **current disk installation**, not the cached session. Likewise, the current
registry's `storePath` identifies the installed store, not necessarily the one
loaded by this session. Use these files only to locate/diagnose the installation;
never substitute their versions for `loaded-version`.

If the managed installation has no valid snapshot in the loaded context, its
loaded version is unknown. Older installers may never inject a snapshot, so a
restart alone cannot repair this condition. Say **“当前会话缺少可验证的 ODK 版本快照，
已跳过更新检查，将继续原操作。”**, skip the optional check and upgrade, and continue
the original command. Do not ask for a restart merely because the snapshot is
missing, guess a version from disk, or report `up-to-date`. Never use
`proposal.md`'s `target_release`, an arbitrary checkout or the newest cache as a
substitute. Explain that automatic checks require a compatible installer and a
refreshed installation; do not automatically install or switch channels.

An already established pending restart or incomplete upgrade takes precedence:
keep that request stopped and report the actual pending step. Missing snapshot
support does not clear a restart required by an observed version mismatch, a
successful upgrade, or a partially failed host refresh. A valid snapshot still
uses the normal check below; `restart-required` continues to stop phase work.

## Check without upgrading

Use the current client and scope, replacing the placeholders and supplying the
loaded skill version:

```sh
npx --yes oh-skillhub@latest plugin check-update ohos-delivery-kit --agent <agent> --scope <scope> --current-version <loaded-version> --json
```

This requires an oh-skillhub release with `plugin check-update`. It may refresh
its source cache, but must not install a plugin or alter registry, projection,
host registration or business files. Do not substitute `plugin update`, even
with an assumed skip-if-current behavior, for a missing check command.

Read the returned JSON `status`:

- `up-to-date`: continue the original command.
- `update-available`: show `currentVersion`, `installedVersion` and
  `latestVersion` as relevant, then ask the user to choose **升级并重启后使用**
  or **暂不升级，继续当前操作**. Wait for an explicit answer before an upgrade.
  No answer, an autonomous workflow, a recommended default, or approval of a
  delivery document is not consent to upgrade. Declining continues the original
  command using the loaded version.
- `restart-required`: the installation was already upgraded while this skill
  is still old. Remind the user to restart the client and rerun the original
  command; stop this request without another upgrade or phase work.
- `unmanaged`, `channel-conflict` or `installation-mismatch`: briefly explain
  that the current installation cannot be updated through this path. Continue
  the original command without changing installation channels, scopes or hosts.
- Missing CLI/Node/network, unknown command, invalid JSON/version, timeout, or
  any other check failure: say **“未能检查 ODK 更新，将继续使用当前版本。”**
  with the short reason and continue. Do not claim the version is current.

The optional update check must not block normal ODK work when the installer is
unavailable. This fallback does not convert an unknown loaded version into a
verified current version or clear a pending restart.

## Upgrade only after the user chooses it

Execute the returned `updateCommand` as an argument list. Set the subprocess
environment `OH_SKILLHUB_SOURCE_DIR` to `sourceDirectory`, and
`OH_SKILLHUB_SOURCE` / `OH_SKILLHUB_REF` to the returned `source.repository` /
`source.ref`. This pins the upgrade to the source just checked instead of a
neighboring local workspace or a different channel. Keep `--atomic` and
`--strict`; do not add `--force`, switch to `--agent all`, or broaden scope.

Then run each returned `hostUpdateCommands` in order, retaining its explicit
scope and JSON options. Claude needs its native plugin update after the SkillHub
projection update; an unscoped native command may update another installation.
Verify its JSON result and native installed-plugin record for the selected
scope (and matching project path) report `latestVersion`.

Codex's installer must refresh the actual native cache with `codex plugin add`
under the running client's `CODEX_HOME` and verify its plugin ID and version. A
project installation uses its host record's project-specific plugin reference,
with activation in project settings; do not substitute the user plugin reference
or change the client home to the project's `.codex` directory. Registering
an existing marketplace alone does not refresh that cache. OpenCode must use the
adapter for its CLI capabilities: V1's native installer or V2's selected local
plugin/skills configuration. A successful config write does not mean the running
OpenCode process has reloaded its cached bootstrap.

Report success only after all commands succeed and the selected host's registry
record and native installation agree on `latestVersion`. Keep the original
session snapshot unchanged until the client restarts. If either step fails, report the failed step and actual installation
state; do not claim success or keep retrying automatically. A failed Claude
native refresh must be reported as a pending host refresh, even if the registry
and projection were already upgraded. Stop the request so phases do not read
partially refreshed resources.

After success say:

> ODK 已从 <old-version> 升级到 <new-version>。请重启当前客户端后生效，再重新执行 <original-command>。

End this request. Do not create the init skeleton, generate the proposal, route
to another phase, automatically restart the client, or claim that this session
already uses the new skill. Keep the original command and arguments in the
reminder so the user can resume after restarting. Discard any cached resource
self-check after the installation changes.

## Avoid duplicate prompts

Within one user request, `using-odk` and a routed init/propose share one check
and one choice for the same client, scope, source and installed/loaded version.
Direct entry into init/propose still checks. Recheck on the next independent
user request or if the installation identity changes. Do not persist approval
for future releases or interpret a previous decline as a permanent preference.
