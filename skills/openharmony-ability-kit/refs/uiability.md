# UIAbility API Reference

## Import
```ts
import { UIAbility } from '@kit.AbilityKit';
```

## Attributes
| Name | Type | Description |
|------|------|-------------|
| context | UIAbilityContext | UIAbility context |
| launchWant | Want | Want received during cold start (onCreate) |
| lastRequestWant | Want | Most recent Want (onCreate or onNewWant) |
| callee | Callee | Backend communication object |

## Lifecycle Callbacks

### onCreate
```ts
onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void
```
Triggered when UIAbility is created (cold start only). Sync, no async.

### onWindowStageCreate
```ts
onWindowStageCreate(windowStage: window.WindowStage): void
```
Triggered after WindowStage created. Load page here:
```ts
windowStage.loadContent('pages/Index', (err, data) => { ... });
```

### onForeground
```ts
onForeground(): void
```
Triggered when app comes to foreground. Request resources here. Sync.

### onBackground
```ts
onBackground(): void
```
Triggered when app goes to background. Release resources here. Sync.

### onWindowStageDestroy
```ts
onWindowStageDestroy(): void
```
Triggered after WindowStage destroyed. Release UI resources.

### onDestroy
```ts
onDestroy(): void | Promise<void>
```
Triggered when UIAbility destroyed. Save data, clean up. Supports async.

### onNewWant
```ts
onNewWant(want: Want, launchParam: AbilityConstant.LaunchParam): void
```
Triggered when already-running UIAbility is launched again (hot start).

## Migration Callbacks

### onContinue
```ts
onContinue(wantParam: Record<string, Object>): AbilityConstant.OnContinueResult | Promise<...>
```
Save data before migration. Returns AGREE/REJECT/MISMATCH.

### onWindowStageRestore
```ts
onWindowStageRestore(windowStage: window.WindowStage): void
```
Restore page stack on target device during migration.

## State Callbacks

### onSaveState
```ts
onSaveState(reason: AbilityConstant.StateType, wantParam: Record<string, Object>): AbilityConstant.OnSaveResult
```
Save state for app recovery. Used with appRecovery.

### onBackPressed
```ts
onBackPressed(): boolean
```
Handle back gesture. Return true = move to background, false = destroy.
- targetSdkVersion < 12: default false
- targetSdkVersion >= 12: default true

### onPrepareToTerminate
```ts
onPrepareToTerminate(): boolean
```
Before close (2in1/Tablet only). Return true = cancel close.
Requires: ohos.permission.PREPARE_APP_TERMINATE

---

# Caller/Callee (Backend Communication)

## Caller (Caller UIAbility - system apps only)

Get via `context.startAbilityByCall(want)`.

### call
```ts
call(method: string, data: rpc.Parcelable): Promise<void>
```
Send data to Callee without expecting response.

### callWithResult
```ts
callWithResult(method: string, data: rpc.Parcelable): Promise<rpc.MessageSequence>
```
Send data and receive response from Callee.

### release
```ts
release(): void
```
Release connection with Callee.

### onRelease / on('release')
```ts
onRelease(callback: OnReleaseCallback): void
on(type: 'release', callback: OnReleaseCallback): void
```
Register callback for Callee disconnect.

## Callee (Callee UIAbility)

Access via `this.callee` in UIAbility.

### on
```ts
on(method: string, callback: CalleeCallback): void
```
Register callback for specific method.

### off
```ts
off(method: string): void
```
Unregister callback.

## Parcelable Data Example
```ts
class MyMessageAble implements rpc.Parcelable {
  num: number = 1;
  str: string = '';
  
  marshalling(messageSequence: rpc.MessageSequence) {
    messageSequence.writeInt(this.num);
    messageSequence.writeString(this.str);
    return true;
  }
  
  unmarshalling(messageSequence: rpc.MessageSequence) {
    this.num = messageSequence.readInt();
    this.str = messageSequence.readString();
    return true;
  }
}
```

## Error Codes
| Code | Message |
|------|---------|
| 16200001 | Caller has been released |
| 16200002 | Callee does not exist |
| 16200004 | Method already registered |
| 16200005 | Method not registered |
