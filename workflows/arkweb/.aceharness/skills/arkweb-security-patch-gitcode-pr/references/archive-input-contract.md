# Archive Input Contract

Batch archive input may be a symlink. Resolve it before deciding whether files
are missing:

```bash
node skills/arkweb-security-patch-gitcode-pr/scripts/resolve_archive_dir.mjs <archive-dir>
```

The submit step must not run plain `find <archive-dir>` on a symlink root and
then treat empty output as proof that `04_final_archive.md` is missing. A
missing archive is real only when the resolved directory or a symlink-following
scan has no current issue directory containing `04_final_archive.md`.

Single issue mode accepts a directory that directly contains
`04_final_archive.md`. Batch mode accepts a run directory whose numeric
children contain `04_final_archive.md`.
