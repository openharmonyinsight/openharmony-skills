# 规则F: 版权声明规范

**严重程度**: 中危

**问题描述**: FUZZ测试的所有源文件（`.cpp`、`.h`、`BUILD.gn`、`project.xml`）必须在文件头部包含正确格式的版权声明和许可证声明。版权年份应为编写用例时的实际年份（如 `2026`、`2027` 等），版权归属必须为 `Huawei Device Co., Ltd.`，许可证必须为Apache License 2.0。

**核心原则**:
1. 所有文件必须包含版权声明
2. 版权年份应为实际编写年份
3. 必须使用Apache License 2.0

**错误示例**:
```cpp
/*
 * Copyright (c) 2022 Huawei Device Co., Ltd.   // 错误：年份过旧
 * ...
 */
```

```gn
# Copyright (c) 2022 Huawei Device Co., Ltd.   // 错误：年份过旧
```

**正确示例**:
```cpp
/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * ...
 */
```

```gn
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# ...
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- Copyright (c) 2026 Huawei Device Co., Ltd.
     ...
-->
```

**检查方法**:
1. 检查文件开头是否有版权声明
2. 检查版权年份是否为当前年份或近期年份（不超过2年）
3. 检查版权归属是否为 `Huawei Device Co., Ltd.`
4. 检查是否包含 Apache License 2.0 声明

**豁免场景**: 
- 无

---
