# modules

三层架构 + 跨层共享规范层。

```
conventions/        跨层共享：CAPI 测试框架规范
L1_Analysis/        解析头文件：.h 解析、覆盖率分析、文档读取、工程配置解析
L2_Generation/      生成测试产物：N-API 封装、ETS 测试、工程配置、三重校验
L3_Validation/      验证产物质量：编译构建、环境配置
```

数据流：`用户输入(.h) → L1_Analysis → L2_Generation → L3_Validation → 编译产物(.hap)`
