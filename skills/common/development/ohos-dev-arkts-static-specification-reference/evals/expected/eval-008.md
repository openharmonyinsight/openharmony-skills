# Expected Output: eval-008

## Key Points (必须包含)

1. 不能只按“最窄类型优先”的直觉判断。ArkTS overload resolution 受 overload set 顺序影响。
2. 如果 `number` 版本排在 `int` 版本前，`int` 实参可能先匹配到 `number` 版本，导致后面的 `int` 版本被遮蔽。
3. 后续重载如果永远不可达，应产生 warning 或等价诊断。
4. 建议把更窄、更精确的签名放在更宽签名前，或显式调整 overload list 顺序。
5. 依据：`spec/semantics.md` — overload / method call resolution 相关章节。

## Anti-Pattern (不得出现)

- “一定优先匹配 int” — 错误
- “重载顺序不影响结果” — 错误
- 未引用 `spec/semantics.md`
