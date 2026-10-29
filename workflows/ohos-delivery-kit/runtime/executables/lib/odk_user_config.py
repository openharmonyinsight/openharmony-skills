"""Preserve installation-local user configuration across native refreshes."""
import json
import os
from pathlib import Path
import shutil
import sys

EXT = 'odk_config_ext.yaml'
EMPTY = '# User overrides for the adjacent odk_config.yaml.\n'


def snapshot(assets, backup):
    assets, backup = Path(assets), Path(backup)
    for candidate in (assets / 'config' / EXT, assets / EXT):
        if candidate.is_symlink():
            raise ValueError(f'User config must be a regular file: {candidate}')
        if candidate.exists():
            if not candidate.is_file():
                raise ValueError(f'User config must be a regular file: {candidate}')
            shutil.copy2(candidate, backup)
            return
    backup.write_text(EMPTY)
    backup.chmod(0o600)


def restore(backup, assets):
    assets = Path(assets)
    directory = assets / 'config'
    if directory.is_symlink() or assets.is_symlink():
        raise ValueError(f'User config must not write through symlink: {directory}')
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / EXT
    if target.is_symlink():
        raise ValueError(f'User config must not write through symlink: {target}')
    shutil.copy2(backup, target)


def claude_assets():
    """Locate only the user-scope cache managed by install-claude.sh.

    Project-scope entries are intentionally excluded from this migration.
    """
    root = Path(os.environ.get('CLAUDE_CONFIG_DIR', str(Path.home() / '.claude')))
    registry = root / 'plugins/installed_plugins.json'
    if not registry.exists():
        return None
    data = json.loads(registry.read_text())
    entries = data.get('plugins', {}).get('ohos-delivery-kit@ohos-delivery-kit-local', [])
    if isinstance(entries, dict):
        entries = [entries]
    users = [e for e in entries if e.get('scope', 'user') == 'user']
    if len(users) > 1:
        raise ValueError('Ambiguous Claude user installation; refusing to select a config')
    return Path(users[0]['installPath']) / 'runtime/assets' if users else None


if __name__ == '__main__':
    command, *args = sys.argv[1:]
    if command == 'snapshot':
        snapshot(*args)
    elif command == 'restore':
        restore(*args)
    elif command == 'claude-assets':
        assets = claude_assets()
        print(assets or '')
    elif command == 'migrate-dist':
        old, new = map(Path, args)
        for relative in ('claude', 'codex', 'opencode/.opencode/ohos-delivery-kit',
                         'openclaw', 'claude-marketplace/plugins/ohos-delivery-kit'):
            source = old / relative / 'runtime/assets'
            dest = new / relative / 'runtime/assets'
            if any(p.exists() or p.is_symlink() for p in (source / 'config' / EXT, source / EXT)):
                backup = dest / '.user-config-backup'
                snapshot(source, backup)
                restore(backup, dest)
                backup.unlink()
    else:
        raise ValueError(f'Unknown command: {command}')
