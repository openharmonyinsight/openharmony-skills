# IPC And External Input Validation

## Expert Checks

Treat `MessageParcel`, remote objects, file descriptors, and network parser output as hostile. The security question is not "is there a read call?" but "can a malformed parcel drive privileged code into a dangerous state before validation fails?"

Check in this order:
1. Every `Read*` operation that reports failure is checked immediately.
2. Values are logically validated after deserialization and before allocation, indexing, looping, path use, or remote call use.
3. Size checks include both lower and upper bounds.
4. `IRemoteObject`, callbacks, death recipients, and fds are validated before storage or use.
5. Parser limits reject malformed input, zip-bomb style expansion, and excessive nesting.

## High-Risk Patterns

```cpp
// VULNERABLE: read failure and bounds are ignored
int32_t size = data.ReadInt32();
std::vector<char> buffer(size);
```

```cpp
// REQUIRED: read success and logical bounds before use
int32_t size = 0;
if (!data.ReadInt32(size)) {
    return ERR_INVALID_DATA;
}
constexpr int32_t MAX_ALLOWED_BUFFER = 1024 * 1024;
if (size < 0 || size > MAX_ALLOWED_BUFFER) {
    return ERR_INVALID_DATA;
}
std::vector<char> buffer(size);
```

## Never Report Without

- Naming the specific attacker-controlled field.
- Showing the sink: allocation, index, loop count, path, fd use, stored remote object, callback, or parser recursion.
- Checking whether a shared validator already covers the field before use.
