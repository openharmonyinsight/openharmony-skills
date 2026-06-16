# hidumper Dump Field Reference

Use `hidumper -s MultimodalInput -a '-G'` when a test phase needs auditable MMI state evidence.

| Section | Field | Meaning |
| --- | --- | --- |
| RuntimeBindings | `deviceId=N displayId=N groupId=N` | HID device binding relationship |
| DisplayGroups | `groupId displays mainDisplayId focusWindowId` | Display group configuration |
| PointerStateByGroup | `cursorPos mouseLocation captureMode` | Per-group cursor position and capture mode |
| KeyboardStateByGroup | `focusWindowId` and key state | Per-group keyboard focus and pressed keys |
| SequenceSnapshots | type, group, targetWindow | Recent event sequence snapshots; may be empty because entries have TTL |
| SoftCursorRS | `displayId cursorPos direction drawFlag` | Soft cursor rendering state |
| PointerStyleByWindow | `pid windowId groupId style(id/size/color)` | Per-window pointer style |
| PointerDrawingRS / Display Info | display table | Registered displays |
| PointerDrawingRS / Cursor Info | `windowId lastPhysicalX/Y` | Current highest zOrder hit-test target at the cursor position |

Interpretation rules:

- `DisplayGroups.focusWindowId=-1` for `MAIN_GROUPID` can be normal. The dump reads `displayGroupInfoMap_`; main-group focus can come from `UpdateWindowInfo`.
- `Cursor Info.windowId` is the hit-test target for the physical cursor position, not necessarily the keyboard focus window.
- `SequenceSnapshots` can be empty if the dump is delayed. Capture immediately after event injection when sequence evidence matters.
- `RuntimeBindings` being `(empty)` means no active device binding.
