# OpenHarmony Device Image Flashing Skill

This skill is registered as `ohos-test-device-image-flashing` and lives under the common testing namespace:

```text
skills/common/testing/ohos-test-device-image-flashing/
```

## Scope

Use this skill to download OpenHarmony daily build images and flash supported real devices through `hdc` updater mode. DAYU200/RK3568 is the default example, while the helper scripts accept other component names and image layouts.

## Runtime Files

- `SKILL.md` is the agent entry point.
- `download_daily.py` queries and safely extracts a daily build image.
- `flash_device.py` discovers image partitions and flashes them through `hdc`.
- `evals/` contains seed prompts and expected behaviors for skill evaluation.
- `tests/` contains helper regression tests.

## Verification

Run:

```bash
python3 -m unittest skills/common/testing/ohos-test-device-image-flashing/tests/test_device_image_flashing.py
```
