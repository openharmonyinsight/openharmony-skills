# 测试编写规范

## 命名规则

测试用例名称必须与 BUILD.gn 中的 target 名称完全一致。

示例：
1. Target: `LnnNetBuilderFuzzTest`
2. 文件名: `LnnNetBuilderFuzzTest.cpp`
3. 用例类名: `LnnNetBuilderFuzzTest`

## 文件位置

测试文件需放在对应模块的 tests 目录结构下。

```
dsoftus/
├── tests/
│   ├── unit_test/
│   │   └── LnnNetBuilderFuzzTest.cpp
│   └── BUILD.gn
```

## 代码风格

1. **不使用 GoogleTest main 函数** - OpenHarmony 测试框架自带入口
2. **禁止魔鬼数字** - 所有常量必须有命名定义,除了0,1,2都是魔鬼数字
3. **遵循 OpenHarmony 测试风格** - 使用 HWTEST_F 宏
4. 安全函数必须校验返回值
5. 函数不能超过五个参数,代码行不能超过50行
## 测试用例命名后缀

| 序号 | 后缀 | 场景 |
|------|------|------|
| 1 | `_001` | 正常场景 |
| 2 | `_002` | 异常场景 |
| 3 | `_003` | 边界场景 |
| 4 | `_004+` | 其他特殊场景 |
