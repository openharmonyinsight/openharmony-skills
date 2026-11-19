"""Preserve installation-local user configuration across native refreshes."""
import errno
import json
import os
import shutil
import stat
import sys
import tempfile
from pathlib import Path

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
            # Open with O_NOFOLLOW so a symlink swapped in between the
            # is_symlink check and the read is rejected atomically (S1).
            try:
                fd = os.open(str(candidate), os.O_RDONLY | os.O_NOFOLLOW)
            except OSError as error:
                if error.errno == errno.ELOOP:
                    raise ValueError(
                        f'User config must be a regular file: {candidate}') from error
                raise
            # Preserve the source permission bits on the backup. Read the mode
            # from the already-open source fd (never the path) so the O_NOFOLLOW
            # protection stays intact, and fchmod the backup fd so the final mode
            # is independent of the process umask. The previous open(backup,
            # 'wb') created 0644 under a typical 022 umask, which restore() then
            # shutil.copy2'd onto the published config, silently widening a
            # user's 0600 odk_config_ext.yaml to 0644.
            with os.fdopen(fd, 'rb') as src:
                # O_NOFOLLOW rejects a symlink planted at the backup path (S1).
                # Do not add O_EXCL: the native installers pass an existing
                # mktemp file as the backup target (scripts/lib/
                # odk_user_config.sh), so refusing pre-existing regular files
                # would break every install.
                backup_fd = os.open(
                    str(backup),
                    os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW,
                    0o600)
                try:
                    mode = stat.S_IMODE(os.fstat(src.fileno()).st_mode)
                    os.fchmod(backup_fd, mode)
                    dst = os.fdopen(backup_fd, 'wb')
                except BaseException:
                    os.close(backup_fd)
                    # Do not leave a half-created backup behind (C2): the
                    # O_CREAT above may already have created the path.
                    try:
                        os.unlink(str(backup))
                    except OSError:
                        pass
                    raise
                with dst:
                    shutil.copyfileobj(src, dst)
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
    # Write to a temp file and atomically replace to avoid TOCTOU (S2):
    # os.replace swaps the directory entry itself, so a symlink appearing
    # at target between the check and the rename is replaced, not followed.
    tmp = tempfile.NamedTemporaryFile(dir=directory, delete=False, suffix='.tmp')
    tmp_name = tmp.name
    tmp.close()
    try:
        shutil.copy2(backup, tmp_name)
        os.replace(tmp_name, target)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def claude_assets():
    """Locate only the user-scope cache managed by install-claude.sh.

    Project-scope entries are intentionally excluded from this migration.
    """
    root = Path(os.environ.get('CLAUDE_CONFIG_DIR', str(Path.home() / '.claude')))
    registry = root / 'plugins/installed_plugins.json'
    if not registry.exists():
        return None
    data = json.loads(registry.read_text(encoding="utf-8"))
    entries = data.get('plugins', {}).get('ohos-delivery-kit@ohos-delivery-kit-local', [])
    if isinstance(entries, dict):
        entries = [entries]
    users = [e for e in entries if e.get('scope', 'user') == 'user']
    if len(users) > 1:
        raise ValueError('Ambiguous Claude user installation; refusing to select a config')
    if not users:
        return None
    install_path = Path(users[0]['installPath'])
    # S3: validate user-controlled installPath before using it as a filesystem
    # path. An attacker who can modify the registry JSON must not redirect
    # snapshot/restore to an unexpected location.
    if not install_path.is_absolute():
        raise ValueError(f'installPath must be absolute: {install_path}')
    if '..' in install_path.parts:
        raise ValueError(f'installPath must not contain path traversal: {install_path}')
    return install_path / 'runtime/assets'


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
