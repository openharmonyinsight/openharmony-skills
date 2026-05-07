# Linux CAPI 编译工作流

> **模块信息**
> - 层级：L3_Validation
> - 优先级：按需加载
> - 适用范围：Linux 环境下的 OpenHarmony CAPI XTS 测试工程编译
> - 平台： Linux

## ⚠️ 重要提示（Linux 环境 CAPI）

**在 Linux 环境下编译 OpenHarmony CAPI XTS 测试工程，必须使用 `./test/xts/acts/build.sh` 脚本进行编译。**

- ✅ **正确方式**： 使用 `./test/xts/acts/build.sh` 脚本
- ❌ **错误方式**: 不要使用 `hvigorw`、`./build.sh --product-name` 等命令

**原因**:
1. `./test/xts/acts/build.sh` 是 OpenHarmony XTS 测试工程的专用编译脚本
2. `./test/xts/acts/build.sh` 会正确处理测试套依赖关系和编译配置
3. `hvigorw` 是 Windows/DevEco Studio 的编译工具，不适用于 Linux 环境
4. `./build.sh --product-name` 是 OpenHarmony 系统编译命令，不适用于测试套编译
5. 使用错误的命令可能导致编译失败或生成的 HAP 包不正确

## 编译命令格式

```bash
# 正确的编译命令
cd {OH_ROOT}
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=<测试套名称>

# 示例：编译 ActsZlibCapiTest
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsZlibCapiTest
```

### 参数说明

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `product_name` | 产品名称 | `rk3568` | `rk3568`, `Hi3516DV300` |
| `system_size` | 系统大小 | `standard` | `standard`, `small`, `large` |
| `suite` | 测试套名称 | (必需) | `ActsZlibCapiTest` |

### 测试套名称获取

从测试套的 `BUILD.gn` 文件中提取测试套名称：

```bash
# 方法1：查看 BUILD.gn 文件
cat test/xts/acts/bundlemanager/zlib/actszlibcapiapitest/BUILD.gn | grep "ohos_js_app_suite"

# 方法2：使用 grep 查找
grep -E "ohos_js_app_(static_)?suite" test/xts/acts/bundlemanager/zlib/actszlibcapiapitest/BUILD.gn
```

示例 BUILD.gn 内容：
```gn
ohos_js_app_suite("ActsZlibCapiTest") {
  test_hap = true
  testonly = true
  hap_name = "ActsZlibCapiTest"
  ...
}
```

从上面提取的测试套名称为：`ActsZlibCapiTest`

## 编译流程

### 步骤 1: 准备编译环境

```bash
# 进入 OpenHarmony 根目录
cd /path/to/openharmony

# 确认编译脚本存在
ls -l test/xts/acts/build.sh

# 确认测试套目录存在
ls -d test/xts/acts/bundlemanager/zlib/actszlibcapiapitest
```

### 步骤 2: 执行编译

```bash
# 执行编译
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsZlibCapiTest

# 编译过程会显示：
# [OHOS INFO] GN Done
# [OHOS INFO] NINJA Excuting ninja command...
# [OHOS INFO] build success
```

### 步骤 3: 验证编译产物

```bash
# 查找生成的 HAP 包
find out/rk3568 -name "*ActsZlibCapiTest*.hap" 2>/dev/null

# 查看 HAP 包详细信息
ls -lh out/rk3568/suites/acts/acts/testcases/ActsZlibCapiTest.hap
```

### 步骤 4: 检查 HAP 包内容（可选）

```bash
# 解压 HAP 包查看内容
unzip -l out/rk3568/suites/acts/acts/testcases/ActsZlibCapiTest.hap | head -20

# 检查 HAP 包大小
du -h out/rk3568/suites/acts/acts/testcases/ActsZlibCapiTest.hap
```

## 编译成功标志

### 成功日志特征

```
[OHOS INFO] Done. Made XXXXX targets from XXXX files in XXXXXms
[OHOS INFO] build success: ActsZlibCapiTest
[OHOS INFO] build time: XXs
```

### 编译产物验证

```bash
# 检查 HAP 包是否存在
if [ -f "out/rk3568/suites/acts/acts/testcases/ActsZlibCapiTest.hap" ]; then
    echo "✅ 编译成功：HAP 包已生成"
    ls -lh out/rk3568/suites/acts/acts/testcases/ActsZlibCapiTest.hap
else
    echo "❌ 编译失败：HAP 包未生成"
fi
```

## 编译失败处理

### 常见错误类型

| 错误类型 | 错误信息 | 解决方案 |
|---------|---------|---------|
| **测试套未找到** | `ninja: error: unknown target 'ActsZlibCapiTest'` | 检查测试套名称是否正确 |
| **BUILD.gn 错误** | `GN Error: ...` | 检查 BUILD.gn 文件语法 |
| **依赖缺失** | `error: 'xxx.h' file not found` | 检查头文件路径和依赖配置 |
| **编译脚本错误** | `./test/xts/acts/build.sh: No such file or directory` | 确认在正确的目录下执行 |

### 错误排查步骤

1. **确认测试套名称正确**
   ```bash
   # 查看 BUILD.gn 中的测试套名称
   grep "ohos_js_app_suite" test/xts/acts/bundlemanager/zlib/actszlibcapiapitest/BUILD.gn
   ```

2. **确认在 OpenHarmony 根目录**
   ```bash
   # 确认当前目录
   pwd
   # 应该显示：/path/to/openharmony
   
   # 确认编译脚本存在
   ls test/xts/acts/build.sh
   ```

3. **检查 BUILD.gn 配置**
   ```bash
   # 查看 BUILD.gn 内容
   cat test/xts/acts/bundlemanager/zlib/actszlibcapiapitest/BUILD.gn
   ```

4. **查看详细错误日志**
   ```bash
   # 查看编译日志
   cat out/rk3568/build.log | tail -100
   
   # 查看错误日志
   cat out/rk3568/error.log
   ```

## 错误修复示例

### 错误 1: 测试套名称不正确

```bash
# 错误命令
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=actszlibcapiapitest

# 错误信息
ninja: error: unknown target 'actszlibcapiapitest'

# 正确命令（从 BUILD.gn 中提取的正确名称）
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsZlibCapiTest
```

### 错误 2: 使用了错误的编译命令

```bash
# ❌ 错误命令 1：使用系统 build.sh
./build.sh --product-name rk3568 --build-target ActsZlibCapiTest

# ❌ 错误命令 2：使用 hvigorw
cd test/xts/acts/bundlemanager/zlib/actszlibcapiapitest
hvigorw assembleHap

# ✅ 正确命令
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsZlibCapiTest
```

### 错误 3: 不在正确的目录

```bash
# ❌ 错误：在测试套目录下执行
cd test/xts/acts/bundlemanager/zlib/actszlibcapiapitest
../../build.sh product_name=rk3568 system_size=standard suite=ActsZlibCapiTest

# ✅ 正确：在 OpenHarmony 根目录执行
cd /path/to/openharmony
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsZlibCapiTest
```

## 高级用法

### 编译多个测试套

```bash
# 编译多个测试套
for suite in ActsZlibCapiTest ActsZlibCapiTest2 ActsZlibCapiTest3; do
    echo "编译测试套: $suite"
    ./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=$suite
done
```

### 清理编译产物

```bash
# 清理指定测试套的编译产物
rm -rf out/rk3568/suites/acts/acts/testcases/ActsZlibCapiTest*

# 清理所有编译产物（谨慎使用）
rm -rf out/rk3568
```

### 查看编译配置

```bash
# 查看 GN 配置
gn args out/rk3568 --list

# 查看当前编译参数
gn args out/rk3568
```

## 编译最佳实践

1. **始终在 OpenHarmony 根目录下执行编译命令**
2. **使用正确的编译脚本**: `./test/xts/acts/build.sh`
3. **从 BUILD.gn 文件中提取正确的测试套名称**
4. **编译前确认测试套目录和 BUILD.gn 文件存在**
5. **编译后验证 HAP 包是否正确生成**
6. **遇到错误时，先查看错误日志再进行修复**
7. **不要混用不同的编译命令和工具**

## 总结

**编译 OpenHarmony CAPI XTS 测试套的正确流程**:

```bash
# 1. 进入 OpenHarmony 根目录
cd /path/to/openharmony

# 2. 确认测试套存在
ls test/xts/acts/bundlemanager/zlib/actszlibcapiapitest/BUILD.gn

# 3. 提取测试套名称
grep "ohos_js_app_suite" test/xts/acts/bundlemanager/zlib/actszlibcapiapitest/BUILD.gn

# 4. 执行编译
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsZlibCapiTest

# 5. 验证编译产物
ls -lh out/rk3568/suites/acts/acts/testcases/ActsZlibCapiTest.hap
```

---

**版本**: 2.0.0
**创建日期**: 2026-03-19
**更新日期**: 2026-03-19
**重要变更**: 明确使用 `./test/xts/acts/build.sh` 作为唯一正确的编译命令
