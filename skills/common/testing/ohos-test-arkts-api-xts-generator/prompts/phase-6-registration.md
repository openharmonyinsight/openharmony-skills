## Phase 6: Register Test Suites

### 条件

仅当新增了测试文件时需要执行此阶段。

### 步骤

使用 `register_test.py` 脚本自动注册：

```bash
python {skill_root}/scripts/register_test.py \
  --list-file {测试套目录}/List.test.ets \
  --new-file {测试套目录}/{NewModule}.test.ets
```

脚本自动完成：
- 按字母顺序插入 import 语句（字母序确保多个开发者并行添加测试时不产生合并冲突，且保证文件内容确定性）
- 在 `testsuite()` 函数中插入调用

如需预览（不写入文件）：
```bash
python {skill_root}/scripts/register_test.py \
  --list-file {测试套目录}/List.test.ets \
  --new-file {测试套目录}/{NewModule}.test.ets \
  --dry-run
```

### 注意

- 如果 `List.test.ets` 不存在，跳过此阶段
- 不要修改 `List.test.ets` 中已有的内容
