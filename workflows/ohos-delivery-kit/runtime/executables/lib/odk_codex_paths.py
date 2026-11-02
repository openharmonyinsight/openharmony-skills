#!/usr/bin/env python3
"""Shared Codex resource inventory, read-only install checks and owned cleanup.

Only stdlib imports are used, and all code is loaded before cleanup starts: an
installed copy may safely remove its own file when it appears in the manifest.
"""
from contextlib import contextmanager
import errno
import os
from pathlib import Path
import stat
import sys


RESOURCES = ("hooks", "skills", "templates", "profiles", "contracts", "adapters", "runtime")
PREFIXES = (".codex-plugin/",) + tuple(".codex/" + name + "/" for name in RESOURCES)
MANIFEST = (".codex-plugin", "odk-owned-files.txt")
DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW


def user_config(parts):
    return parts[-1].casefold() == "odk_config_ext.yaml"


class TargetPaths:
    def __init__(self, target):
        # The explicitly selected project root itself may be an alias.
        self.root = os.open(target, os.O_RDONLY | os.O_DIRECTORY)

    def close(self):
        os.close(self.root)

    @staticmethod
    def kind(directory, name):
        try:
            return os.stat(name, dir_fd=directory, follow_symlinks=False).st_mode
        except FileNotFoundError:
            return 0

    def error(self, error, directory, parts):
        path = "/".join(parts)
        try:
            linked = stat.S_ISLNK(self.kind(directory, parts[-1]))
        except OSError:
            linked = False
        reason = ("refusing symlink" if linked else
                  "not a directory" if error.errno == errno.ENOTDIR else
                  "permission denied" if error.errno in (errno.EACCES, errno.EPERM) else
                  "filesystem operation failed")
        name = errno.errorcode.get(error.errno, "UNKNOWN")
        return ValueError(f"{reason}: {path} [{name}, errno={error.errno}: {error.strerror}]")

    @contextmanager
    def parent_directory(self, parts):
        descriptor = os.dup(self.root)
        try:
            for index, component in enumerate(parts[:-1]):
                try:
                    child = os.open(component, DIRECTORY_FLAGS, dir_fd=descriptor)
                except FileNotFoundError:
                    yield None
                    return
                except OSError as error:
                    raise self.error(error, descriptor, parts[:index + 1]) from error
                os.close(descriptor)
                descriptor = child
            yield descriptor
        finally:
            os.close(descriptor)

    def read_manifest(self):
        with self.parent_directory(MANIFEST) as directory:
            if directory is None:
                return None
            try:
                source = os.open(MANIFEST[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                                 dir_fd=directory)
            except FileNotFoundError:
                return None
            except OSError as error:
                raise self.error(error, directory, MANIFEST) from error
            with os.fdopen(source, encoding="utf-8", errors="surrogateescape") as stream:
                if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                    raise ValueError("owned-files manifest must be a regular file: " + "/".join(MANIFEST))
                return stream.read().splitlines()

    def owned_paths(self, entries):
        paths = []
        seen = set()
        preserved = invalid = 0
        for value in entries:
            if not value:
                continue
            reason = ("absolute path" if value.startswith("/") else
                      "traversal path" if ".." in value.split("/") else
                      "non-ODK path" if not value.startswith(PREFIXES) else None)
            if reason:
                print("  reject " + reason + ": " + value, file=sys.stderr)
                invalid += 1
                continue
            parts = tuple(part for part in value.split("/") if part and part != ".")
            with self.parent_directory(parts) as directory:
                try:
                    kind = self.kind(directory, parts[-1]) if directory is not None else 0
                except OSError as error:
                    raise self.error(error, directory, parts) from error
                if kind and not (stat.S_ISREG(kind) or stat.S_ISLNK(kind)):
                    raise ValueError("owned entry must be a regular file or leaf symlink: " + value)
            if user_config(parts):
                preserved += 1
            elif parts != MANIFEST and parts not in seen:
                paths.append(parts)
                seen.add(parts)
        if invalid:
            raise ValueError(f"manifest contains {invalid} unsupported or unsafe entries; repair the manifest before retry")
        return paths, preserved

    def check_install(self, package):
        expected = {".codex-plugin", *RESOURCES}
        actual = {path.name for path in package.iterdir() if path.is_dir()}
        if actual != expected:
            raise ValueError("package resource inventory differs from RESOURCES: "
                             f"unexpected={sorted(actual - expected)}, missing={sorted(expected - actual)}")
        entries = self.read_manifest()
        owned = set(self.owned_paths(entries)[0]) if entries is not None else set()
        for resource in (".codex-plugin", *RESOURCES):
            source = package / resource
            if source.is_symlink():
                raise ValueError("package contains unsupported symlink: " + str(source))
            prefix = (resource,) if resource == ".codex-plugin" else (".codex", resource)
            for current, directories, files in os.walk(source):
                relative = Path(current).relative_to(source).parts
                parts = prefix + relative
                # Include empty package directories, but never inspect unrelated
                # user directories which the package will not touch.
                with self.parent_directory(parts + ("_",)):
                    pass
                for name in directories + files:
                    if (Path(current) / name).is_symlink():
                        raise ValueError("package contains unsupported symlink: " + str(Path(current) / name))
                for name in files:
                    leaf = parts + (name,)
                    with self.parent_directory(leaf) as directory:
                        try:
                            kind = self.kind(directory, name) if directory is not None else 0
                        except OSError as error:
                            raise self.error(error, directory, leaf) from error
                        if stat.S_ISLNK(kind) and leaf not in owned:
                            raise ValueError("refusing unowned destination file symlink: " + "/".join(leaf))
                        if kind and not (stat.S_ISREG(kind) or stat.S_ISLNK(kind)):
                            raise ValueError("destination file has incompatible type: " + "/".join(leaf))

    def uninstall(self, target, quiet):
        entries = self.read_manifest()
        if entries is None:
            print("No ODK owned-files manifest found at " + str(Path(target).joinpath(*MANIFEST)) + ".", file=sys.stderr)
            print("Cannot safely uninstall without risking the user's own Codex files.\n"
                  "If this was a pre-manifest install, inspect ODK files under:", file=sys.stderr)
            for parts in ((".codex-plugin",),) + tuple((".codex", item) for item in RESOURCES):
                print("  " + str(Path(target).joinpath(*parts)) + "/", file=sys.stderr)
            raise ValueError("keep user files and user-owned odk_config_ext.yaml when checking these shared directories")
        paths, preserved = self.owned_paths(entries)
        removed = 0
        # Preflight has completed for ALL entries before the first unlink.
        for parts in paths + [MANIFEST]:
            with self.parent_directory(parts) as directory:
                if directory is None:
                    continue
                try:
                    kind = self.kind(directory, parts[-1])
                    if stat.S_ISREG(kind) or stat.S_ISLNK(kind):
                        os.unlink(parts[-1], dir_fd=directory)
                        removed += 1
                    elif kind:
                        raise ValueError("owned entry changed to incompatible type: " + "/".join(parts))
                except OSError as error:
                    raise self.error(error, directory, parts) from error
        if not quiet:
            print(f"Removed {removed} ODK-owned files from {target} (preserved {preserved} user configs).")


def main(argv):
    if argv == ["resources"]:
        print("\n".join(RESOURCES))
        return 0
    if len(argv) != 3 or argv[0] not in ("check-install", "uninstall"):
        print("Usage: odk_codex_paths.py resources | check-install TARGET PACKAGE | uninstall TARGET QUIET", file=sys.stderr)
        return 1
    paths = None
    try:
        paths = TargetPaths(argv[1])
        if argv[0] == "check-install":
            paths.check_install(Path(argv[2]))
        else:
            paths.uninstall(argv[1], argv[2] == "true")
        return 0
    except (OSError, ValueError) as error:
        print("Error: " + str(error) + "; owned-files manifest retained for retry.", file=sys.stderr)
        print("Restore the reported directory as a real directory or correct its permissions; "
              "for rejected entries, verify ownership and repair the manifest, then retry.", file=sys.stderr)
        return 1
    finally:
        if paths is not None:
            paths.close()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
