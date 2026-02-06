# Linux 编译问题排查指南

> **模块信息**
> - 层级：L2_Analysis
> - 优先级：按需加载（编译失败时加载）
> - 适用范围：Linux 环境下的 XTS 测试工程编译
> - 平台：Linux
> - 依赖：无
> - 相关：`build_workflow_linux.md`（完整的编译工作流）

> **使用说明**
>
> 本指南提供编译问题的诊断和解决方案。
>
> 用户遇到编译错误时，加载此模块进行排查。

---

## 一、问题诊断流程

### 1.1 诊断步骤

```
1. 查看编译日志
   ├─ 定位错误信息
   └─ 识别错误类型

2. 对照常见错误
   ├─ 匹配错误现象
   └─ 查找解决方案

3. 应用解决方案
   ├─ 执行解决步骤
   └─ 验证解决效果

4. 如果问题持续
   ├─ 清理缓存
   └─ 重新编译
```

### 1.2 日志位置

```
out/{product_name}/suites/acts/acts/
├── build.log              # 编译总日志
├── {suite_name}/          # 测试套目录
│   └── build.log          # 测试套编译日志
└── testcases/             # 编译产物
```

---

## 二、常见错误

### 2.1 编译失败：BUILD FAILED

**现象**：
```
BUILD FAILED
error: build script exited with status 1
```

**可能原因**：
1. 代码语法错误
2. 依赖缺失
3. 配置文件错误

**解决方案**：

步骤1：查看详细错误日志
```bash
cat out/rk3568/suites/acts/acts/build.log | grep -A 5 "ERROR"
```

步骤2：根据错误信息定位问题
- 如果是语法错误，修改代码
- 如果是依赖错误，检查 BUILD.gn 中的 deps
- 如果是配置错误，检查配置文件

步骤3：清理后重新编译
```bash
# 清理编译产物
rm -rf out/rk3568/suites/acts/

# 重新编译
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTest
```

### 2.2 依赖错误

**现象**：
```
error: dependency 'xxx' not found
```

**可能原因**：
1. 依赖模块不存在
2. 依赖模块名称拼写错误
3. 依赖模块未编译

**解决方案**：

步骤1：检查 BUILD.gn 中的 deps 配置
```bash
# 查看当前测试套的 BUILD.gn
cat test/xts/acts/testfwk/<test_suite_name>/BUILD.gn | grep -A 10 "deps"
```

步骤2：确认依赖模块存在
```bash
# 查找依赖模块
find . -name "BUILD.gn" -exec grep -l "ohos_js_app_suite.*ModuleName" {} \;
```

步骤3：检查依赖模块名称拼写
```gni
# 确保名称一致
deps = [
  ":ActsUiTestEntry",  # 正确
  # ":ActsUiTestEntr",  # 错误：拼写错误
]
```

### 2.3 证书错误

**现象**：
```
error: certificate not found: ./signature/*.p7b
```

**可能原因**：
1. 证书文件不存在
2. 证书路径配置错误
3. 证书文件损坏

**解决方案**：

步骤1：检查证书文件是否存在
```bash
ls -la ./signature/*.p7b
```

步骤2：检查 BUILD.gn 中的证书路径
```gni
certificate_profile = "./signature/auto_ohos_default_com.uitest.test.p7b"
```

步骤3：如果证书不存在，使用默认证书
```bash
# 复制默认证书
cp /path/to/default.p7b ./signature/
```

### 2.4 Node.js 版本错误

**现象**：
```
error: Node version too old
```

**可能原因**：
1. Node.js 版本过低
2. npm 版本不匹配

**解决方案**：

步骤1：检查当前版本
```bash
node --version
npm --version
```

步骤2：更新 Node.js
```bash
# 使用 nvm 安装新版本
nvm install 16
nvm use 16

# 或使用包管理器
apt install nodejs npm
```

步骤3：验证版本
```bash
node --version  # 应该 >= 14.x
npm --version   # 应该 >= 6.x
```

### 2.5 权限错误

**现象**：
```
error: permission denied
```

**可能原因**：
1. 目录权限不足
2. 文件被其他进程占用

**解决方案**：

步骤1：检查目录权限
```bash
ls -la /path/to/directory
```

步骤2：修改权限（谨慎使用）
```bash
chmod -R 755 /path/to/directory
```

步骤3：检查文件占用
```bash
lsof | grep <filename>
```

### 2.6 磁盘空间不足

**现象**：
```
error: no space left on device
```

**解决方案**：

步骤1：检查磁盘空间
```bash
df -h
```

步骤2：清理不必要的文件
```bash
# 清理编译产物
rm -rf out/

# 清理系统缓存
sudo apt clean
```

步骤3：扩展磁盘空间（如果需要）

---

## 三、编译优化

### 3.1 增量编译

只编译修改的部分，加快编译速度：

```bash
# 不清理产物，直接编译
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTest
```

**适用场景**：
- 仅修改了少量测试代码
- 确认没有影响编译产物的修改

### 3.2 并行编译

利用多核 CPU 加速编译（默认启用）：

```bash
# 查看并行数
cat out/rk3568/build.ninja | grep "pool"
```

### 3.3 缓存管理

清理缓存解决编译问题：

```bash
# 清理编译产物
rm -rf out/rk3568/suites/acts/

# 清理 ninja 缓存
rm -rf out/rk3568/.ninja*

# 重新编译
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTest
```

---

## 四、日志分析

### 4.1 关键日志位置

```
out/{product_name}/suites/acts/acts/
├── build.log              # 编译总日志
├── {suite_name}/          # 测试套目录
│   └── build.log          # 测试套编译日志
└── testcases/             # 编译产物
```

### 4.2 日志过滤命令

```bash
# 查看错误日志
grep -i "error" build.log

# 查看警告日志
grep -i "warn" build.log

# 查看特定模块日志
grep "ActsUiTest" build.log

# 实时监控编译日志
tail -f build.log

# 查看最近 50 行错误
grep -i "error" build.log | tail -50

# 查看错误上下文（前后 5 行）
grep -A 5 -B 5 "error" build.log
```

### 4.3 日志分析技巧

**技巧1：按错误类型统计**
```bash
grep -i "error" build.log | sort | uniq -c | sort -nr
```

**技巧2：定位首次错误**
```bash
grep -n "error" build.log | head -1
```

**技巧3：导出错误日志**
```bash
grep -i "error" build.log > errors.txt
```

---

## 五、问题排查检查清单

### 5.1 编译前检查

- [ ] 环境准备完成（Node.js、npm、Python、Git）
- [ ] 已执行预编译清理
- [ ] BUILD.gn 配置正确
- [ ] 证书文件存在
- [ ] 磁盘空间充足

### 5.2 编译中检查

- [ ] 在 OH_ROOT 目录下执行编译命令
- [ ] 使用 `build.sh` 脚本（不使用 `hvigorw`）
- [ ] 编译参数正确（`product_name`、`system_size`、`suite`）
- [ ] 查看编译日志，确认无错误

### 5.3 编译后检查

- [ ] HAP 包生成成功
- [ ] HAP 包时间戳为最新
- [ ] 测试用例已更新

---

## 六、高级排查

### 6.1 启用详细日志

```bash
# 启用详细编译日志
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTest --verbose
```

### 6.2 检查 GN 配置

```bash
# 验证 GN 语法
gn check out/rk3568 //test/xts/acts/testfwk/<test_suite_name>:BUILD.gn
```

### 6.3 查看编译依赖

```bash
# 查看依赖图
gn desc out/rk3568 //test/xts/acts/testfwk/<test_suite_name>:ActsUiTest deps
```

### 6.4 调试编译脚本

```bash
# 查看 build.sh 内容
cat test/xts/acts/build.sh

# 使用 bash 调试模式
bash -x test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTest
```

---

## 七、获取帮助

### 7.1 社区资源

- [OpenHarmony 文档](https://docs.openharmony.cn/)
- [OpenHarmony 社区](https://www.openharmony.cn/)
- [XTS 测试规范](https://gitee.com/openharmony/test_xts)

### 7.2 提问指南

提问时请提供：
1. 完整的错误日志
2. BUILD.gn 配置
3. 编译命令
4. 环境信息（OS、Node.js 版本等）

---

## 八、版本历史

- **v1.0.0** (2026-02-06): 从 `build_workflow_linux.md` 中抽取编译问题排查相关内容，创建独立模块
