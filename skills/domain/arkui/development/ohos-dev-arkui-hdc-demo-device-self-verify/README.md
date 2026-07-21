# ArkUI HDC Demo Device Self Verify

This skill guides device-side end-to-end self-verification for OpenHarmony ArkUI and ACE Engine changes. It covers pushing artifacts through HDC, installing or replacing the tested artifact, launching a demo, collecting UI/log evidence, and reporting pass or blocker criteria.

Use `ohos-dev-hdc-reverse-ssh-setup` first when the Linux build host must access the device through a Windows USB host.

## Dependency index

Install or verify the shared HDC foundation before first use:

```bash
bash scripts/install_related_skills.sh
```

The dependency index points to `ohos-dev-hdc-command-usage`, which owns generic HDC target selection, connection diagnosis, install/file-transfer decisions, system-write guardrails, and log collection. This ArkUI skill adds reverse-SSH delegation, ability/window/UI evidence, native-library load proof, and end-to-end pass criteria.
