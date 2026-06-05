# OpenHarmony Device Image Flashing Skill

This skill is registered as `ohos-ci-device-image-flashing` and lives under the common CI/CD namespace:

```text
skills/common/cicd/ohos-ci-device-image-flashing/
```

## Scope

Use this skill to download OpenHarmony daily build images and flash supported real devices through `hdc` updater mode. DAYU200/RK3568 is the default example, while the helper scripts accept other component names and image layouts.

## Runtime Files

- `SKILL.md` is the agent entry point.
- `download_daily.py` queries and safely extracts a daily build image.
- `flash_device.py` discovers image partitions and flashes them through `hdc`.

## Verification

Repository-level regression tests live in `tests/test_flash_dayu200.py`.
