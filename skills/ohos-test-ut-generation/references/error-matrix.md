# 错误排查矩阵（症状→原因→修复）

---

## 一、编译错误矩阵

### BUILD.gn配置类

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

## 三、门禁拒绝类（OpenHarmony特有）

| 症状 | 原因 | 修复 | 验证 |
|------|------|------|------|
| 门禁无法识别测试 | 使用GTest原生TEST()宏 | 改用HWTEST或HWTEST_F | 门禁识别成功 |
| 门禁拒绝：缺少等级参数 | HWTEST宏未指定Level | 添加 `TestSize.Level1` | 门禁通过 |
| 门禁拒绝：命名空间缺失 | 缺少 `using namespace testing::ext;` | 文件头添加声明 | HWTEST宏可用 |

---

## 四、常见错误排查流程

### 编译失败排查步骤

```
1. 检查BUILD.gn第一行是否有import("//build/test.gni")
2. 检查deps是否包含gtest_main
3. 检查sources是否包含所有测试文件
4. 检查include_dirs是否完整
5. 检查external_deps是否包含跨子系统依赖
6. 检查cflags_cc是否配置（测试私有成员时）
```

### 链接失败排查步骤

```
1. 检查gtest_main是否在deps中
2. 检查被测模块是否在deps中
3. 检查Mock cpp文件是否在sources中
4. 检查external_deps是否包含gmock（使用Mock时）
```

### 运行失败排查步骤

```
1. 检查SetUp是否初始化所有测试对象
2. 检查TearDown是否释放所有资源
3. 检查测试目录是否存在（SetUpTestCase创建）
4. 检查依赖服务是否启动（如hilog）
5. 检查是否有硬编码路径
```

---

## 五、错误预防检查清单

**编译前检查**：
- [ ] BUILD.gn第一行：`import("//build/test.gni")`
- [ ] deps包含：`//third_party/googletest:gtest_main`
- [ ] sources包含所有测试文件
- [ ] 测试私有成员：cflags_cc配置

**运行前检查**：
- [ ] SetUp初始化所有测试对象
- [ ] TearDown释放所有资源
- [ ] 无硬编码绝对路径
- [ ] 测试目录已创建

---

## 相关文档

- [build-rules.md](build-rules.md) - BUILD.gn配置规则
- [framework-quickref.md](framework-quickref.md) - 测试框架速查表
- [test-case-spec.md](test-case-spec.md) - 测试文件结构