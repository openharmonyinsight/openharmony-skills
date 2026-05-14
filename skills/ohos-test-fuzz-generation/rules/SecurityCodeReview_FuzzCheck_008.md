# 规则008: 种子合理构造

**严重程度**: 中危

**问题描述**: 种子的初始形态应与被测 API 预期的输入格式高度相关。如果种子与目标格式差异过大，fuzz 引擎需要极多轮变异才能产生有效输入，导致前期大量执行被简单的前置校验拦截，效率极低。被测 API 可能处理的输入类型包括：媒体文件（JPEG、PNG、WebP、MP4）、3D/图形资源（gltf/glb、obj）、结构化数据（JSON、XML、protobuf）、网络/通信数据（HTTP 请求、IPC MessageParcel）、其他二进制格式（压缩包、证书）。

**核心原则**:
1. 种子格式应与被测API期望的输入格式匹配
2. corpus目录必须存在且包含有效种子
3. 合理的初始种子能显著提高fuzz效率

**错误示例**:
```
❌ corpus/init 是纯文本，但测试的是 JPEG 解码
❌ corpus/init 是空文件，但测试的是字体解析
❌ corpus/init 是随机二进制，但测试的是 gltf/JSON 加载
❌ corpus/init 是固定值（如全0），无法提供有效的初始变异基础
```

**正确示例**:
```
✅ 测试图片解码：
corpus/
├── init.jpg      # 仅保留 JPEG SOI + APP0 头的最小合法文件（~20 字节）
├── init_small.jpg # 更小的变体
└── init_large.jpg # 更大的变体

✅ 测试序列化解析：
corpus/
├── init.bin      # 包含 Magic(4B) + Version(2B) + 空 payload 的最小包
├── init_v1.bin   # 版本1变体
└── init_v2.bin   # 版本2变体

✅ 测试 JSON 解析：
corpus/
├── init.json     # {"type":"user","data":{}}
├── init_array.json # ["item1", "item2"]
└── init_nested.json # {"a":{"b":{"c":1}}}

✅ 测试字体解析：
corpus/
├── init.ttf      # 仅保留 sfnt version + numTables + 一个空表目录项

✅ 测试 gltf 加载：
corpus/
├── init.gltf     # 最小合法 JSON，含 scene / node / mesh 骨架
└── init.bin      # 对应的二进制 buffer（若有）
```

**检查方法**: 
1. 分析被测 API 的输入格式要求
2. 检查 `corpus/` 目录是否存在
3. 检查 `corpus/` 中是否放置了与目标格式匹配的种子文件
4. 检查种子文件是否为空或明显不符合格式要求
5. 确保 fuzz 引擎能从合理的初始状态开始变异

**豁免场景**: 
- 简单参数类型的API（如纯数值参数）无需种子文件

---
