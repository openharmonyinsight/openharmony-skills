# hb-build 使用示例

实际使用场景和最佳实践示例。

## 目录

- [基础示例](#基础示例)
- [常见场景](#常见场景)
- [高级用法](#高级用法)
- [实际案例](#实际案例)
- [故障排除示例](#故障排除示例)

---

## 基础示例

### 示例 1: 自动检测并编译

**场景**: 修改了 UriPermissionManager 的代码，需要编译

```bash
# 1. 修改代码
vim services/uripermmgr/src/libupms/batch_uri.cpp

# 2. 自动检测并编译
python3 scripts/helper.py

# 输出:
# ============================================================
# Ability Runtime 自动编译工具
# ============================================================
#
# [INFO] 检测到 2 个修改的文件:
#   - services/uripermmgr/src/libupms/batch_uri.cpp
#   - services/uripermmgr/include/batch_uri.h
#
# [INFO] 编译目标: libupms
# [INFO] 完整路径: //foundation/ability/ability_runtime/services/uripermmgr:libupms
# [INFO] 编译类型: -i
# [INFO] 最大重试: 3 次
#
# [INFO] 执行编译命令（第 1 次，最多 3 次）
# [INFO] 命令: hb build ability_runtime -i --build-target //foundation/ability/ability_runtime/services/uripermmgr:libupms
# ...
# [SUCCESS] 编译成功！
```

### 示例 2: 编译特定服务

**场景**: 只编译 AbilityManagerService

```bash
# 方法 1: 使用短名称
python3 scripts/helper.py --target abilityms

# 方法 2: 使用完整路径
python3 scripts/helper.py --target //foundation/ability/ability_runtime/services/abilitymgr:abilityms
```

### 示例 3: 快速编译

**场景**: 频繁修改代码，需要快速迭代

```bash
# 启用快速编译模式
python3 scripts/helper.py --target libupms --fast

# 输出命令会包含 --fast-rebuild
# hb build ability_runtime -i --build-target ... --fast-rebuild
```

---

## 常见场景

### 场景 1: 修改多个服务

**场景**: 同时修改了 UriPermissionManager 和 AbilityManagerService

```bash
# 1. 查看修改的文件
git status --short

# 输出:
# M  services/uripermmgr/src/libupms/file_permission_manager.cpp
# M  services/abilitymgr/src/ability_manager/ability_manager_service.cpp

# 2. 运行 hb-build
python3 scripts/helper.py

# 输出:
# [INFO] 检测到 2 个修改的文件:
#   - services/uripermmgr/src/libupms/file_permission_manager.cpp
#   - services/abilitymgr/src/ability_manager/ability_manager_service.cpp
#
# [INFO] 检测到 2 个编译目标，将一起编译
# [INFO] 编译目标 (2 个):
#   1. libupms
#   2. abilityms
#
# [INFO] 执行编译命令...
```

**说明**: 脚本会自动将所有修改的服务一起编译，提高效率。

### 场景 2: 编译失败后重试

**场景**: 编译出现语法错误，需要修复后重试

```bash
# 1. 首次编译（失败）
python3 scripts/helper.py --target libupms

# 输出:
# [ERROR] 编译失败（返回码: 1）
# [ERROR] 发现 3 个编译错误
# [WARNING] 原因: 发现需要手动修复的错误: syntax error
# [WARNING]
# 还有 2 次重试机会
# [INFO] 您可以：
#   1. 手动修复代码后，按 Enter 继续重试
#   2. 输入 'r' 开启自动重试模式
#   3. 输入 'q' 或 'quit' 退出
#
# 您的选择 [Enter/r/q]:

# 2. 在另一个终端修复错误
vim services/uripermmgr/src/libupms/batch_uri.cpp
# 修复第 123 行的语法错误

# 3. 回到原终端，按 Enter 继续重试
# 脚本会自动重新编译

# 4. 如果继续失败，再次提示重试
# 最多重试 3 次
```

### 场景 3: 启用自动重试

**场景**: 编译偶尔失败，希望自动重试

```bash
# 启用自动重试模式
python3 scripts/helper.py --auto-retry --target libupms

# 输出（如果编译失败）:
# [ERROR] 编译失败（返回码: 1）
# [WARNING] ✓ 发现可重试的错误: ninja: error: rebuilding
# [WARNING] ⚠ 自动重试中... (2 次剩余)
# [INFO] 执行编译命令（第 2 次，最多 3 次）
# ...
# [SUCCESS] 编译成功！
```

**说明**: 启用 `--auto-retry` 后，脚本会自动判断是否可以重试。对于构建系统临时问题会自动重试，对于语法错误等需要手动修复的问题则提示用户。

### 场景 3: 编译测试套

**场景**: 修改了测试代码，需要编译测试套

```bash
# 编译全仓测试套
python3 scripts/helper.py --target full --type -t

# 或编译特定服务的测试
python3 scripts/helper.py --target abilityms --type -t
```

### 场景 4: 全仓编译

**场景 1: 需要编译整个 ability_runtime 组件**

```bash
# 方法 1: 明确指定 full
python3 scripts/helper.py --target full

# 方法 2: 让脚本自动检测（当无法确定目标时）
python3 scripts/helper.py --target auto
```

**场景 2: 自动触发整仓编译（目标数量 > 5）**

```bash
# 修改了多个服务（假设修改了 6 个服务）
git status --short

# 输出:
# M  services/uripermmgr/src/libupms/file_permission_manager.cpp
# M  services/abilitymgr/src/ability_manager/ability_manager_service.cpp
# M  services/appmgr/src/app_manager/app_manager_service.cpp
# M  services/dataobsmgr/src/data_observer_manager/data_observer_manager.cpp
# M  services/quickfixmgr/src/quick_fix_manager/quick_fix_manager.cpp
# M  frameworks/native/ability/src/ability_context.cpp

# 运行 hb-build
python3 scripts/helper.py

# 输出:
# [INFO] 检测到 6 个修改的文件:
#   ...
# [WARNING] 检测到 6 个编译目标，超过 5 个
# [WARNING] 建议使用整仓编译以节省时间
# [INFO] 编译目标: full (全仓编译)
```

**注意**: 全仓编译耗时较长（10-30 分钟），建议在以下情况使用：
- 首次编译
- 修改了跨服务的公共接口
- 清理后重新编译
- 修改了多个服务（> 5 个）

---

## 高级用法

### 示例 1: 自定义重试次数

**场景**: 期望有更多重试机会

```bash
# 设置最多 5 次重试
python3 scripts/helper.py --target libupms --max-retries 5
```

### 示例 2: 组合参数

**场景**: 快速编译 + 自定义重试 + 特定目标

```bash
python3 scripts/helper.py --target abilityms --fast --max-retries 2
```

### 示例 3: 在脚本中使用

**场景**: 在自动化脚本中集成 hb-build

```bash
#!/bin/bash
# build_and_test.sh - 自动编译并测试

echo "开始编译..."

# 编译修改的代码
if python3 .claude/skills/hb-build/scripts/helper.py; then
    echo "✅ 编译成功"

    # 运行测试
    echo "运行测试..."
    ./run_tests.sh
else
    echo "❌ 编译失败"
    exit 1
fi
```

### 示例 4: 批量编译多个服务

**场景**: 需要编译多个相关的服务

```bash
#!/bin/bash
# batch_build.sh - 批量编译服务

services=("libupms" "abilityms" "appms")

for service in "${services[@]}"; do
    echo "编译 $service..."

    if python3 .claude/skills/hb-build/scripts/helper.py --target "$service"; then
        echo "✅ $service 编译成功"
    else
        echo "❌ $service 编译失败，停止批量编译"
        exit 1
    fi
done

echo "✅ 所有服务编译完成"
```

---

## 实际案例

### 案例 1: 修复 URI 权限 Bug

**背景**: 用户报告 URI 权限验证有漏洞

```bash
# 1. 定位问题
vim services/uripermmgr/src/libupms/uri_permission_manager_stub_impl.cpp
# 修改第 234 行的权限检查逻辑

# 2. 自动编译
python3 scripts/helper.py

# 输出:
# [INFO] 检测到 1 个修改的文件:
#   - services/uripermmgr/src/libupms/uri_permission_manager_stub_impl.cpp
#
# [INFO] 编译目标: libupms
# [SUCCESS] 编译成功！

# 3. 验证修复
adb push out/standard/ability/ability_runtime/libupms.z.so /system/lib64/
adb reboot
```

### 案例 2: 添加新的 Ability 类型

**背景**: 需要添加一个新的 Ability 扩展类型

```bash
# 1. 修改接口定义
vim interfaces/inner_api/ability_manager/include/iability_manager_collaborator.h
# 添加新的接口方法

# 2. 实现接口
vim services/abilitymgr/src/ability_manager/ability_manager_collaborator_proxy.cpp
# 实现新的业务逻辑

# 3. 编译（会自动检测到两个文件修改）
python3 scripts/helper.py

# 输出:
# [INFO] 检测到 2 个修改的文件:
#   - interfaces/inner_api/ability_manager/include/iability_manager_collaborator.h
#   - services/abilitymgr/src/ability_manager/ability_manager_collaborator_proxy.cpp
#
# [INFO] 编译目标: abilityms
# [INFO] 编译类型: -i
#
# [INFO] 执行编译命令（第 1 次，最多 3 次）
# [SUCCESS] 编译成功！
```

### 案例 3: 性能优化和快速迭代

**背景**: 优化 UriPermissionManager 性能，需要频繁修改和测试

```bash
# 1. 创建别名
alias hbupms='python3 .claude/skills/hb-build/scripts/helper.py --target libupms --fast'

# 2. 修改代码
vim services/uripermmgr/src/libupms/file_permission_manager.cpp

# 3. 快速编译
hbupms

# 4. 测试
./test_uri_permission.sh

# 5. 重复 2-4 步，直到完成优化
```

---

## 故障排除示例

### 示例 1: 处理路径错误

**问题**: 在错误的目录运行脚本

```bash
# 错误示例 - 在非 ability_runtime 目录
cd foundation/ability
python3 ../ability_runtime/.claude/skills/hb-build/scripts/helper.py

# 输出:
# [WARNING] 未检测到修改的文件
# [WARNING] 无法确定编译目标，将编译全仓

# 正确方法 - 在 ability_runtime 目录
cd foundation/ability/ability_runtime  # 或已在 ability_runtime 目录
python3 .claude/skills/hb-build/scripts/helper.py
```

### 示例 2: 处理编译错误

**问题**: 编译出现 undefined reference 错误

```bash
# 1. 运行编译
python3 scripts/helper.py --target libupms

# 2. 查看错误信息
# 输出:
# [ERROR] 编译失败（返回码: 1）
# [ERROR] 发现 1 个编译错误
#   - services/uripermmgr/src/libupms/uri_permission_manager_service.cpp:234:10: error: undefined reference to 'SomeFunction'

# 3. 分析问题
# 缺少某个函数的定义或链接

# 4. 修复代码
vim services/uripermmgr/src/libupms/uri_permission_manager_service.cpp
# 添加缺失的头文件或实现

# 5. 按 Enter 重试（在编译终端）
# 或重新运行
python3 scripts/helper.py --target libupms
```

### 示例 3: 处理依赖问题

**问题**: 编译时缺少依赖库

```bash
# 1. 运行编译
python3 scripts/helper.py --target libupms

# 2. 查看错误
# [OHOS ERROR] ninja: error: unknown dependency: libsome_library.z.so

# 3. 检查依赖
grep -r "libsome_library" .  # 在当前 ability_runtime 目录搜索

# 4. 先编译依赖
python3 scripts/helper.py --target full  # 编译全仓以确保依赖完整

# 5. 重新编译目标
python3 scripts/helper.py --target libupms
```

---

### 综合示例: 多服务修改 + 自动重试

**场景**: 修改了多个服务，启用自动重试

```bash
# 1. 修改多个服务的代码
vim services/uripermmgr/src/libupms/batch_uri.cpp
vim services/abilitymgr/src/ability_manager/ability_manager_service.cpp
vim services/appmgr/src/app_manager/app_manager_service.cpp

# 2. 启用自动重试并编译
python3 scripts/helper.py --auto-retry

# 输出:
# ============================================================
# Ability Runtime 自动编译工具
# ============================================================
#
# [INFO] 检测到 3 个修改的文件:
#   - services/uripermmgr/src/libupms/batch_uri.cpp
#   - services/abilitymgr/src/ability_manager/ability_manager_service.cpp
#   - services/appmgr/src/app_manager/app_manager_service.cpp
#
# [INFO] 检测到 3 个编译目标，将一起编译
# [INFO] 编译目标 (3 个):
#   1. libupms
#   2. abilityms
#   3. appms
#
# [INFO] 编译类型: -i
# [INFO] 自动重试: 开启
# [INFO] 最大重试: 3 次
#
# [INFO] 执行编译命令（第 1 次，最多 3 次）
# [INFO] 命令: hb build ability_runtime -i --build-target ... --build-target ... --build-target ...
# [INFO] 工作目录: /home/duansizhao/oh
# ...编译输出...
# [SUCCESS] 编译成功！
#
# ============================================================
# 编译完成！
# ============================================================
#
# [INFO] 编译产物目录: /home/duansizhao/oh/out
```

---

## 最佳实践

### 1. 优先使用自动检测模式

```bash
# 推荐：让脚本自动检测并编译
python3 scripts/helper.py

# 脚本会智能决定：
# - 单个目标 → 编译单个目标
# - 多个目标（≤ 5）→ 一起编译多个目标
# - 多个目标（> 5）→ 使用整仓编译
```

### 2. 修改代码前检查状态

```bash
# 查看当前修改
git status

# 确认要修改的文件
git diff services/uripermmgr/
```

### 3. 小步快跑，频繁编译

```bash
# 修改一个文件 → 编译 → 测试
vim services/uripermmgr/src/libupms/batch_uri.cpp
python3 scripts/helper.py --target libupms --fast
./test_batch_uri.sh
```

### 4. 启用自动重试处理临时问题

```bash
# 对于偶尔出现的编译问题，启用自动重试
python3 scripts/helper.py --auto-retry

# 或创建别名
alias hbbuild='python3 .claude/skills/hb-build/scripts/helper.py --auto-retry'
hbbuild
```

### 5. 使用快速编译模式

```bash
# 开发阶段使用 --fast
python3 scripts/helper.py --target libupms --fast

# 最终编译不加 --fast，确保完整编译
python3 scripts/helper.py --target libupms
```

### 6. 保存编译日志

```bash
# 重定向输出到日志文件
python3 scripts/helper.py --target libupms 2>&1 | tee build_$(date +%Y%m%d_%H%M%S).log
```

### 7. 集成到工作流

```bash
# 在 Makefile 中集成
.PHONY: build
build:
	@echo "编译修改的代码..."
	@python3 .claude/skills/hb-build/scripts/helper.py

.PHONY: test
test: build
	@echo "运行测试..."
	@./run_tests.sh
```

---

## 相关资源

- [详细文档](reference.md) - API 参考和技术细节
- [主文档](SKILL.md) - 概述和快速入门
- [执行脚本](scripts/helper.py) - 核心实现
