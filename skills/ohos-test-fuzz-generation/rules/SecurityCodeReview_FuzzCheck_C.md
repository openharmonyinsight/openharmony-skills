# 规则C: project.xml格式规范

**严重程度**: 中危

**问题描述**: FUZZ测试的project.xml配置文件必须使用正确的XML格式（以`<?xml version="1.0" encoding="utf-8"?>`开头）、版权声明、根元素`<fuzz_config>`、`<fuzztest>`子元素以及`max_len`、`max_total_time`、`rss_limit_mb`配置项。格式不规范会导致fuzz引擎无法正确读取配置参数。

**核心原则**:
1. 必须以正确的XML声明开头
2. 根元素必须是<fuzz_config>
3. 必须包含max_len、max_total_time、rss_limit_mb

**错误示例**:
```xml
<!-- ❌ 缺少XML声明和必要配置 -->
<config>
    <max_len>1000</max_len>
</config>
```

**正确示例**:
```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- Copyright ... -->
<fuzz_config>
    <fuzztest>
        <max_len>1000</max_len>
        <max_total_time>300</max_total_time>
        <rss_limit_mb>4096</rss_limit_mb>
    </fuzztest>
</fuzz_config>
```

**检查方法**:
1. 检查文件开头是否有正确的XML声明
2. 检查是否包含版权声明
3. 检查根元素是否为 `<fuzz_config>`
4. 检查是否包含 `<fuzztest>` 子元素
5. 检查是否包含 `max_len`、`max_total_time`、`rss_limit_mb` 配置项

**豁免场景**: 
- 无

---
