# Eval Design

These evals check whether `ohos-dev-hdc-command-usage` changes agent behavior in the places where generic hdc advice is most likely to be unsafe or incomplete.

The cases focus on:
- selecting the intended target before mutating commands
- treating CI, multiple targets, `Unauthorized`, `Offline`, and `[Empty]` as explicit states instead of retry loops
- using layered connection diagnosis before disruptive recovery
- protecting system partition writes with probe, rollback, verification, and `sync`
- choosing install flows from package shape, especially HAP/HSP dependency layouts
- separating device logs, crash evidence, bugreport, and hdc service logs
- naming security boundaries for remote hdc servers and non-loopback forwarding

The expectations are intentionally phrased as observable output requirements so a grader can compare with-skill and baseline runs. A strong with-skill answer should include concrete `hdc` command patterns and guardrails; a weak or baseline answer will usually skip `-t`, retry blindly, remount too early, pull broad log directories, or expose remote hdc surfaces without calling out the risk.
