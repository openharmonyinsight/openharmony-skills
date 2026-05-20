---
name: run-cangjie-tests
description: 仓颉测试用例执行技能。
descriptionZH: 仓颉测试用例执行。【触发场景】test
  case/测试用例、testsuite/testlist、HLT/LLT/cjcov/LSP。【注意】依赖 CANGJIE_HOME 环境变量。参数：-j
  并行、--timeout 超时、-pFAIL 只显失败、--retry 重试、--fail_exit 失败退码。
tags:
  - 测试
  - 编译器
  - 仓颉
---

# Run Cangjie Tests

仓颉测试用例执行技能。**每当用户提到以下任何场景时，必须调用此 skill：**
- 「运行测试」「run test」「跑测试用例」「执行测试」
- 「HLT 测试」「LLT 测试」「cjcov 测试」「LSP 测试」
- 「test case」「测试通过了吗」「测试失败」「testsuite」「testlist」
- 「运行 cangjie_test」「执行测试框架」「测试框架」
- 在任何需要运行 `cangjie_test` 仓库中测试用例的场景

**注意：需要先设置 `CANGJIE_HOME` 环境变量。**

## 测试类型

| 类型 | 说明 | 命令特征 |
|------|------|----------|
| HLT | 高层测试（编译+运行） | `cangjie2cjnative_*_test.cfg` |
| LLT | 低层测试（单元测试） | `cjnative_test.cfg` |
| cjcov | 覆盖率测试 | `cjcov/configs/test.cfg` |
| LSP | 语言服务器测试 | `cjlsp/` |

## 常用命令

```bash
# 运行单个 HLT 测试
python3 cangjie_test_framework/main.py \
  --test_cfg=cangjie_test/testsuites/HLT/configs/cjnative/cangjie2cjnative_linux_x86_test.cfg \
  --verbose \
  cangjie_test/testsuites/HLT/compiler/cjnative/Chir/ForIn/for_in_01.cj

# 运行所有 HLT 测试
python3 cangjie_test_framework/main.py \
  --test_cfg=cangjie_test/testsuites/HLT/configs/cjnative/cangjie2cjnative_linux_x86_test.cfg \
  --test_list=cangjie_test/testsuites/HLT/testlist \
  -pFAIL -j20 --timeout=180 \
  cangjie_test/testsuites/HLT/

# 运行所有 LLT 测试
python3 cangjie_test_framework/main.py \
  --test_cfg=cangjie_test/testsuites/LLT/configs/cjnative/cjnative_test.cfg \
  --test_list=cangjie_test/testsuites/LLT/cjnative_testlist,cangjie-ci/scripts/cangjie/ci/test/llt/linux/x64/exclude_cjnative_testlist \
  --fail_exit -pFAIL --retry=3 --debug \
  --fail-verbose -j20 --timeout=180 \
  cangjie_test/testsuites/LLT/
```

## 关键参数

- `-j <num>` - 并行测试数
- `--timeout <秒>` - 单个测试超时
- `-pFAIL` - 仅显示失败测试
- `--retry <num>` - 失败重试次数
- `--fail_exit` - 有失败则退出码非零
- `--debug` - 保留失败测试临时文件
