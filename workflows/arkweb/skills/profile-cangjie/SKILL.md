---
name: profile-cangjie
description: 仓颉编译器性能分析技能。
descriptionZH: 仓颉编译器性能分析。【触发场景】profile-compile-time、profile-compile-memory、.prof
  报告、编译瓶颈。【注意】需先构建 compiler，直接用 --profile 标志无需重编译。
tags:
  - 性能分析
  - 编译器
  - 仓颉
---

# Profile Cangjie Compiler

仓颉编译器性能分析技能。**每当用户提到以下任何场景时，必须调用此 skill：**
- 「profile」「性能分析」「分析编译时间」「内存分析」
- 「编译性能」「profile-compile-time」「profile-compile-memory」
- 「compilation time」「memory usage」「查看 .prof 文件」
- 「分析编译瓶颈」「哪个阶段最慢」「编译速度慢」
- 在任何需要测量和分析编译器编译性能和内存占用的场景

**注意：compiler 必须先构建完成才能 profile，无需修改源码或重新编译。**

## 快速开始

```bash
# 同时 profile 时间和内存
python3 skills/profile-cangjie/scripts/profile-cangjie.py test.cj --both

# 仅 profile 内存
python3 skills/profile-cangjie/scripts/profile-cangjie.py test.cj --memory

# 仅 profile 时间
python3 skills/profile-cangjie/scripts/profile-cangjie.py test.cj --time

# 分析已有的 .prof 文件
python3 skills/profile-cangjie/scripts/profile-cangjie.py --analyze test.cj.mem.prof
```

## 手动使用

```bash
source output/envsetup.sh

# Profile 编译时间
cjc --profile-compile-time test.cj -o test
cat test.cj.time.prof

# Profile 内存
cjc --profile-compile-memory test.cj -o test
cat test.cj.mem.prof
```
