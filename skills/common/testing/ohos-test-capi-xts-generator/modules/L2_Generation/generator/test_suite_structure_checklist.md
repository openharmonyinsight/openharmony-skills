# CAPI 测试套工程结构完整检查清单

> **版本**: 1.1.0  
> **创建日期**: 2026-03-19  
> **更新日期**: 2026-03-19  
> **用途**: 确保新生成的 CAPI 测试套工程结构完整且正确
---
## 必需文件清单（强制）

> ⚠️ **警告**：创建新工程时，必须确保以下所有文件都存在，否则编译会失败！

**推荐方式**：复制整个模板工程，而不是从零生成

**模板工程位置**：`.opencode/skills/oh-capi-xts-gen/template_project/capi_test_template/`

## 一级必需文件（缺失会导致编译失败）

### 测试套编译配置

- [ ] `BUILD.gn` - ⭐ 测试套编译配置（必需）
- [ ] `Test.json` - ⭐ Hypium 测试配置（必需）
- [ ] `build-profile.json5` - 项目构建配置
- [ ] `oh-package.json5` - 项目包配置
- [ ] `hvigorfile.ts` - Hvigor 构建脚本（根目录）
- [ ] `hvigor/hvigor-config.json5` - Hvigor 配置文件
- [ ] `.gitignore` - Git 忽略配置（推荐）

### AppScope 应用级配置

- [ ] `AppScope/app.json5` - ⭐ 应用配置（bundleName、版本等）
- [ ] `AppScope/resources/base/element/string.json` - 应用级字符串资源
- [ ] `AppScope/resources/base/media/app_icon.png` 或分层图标
  - 分层图标：`background.png` + `foreground.png` + `layered_image.json`

### 签名文件

- [ ] `signature/openharmony.p7b` - 签名证书文件

---

## 二级必需文件（缺失会导致编译或运行时错误）

### Entry 模块配置

- [ ] `entry/build-profile.json5` - 模块构建配置
- [ ] `entry/oh-package.json5` - 模块包配置
- [ ] `entry/hvigorfile.ts` - 模块 Hvigor 脚本
- [ ] `entry/.gitignore` - Git 忽略配置（推荐）

### C++ 代码和配置

- [ ] `entry/src/main/cpp/NapiTest.cpp` - ⭐ N-API 封装实现
- [ ] `entry/src/main/cpp/CMakeLists.txt` - ⭐ CMake 构建配置
- [ ] `entry/src/main/cpp/types/libentry/index.d.ts` - ⭐ TypeScript 类型声明
- [ ] `entry/src/main/cpp/types/libentry/oh-package.json5` - 类型包配置

### ETS 代码和配置

- [ ] `entry/src/main/ets/entryability/EntryAbility.ts` - ⚠️ **注意后缀是 .ts，不是 .ets**
- [ ] `entry/src/main/ets/pages/Index.ets` - 主页面
- [ ] `entry/src/main/module.json5` - ⭐ main 模块配置
- [ ] `entry/src/main/syscap.json` - ⭐ 系统能力配置

### Main 模块资源

- [ ] `entry/src/main/resources/base/element/color.json` - 颜色资源
- [ ] `entry/src/main/resources/base/element/string.json` - 字符串资源
- [ ] `entry/src/main/resources/base/profile/main_pages.json` - 页面配置
- [ ] `entry/src/main/resources/base/media/icon.png` - 图标资源

---

## 三级必需文件（缺失会导致测试无法运行）

### OhosTest 测试模块

- [ ] `entry/src/ohosTest/ets/test/List.test.ets` - ⭐ 测试套注册文件（必需）
- [ ] `entry/src/ohosTest/ets/test/*.test.ets` - 实际测试用例文件
- [ ] `entry/src/ohosTest/ets/testability/TestAbility.ets` - 测试 Ability 实现
- [ ] `entry/src/ohosTest/ets/testability/pages/Index.ets` - 测试 Ability 页面
- [ ] `entry/src/ohosTest/ets/testrunner/OpenHarmonyTestRunner.ts` - 测试运行器
- [ ] `entry/src/ohosTest/module.json5` - ⭐ ohosTest 模块配置
- [ ] `entry/src/ohosTest/syscap.json` - ⭐ 测试模块系统能力配置

### OhosTest 资源

- [ ] `entry/src/ohosTest/resources/base/element/color.json` - 颜色资源
- [ ] `entry/src/ohosTest/resources/base/element/string.json` - 字符串资源
- [ ] `entry/src/ohosTest/resources/base/profile/test_pages.json` - 测试页面配置
- [ ] `entry/src/ohosTest/resources/base/media/icon.png` - 图标资源

---

## ⚠️ 常见错误

### 1. EntryAbility 文件后缀错误

❌ **错误**：`EntryAbility.ets`  
✅ **正确**：`EntryAbility.ts`

### 2. 签名文件名错误

❌ **错误**：`openharmony_sx.p7b`  
✅ **正确**：`openharmony.p7b`

### 3. 缺少 syscap.json

⚠️ `entry/src/main/syscap.json` 和 `entry/src/ohosTest/syscap.json` 都是必需的

### 4. 缺少 List.test.ets

⚠️ `entry/src/ohosTest/ets/test/List.test.ets` 是测试套注册文件，必须存在

---

## 📋 文件统计

- **一级必需文件**：10 个
- **二级必需文件**：14 个
- **三级必需文件**：11 个
- **总计**：35+ 个必需文件

---

## 🔧 推荐操作

### 创建新工程（推荐）

```bash
# 1. 复制模板工程
cp -r .opencode/skills/oh-capi-xts-gen/template_project/capi_test_template \
  ${OH_ROOT}/test/xts/acts/${SUBSYSTEM}/${TEST_SUITE_NAME}

# 2. 验证文件完整性
bash .opencode/skills/oh-capi-xts-gen/scripts/check_test_suite_structure.sh \
  ${OH_ROOT}/test/xts/acts/${SUBSYSTEM}/${TEST_SUITE_NAME}
```

### 验证已有工程

```bash
# 检查必需文件是否完整
bash .opencode/skills/oh-capi-xts-gen/scripts/check_test_suite_structure.sh \
  ${测试套路径}
```

---

**版本**: 1.0.0  
**创建日期**: 2026-03-25  
**更新日期**: 2026-03-25
