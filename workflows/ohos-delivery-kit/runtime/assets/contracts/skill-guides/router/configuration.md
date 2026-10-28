# Effective ODK configuration

Keep the two files together in the active installation's assets/config directory:

```text
assets/
  config/
    odk_config.yaml        # shipped defaults; refreshed on upgrade
    odk_config_ext.yaml    # user-owned overrides; preserved on upgrade
  templates/
  contracts/
  profiles/
```

Source checkout uses core/config; native and neutral packages use runtime/assets/config;
SkillHub host projections use assets/config. Always use
the directory returned by the loader, never mix files from different installs
or read a similarly named file in the business working directory.

## Shared loading command

Run the installed executable `lib/odk_repository.py` with `--effective-config`,
using the executable root resolved by the calling skill. In a source checkout
use `scripts/lib/odk_repository.py`. This read-only command prints JSON containing
`config` and `user_config_path`. It performs no writes and executes no commands.

Use the merged `config` for build products/commands, device preparation, reviews,
PR tools, CI/online-test triggers, and design-docs defaults. Do not independently
merge files in individual phases. Missing user keys inherit shipped defaults;
user keys override same-named defaults. An explicit empty string remains empty.
Space-separated list settings replace the whole default list. New default keys
are available after upgrades without copying them into the extension file.

The supported YAML subset is a flat string mapping with comments and quoted
scalars. Use `""` for empty values. Malformed quotes, duplicate keys, nulls,
nested mappings and arrays fail with the file and line; stop config-dependent
work rather than silently executing defaults. Quoted `#` characters are literal.

```yaml
build_products: arm64_virt rk3568 custom_board
build_product: rk3568
emulator_command: ""
source_cli: gh
ci_trigger: none
```

## Ownership and upgrades

Users edit the reported sibling `user_config_path`; shipped defaults are read-only
from the user's perspective. The installer must keep that extension byte-for-byte
while replacing the default and templates. Each installation/scope owns its own
overrides. When upgrading the old flat assets layout, the installer migrates its
override into config/; an existing config/ override wins, even when empty. The
loader supports an entirely old flat installation, but never mixes its override
with a new config/ default. A symlink into an immutable package store is not a writable config
location: the installer must provide a writable asset directory before customization.
Native install scripts preserve overrides before refresh; dist rebuilds preserve linked
OpenClaw and session-scoped Claude overrides. For persistent Claude updates, use
install-claude.sh (with --force for same-version refresh) so cache overrides migrate.
Installers without this preservation support require an upgrade or explicit backup
before reinstall; the ODK loader alone cannot prevent an installer deleting files.
A file already lost in an earlier update cannot be reconstructed automatically.

Reload at each phase. Implementation reuses approved execution-plan commands until
the user explicitly requests a change. A valid design-docs address still requires
submission confirmation; an empty or invalid override must ask for an address,
not silently fall back to another repository. Configuration is not authorization
for publishing or CI.
