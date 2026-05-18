# 错误排查矩阵（症状→修复）

---

## 一、编译错误矩阵

### BUILD.gn 配置类

| 症状 | 原因 | 修复 | 验证 |
|------|------|------|------|
| `template 'ohos_unittest' not found` | 缺少 `import("//build/test.gni")` | BUILD.gn第一行添加import | GN解析成功 |
| `fatal error: xxx.h: No such file` | include_dirs缺失 | 在config块添加include_dirs | 编译无错误 |
| `undefined reference to xxx` | deps/external_deps缺失 | 添加gtest_main和被测模块到deps | 链接成功 |
| `undefined reference to main` | 缺少gtest_main | deps添加 `//third_party/googletest:gtest_main` | 测试可运行 |
| `'xxx' is private within this context` | 访问private成员 | 添加 `cflags_cc = ["-Dprivate=public"]` | 可访问private |
| `cannot use 'dynamic_cast' with -fno-rtti` | RTTI禁用 | config添加 `cflags = ["-frtti"]` | dynamic_cast可用 |
| `multiple definition of xxx` | 同一源文件被多处包含 | 使用 `sources +=` 复用变量 | 链接成功 |
| `no input files` | sources遗漏测试文件 | sources包含所有*_test.cpp | 编译成功 |

### 测试代码类

| 症状 | 原因 | 修复 | 验证 |
|------|------|------|------|
| `'HWTEST_F' was not declared` | 缺少命名空间声明 | 文件头添加 `using namespace testing::ext;` | HWTEST可用 |
| `'MOCK_METHOD' was not declared` | 缺少gmock依赖/头文件 | external_deps添加 `"googletest:gmock"`，include `<gmock/gmock.h>` | MOCK_METHOD可用 |
| `'ON_CALL' was not declared` | 缺少命名空间 | 添加 `using namespace testing;` | gmock宏可用 |

---

## 二、运行错误矩阵

| 症状 | 原因 | 修复 | 验证 |
|------|------|------|------|
| `Segmentation fault` | SetUp未初始化对象 | SetUp中 `detector_ = new BBoxDetector()` | 测试稳定运行 |
| `Segmentation fault` | 使用已delete对象 | TearDown中reset智能指针 | 无崩溃 |
| `Segmentation fault` | 数组越界 | 添加 `ASSERT_LT(index, array.size())` | 无崩溃 |
| `SetUp failed` 所有用例失败 | 测试目录不存在 | SetUpTestCase创建目录 | SetUp成功 |
| `SetUp failed` 所有用例失败 | 平台服务未启动 | 检查hilog等依赖服务 | SetUp成功 |
| `Timeout` | 异步回调未返回 | 添加超时控制逻辑 | 测试在规定时间完成 |
| `Timeout` | SetUp/TearDown阻塞 | 优化耗时操作 | 连续运行稳定通过 |
| `Failed to load config file` | resource_config_file缺失 | 配置ohos_test.xml路径 | 资源正常加载 |
| `Invalid test level` | HWTEST缺少等级参数 | 添加 `TestSize.Level1` | 门禁识别正确 |

---

## 三、Anti-Patterns 禁止事项速查

### 编译配置类（NEVER）

| ❌ 禁止操作 | 原因 | ✅ 正确做法 |
|------------|------|------------|
| 省略 `import("//build/test.gni")` | template not found | BUILD.gn第一行import |
| module_out_path使用GN路径 | 路径解析错误 | 用 `"hiviewdfx/hiview_test"` 格式 |
| 省略gtest_main依赖 | undefined reference to main | deps必须包含 |
| 访问private时忘记cflags_cc | is private错误 | 添加 `-Dprivate=public` |
| 直接在ohos_unittest写include_dirs | 不符合规范 | 使用config()块管理 |

### 测试代码类（NEVER）

| ❌ 禁止操作 | 原因 | ✅ 正确做法 |
|------------|------|------------|
| 省略 `using namespace testing::ext;` | HWTEST未声明 | 文件头必须包含 |
| 使用GTest原生 `TEST()` | 门禁无法识别 | 使用 `HWTEST(A, B, TestSize.Level1)` |
| HWTEST缺少等级参数 | 门禁拒绝 | 必须指定Level1-4 |
| SetUp忘记初始化对象 | SEGFAULT | `detector_ = new BBoxDetector()` |
| 省略@tc.type注释 | 测试报告异常 | 每个HWTEST_F前添加注释块 |
| EXPECT_*做前置检查 | 可能空指针崩溃 | 前置检查用ASSERT_* |

### 运行阶段类（NEVER）

| ❌ 禁止操作 | 原因 | ✅ 正确做法 |
|------------|------|------------|
| SetUpTestCase创建临时对象 | 状态污染 | SetUpTestCase仅初始化共享资源 |
| TearDown忘记清理 | 内存泄漏 | delete/reset所有SetUp创建的对象 |
| 硬编码路径 | 不同设备路径不存在 | 使用resource_config_file |

---

## 四、BUILD.gn 配置检查清单

| 检查项 | 配置项 | 必填性 | 正确示例 |
|--------|--------|--------|----------|
| Import语句 | `import("//build/test.gni")` | **必填** | BUILD.gn第一行 |
| 输出路径 | `module_out_path` | **必填** | `"hiviewdfx/hiview_test"` |
| 源文件 | `sources` | **必填** | `["unittest/bbox_test.cpp"]` |
| 头文件目录 | `include_dirs`（config块中） | **必填** | `["//base/xxx/include"]` |
| 内部依赖 | `deps` | **必填** | `["//third_party/googletest:gtest_main"]` |
| 外部依赖 | `external_deps` | 按需 | `["hilog:libhilog"]` |
| 访问控制 | `cflags_cc` | 按需 | `["-Dprivate=public"]` |
| 编译宏 | `defines` | 按需 | `["UNIT_TEST"]` |

---

## 五、错误排查流程

```
测试失败
  ↓
检查日志（GTEST_LOG_）
  ↓
┌─ 编译错误 ──────────────────────┐
│  检查BUILD.gn:                  │
│    - import语句                 │
│    - include_dirs（config块）   │
│    - deps/external_deps         │
│    - cflags_cc（private访问）   │
│  检查测试代码:                   │
│    - using namespace testing::ext│
│    - HWTEST宏格式+等级参数       │
└─────────────────────────────────┘
  ↓
┌─ 运行错误 ──────────────────────┐
│  Segmentation fault → SetUp初始化│
│  Timeout → 异步操作+超时控制     │
│  SetUp failed → 目录/权限/服务   │
│  资源找不到 → resource_config_file│
└─────────────────────────────────┘
  ↓
定位修复 → 重新编译验证
```

---

## 六、提交前10项必查

1. `import("//build/test.gni")` - BUILD.gn第一行
2. `using namespace testing::ext;` - 测试文件头部
3. `//third_party/googletest:gtest_main` - deps必加
4. SetUp初始化对象 - 防止段错误
5. TearDown清理资源 - 防止内存泄漏
6. 使用HWTEST而非TEST() - 门禁要求
7. TestSize.Level参数 - HWTEST必填
8. @tc注释块 - 每个HWTEST_F前必加
9. config()块管理include_dirs - 符合规范
10. module_out_path用子系统/模块格式 - 不是GN路径

---

## 相关文档

- [build-gn-config.md](build-gn-config.md) - BUILD.gn完整配置
- [assertion-gmock-guide.md](assertion-gmock-guide.md) - 断言与gmock配置
