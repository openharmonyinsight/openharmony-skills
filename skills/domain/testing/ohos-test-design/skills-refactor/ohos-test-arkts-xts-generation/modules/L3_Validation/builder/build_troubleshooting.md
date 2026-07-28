# Linux 编译问题排查

> **模块信息**
> - 层级：L3_Validation
> - 按需加载：编译失败时参考

---

## 一、自动错误处理（v1.16.0+）

subagent 执行编译时的自动错误处理流程：

**语法错误（自动修复）**：
```
编译失败 → 分析错误日志 → 定位文件/行号 → 识别错误类型 → 修改源代码 → 重新编译（最多 3 次）
```

**配置错误（需确认）**：
```
检测到配置问题 → 说明问题和方案 → 向用户确认 → 用户同意后修改并重试
```

---

## 二、常见错误速查

### 2.1 BUILD FAILED

```bash
# 查看错误详情
grep -i "error" out/rk3568/suites/acts/acts/build.log

# 查看错误上下文
grep -A 5 -B 5 "error" out/rk3568/suites/acts/acts/build.log | head -50
```

### 2.2 依赖错误

```bash
# 检查 BUILD.gn 中依赖配置
cat {测试套目录}/BUILD.gn | grep -A 10 "deps"
```

### 2.3 证书错误

```bash
# 检查证书文件
ls -la ./signature/*.p7b

# 使用默认证书
cp /path/to/default.p7b ./signature/
```

### 2.4 Node.js 版本

```bash
node --version  # 需要 >= 14.x
nvm install 16 && nvm use 16
```

### 2.5 权限错误

```bash
# 检查目录权限
ls -la /path/to/directory

# 检查文件占用
lsof | grep <filename>
```

### 2.6 磁盘空间

```bash
df -h
rm -rf out/  # 清理编译产物
```

### 2.7 静态编译专用错误

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| SDK 找不到 | 首次编译未清理 prebuilts | `rm -rf prebuilts/ohos-sdk/linux` 后重新编译 |
| hap_static 参数无效 | BUILD.gn 目标类型错误 | 确认使用 `ohos_js_app_static_suite()` |
| hvigor 版本错误 | 未替换静态编译工具 | 执行版本校验和替换（见 build_workflow_linux.md 第三章） |
| 编译超时 | SDK 编译耗时过长 | 增加超时时间，使用异步编译 |

---

## 三、日志分析

### 3.1 日志位置

```
out/{product_name}/suites/acts/acts/
├── build.log              # 编译总日志
├── {suite_name}/          # 测试套编译日志
└── testcases/             # 编译产物
```

### 3.2 异步编译日志

异步编译时日志位于 `/tmp/oh_xts_build/`：

```bash
# 查看异步编译错误
{skill_root}/scripts/async_build.sh {OH_ROOT} {suite} rk3568 errors

# 查看完整日志
{skill_root}/scripts/async_build.sh {OH_ROOT} {suite} rk3568 logs
```

### 3.3 常用过滤命令

```bash
# 按错误类型统计
grep -i "error" build.log | sort | uniq -c | sort -nr

# 定位首次错误
grep -n "error" build.log | head -1

# 导出错误日志
grep -i "error" build.log > errors.txt
```

---

**版本**: 2.0.0
**更新日期**: 2026-04-01
