# Eval Cases

The seven cases verify:

- missing-input and secret-handling boundaries;
- non-root fail-closed prerequisite checks;
- separation of SSH success from HDC target readiness;
- skipping reverse SSH when direct Linux HDC is already healthy;
- bounded reverse-SSH reconnects with configuration/runtime guidance;
- `[Empty]` recovery across HDC service, USB hardware, driver, and authorization layers;
- image/HDC-daemon diagnosis with evidence and approval before reflashing.

They also require loopback-only topology, Windows-side HDC execution, and no separate HDC server port forward.
