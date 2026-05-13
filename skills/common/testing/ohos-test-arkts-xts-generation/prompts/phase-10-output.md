## Phase 10: Output Results

---

### 📦 MANDATORY - 必须先加载以下模块

本 Phase 仅输出结果，不需要加载任何模块。

---

### ⚙️ 按需加载

本 Phase 不需要额外加载模块。

---

### 🚫 Do NOT Load - 禁止加载

本 Phase 期间禁止加载以下模块：

```
所有模块（仅输出结果）
```

---

### 输出内容

1. **更新文件列表**: 所有新建和修改的文件路径
2. **测试设计文档**: 所有生成的 `.design.md` 文件
3. **覆盖率对比**（Flow B 必有，Flow A 可选）:
   - 生成前覆盖率
   - 生成后预期覆盖率
   - 新增覆盖的 API/参数/错误码数量

### 输出格式

```
## 生成结果

### 文件清单
- {path}/{TestFile1}.test.ets ({lines} 行, {N} 个测试用例)
- {path}/{TestFile2}.test.ets ({lines} 行, {N} 个测试用例)

### 测试设计文档
- {path}/{TestFile1}.test.design.md
- {path}/{TestFile2}.test.design.md

### 覆盖率变化
| 指标 | 生成前 | 生成后 | 新增 |
|------|--------|--------|------|
| 方法覆盖 | X/Y | X+M/Y | +M |
| 参数场景覆盖 | A/B | A+N/B | +N |
| 错误码覆盖 | P/Q | P+R/Q | +R |
```
