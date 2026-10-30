# Ensure a configured skill is available before invoking it

Use this procedure immediately before an applicable configured skill runs.
It covers `pre_commit_reviews`, `post_commit_reviews`, `post_cr_mr_pr_hooks`,
`device_flash_skill`, and the `skill:<name>` modes of `ci_trigger` and
`online_test_trigger`. Empty values and non-skill trigger modes need no skill
installation. CLI names and shell commands are not skill names.

## Check, locate, install, resume

1. Check the **current agent's** available skills and installation/discovery
   mechanism for the configured identity. An unqualified name such as `odk-review`
   may resolve to a unique installed skill's declared name; retain its discovered
   plugin namespace when invoking it. Resolve ambiguous same-name skills before
   proceeding. If available, load and invoke it with the original step's context.
   Distinguish an absent installation from an installed skill awaiting discovery.
   For an existing installation, use a supported discovery refresh; if it is
   disabled or needs a later turn/restart, keep the step pending and report how
   to resume. Do not reinstall over it or silently enable a disabled plugin.
   A skill installed only in another agent does not satisfy the current agent.
2. If missing, run the same installed `lib/odk_repository.py` resolved for
   [configuration.md](configuration.md), with
   `--skill-install-hints <config-key> --skill <configured-name>`.
   Source checkout example:

   ```sh
   python3 scripts/lib/odk_repository.py --skill-install-hints pre_commit_reviews --skill my-security-review
   ```

   The read-only JSON lists candidate URLs with their config file, comment line
   and match type. It searches the parameter's preceding comment section in the
   active `odk_config_ext.yaml` first, then `odk_config.yaml`; adjacent keys may
   share a section. It never searches other installations or unrelated sections.
   The legacy `post_pr_hooks` alias follows the configuration loader's precedence.
3. Inspect the linked installation instructions or skill source. An `explicit`
   annotation binds a URL to a name; `path` means the URL contains the skill
   name; `reference` means a general repository/catalog link. All require checking
   the actual skill identity and supported installation method. A collection
   link is not permission to install every skill. Locate the requested skill's
   `SKILL.md` and install only that skill (and required dependencies). Prefer
   a matching user-override link; do not substitute an unrelated community
   review skill for a missing built-in `odk-review`. If several sources remain
   plausible, ask for the intended source rather than selecting an arbitrary URL.
4. Install through the current agent's supported installer, following the source
   instructions and the current project's installation scope. Use a user-level
   scope only when that is the supported scope for the current setup. Target
   only the running agent; reuse existing installation authorization and do not
   ask a redundant confirmation for this requested install-before-run behavior.
   Pass URLs/paths as data to the installer; do not execute shell text copied
   from YAML comments or overwrite an existing unrelated installation.
5. Recheck actual availability and identity, then load and invoke the skill.
   Preserve the original invocation order and context (diff, confirmed CR/MR/PR
   URL, or selected device). A successful install is not a successful review,
   CI run, test or flash. If the client exposes newly installed skills only on
   a later turn or after restart, record the pending key, skill and step, explain
   how to resume, and wait until the skill is discoverable before execution.

No link, inaccessible source, mismatched identity, unavailable installer or
failed installation: report the missing skill, searched config paths and pending
step; stop that dependent step. Do not mark it PASS, silently skip a configured
review/hook, or repeatedly try unrelated sources. Report partial results when a
source CR/MR/PR already exists; an install failure does not roll it back.

## Applicability comes first

- Reviews and post-submission hooks: ensure each skill just before its turn in
  the configured ordered list; do not preinstall the entire configuration.
- CI and online tests: resolve `none`/skip and the user's trigger choice first.
  Only an authorized `skill:` action reaches this procedure. Installing a skill
  does not itself authorize a comment, label, CI run or online test.
- Device flashing: planning only records the method. Ensure the skill only
  during execution when product `rk3568`, nonempty `device_flash_skill`, the
  plan's `daily` strategy, selected target device and explicit flash/overwrite
  confirmation all apply. QEMU, other products and `existing` never install it.

## Writing installation hints

Place the link above its configuration key in `odk_config_ext.yaml`. Existing
plain repository/installation URLs are supported; an annotation makes the
intended skill unambiguous, especially for a shared section or skill collection:

```yaml
# skill-install: my-security-review https://github.com/your-team/reviews/tree/main/skills/my-security-review
pre_commit_reviews: odk-review my-security-review

# skill-install: my-ci-trigger https://gitcode.com/your-team/skills/tree/main/my-ci-trigger
ci_trigger: skill:my-ci-trigger
```

`skill-install` is a comment convention, not a new YAML setting. A comment link
does not alter the configured skill name or the existing action permissions.
