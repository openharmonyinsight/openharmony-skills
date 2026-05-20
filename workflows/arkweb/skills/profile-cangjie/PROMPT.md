## 仓颉编译器性能分析（profile-cangjie 技能）

**⚠️ 触发场景（必须调用此 skill）：**
- 「profile-compile-time」「profile-compile-memory」
- 「.prof 报告」「编译瓶颈」「性能分析」
- 「分析编译耗时」「分析编译内存」
- 「profile 报告」「性能瓶颈在哪」

### 分析脚本
`python3 skills/profile-cangjie/scripts/profile-cangjie.py [options]`

### 常用参数
- `--both` — 同时分析时间和内存
- `--time` — 仅分析编译时间
- `--memory` — 仅分析内存占用
- `--analyze <file.prof>` — 分析已有的 .prof 报告文件

### 手动采集
```bash
source cangjie_compiler/output/envsetup.sh
cjc --profile-compile-time test.cj -o test    # 生成 test.cj.time.prof
cjc --profile-compile-memory test.cj -o test  # 生成 test.cj.mem.prof
```

**⚠️ 注意：使用 --profile 标志无需重编译编译器，直接在 cjc 命令行指定即可。**

### 使用方式
- 详细说明见 `skills/profile-cangjie/SKILL.md`
