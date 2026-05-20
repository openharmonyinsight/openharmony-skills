---
name: xmind
description: Generate and read XMind (.xmind) files via the published xmind-generator-mcp MCP server (npm), with a chat-first UX.
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["mcporter", "npx"]
    install:
      - id: npm
        kind: note
        label: "Uses npx xmind-generator-mcp@0.1.2 (no separate install needed)"
---

# xmind 🧠

Generate and read **XMind** `.xmind` files using the published MCP server `xmind-generator-mcp` (npm).

## When to use
- User wants: "generate an XMind file from this outline / plan / PRD / test plan"
- Output should be a real `.xmind` file that opens in XMind

## Input format (Schema A JSON)
```json
{
  "title": "Root topic",
  "filename": "mindmap-name-no-date",
  "topics": [
    {
      "title": "Topic title",
      "note": "Optional: use sparingly for details",
      "labels": ["optional"],
      "markers": ["Arrow.refresh"],
      "children": [{"title": "Child topic"}]
    }
  ]
}
```

## How to call MCP
### Generate XMind
```bash
mcporter call --stdio "npx -y xmind-generator-mcp@0.1.2" generate-mind-map --args '{...}'
```

### Read XMind
```bash
mcporter call --stdio "npx -y xmind-generator-mcp@0.1.2" read-mind-map --args '{"inputPath":"/path/to/file.xmind","style":"A"}'
```

## Chat-first workflow

**Trigger phrases:** "Generate an XMind for this" / "Make an XMind from this" / "Read this XMind"

**Language rule (important):**
- If user does **not** explicitly specify language, **match the language of the user's request**
- Chinese → Chinese topics; English → English topics

**Filename rule (important):**
- If user provides filename/path → use it
- If not specified → short hyphen style, **no date**, default to `~/Desktop`
- Sanitize invalid chars: `\\ / : * ? \" < > |` → `-`

**Steps:**
1) Parse save location (default `~/Desktop`) and language (match user)
2) Convert content to Schema A JSON
   - Keep reasonably sized
   - `note`: **use sparingly**, only when title is too long
   - `labels`: lightweight categorization
   - `relationships`: sparingly, only for cross-branch links
3) Write JSON to `/tmp/xmind-<ts>.json`
4) Call MCP via mcporter stdio
5) **Send the `.xmind` back in chat as attachment** and tell user disk location

## Template: DT 覆盖设计方案

当用户要求为代码提交生成 DT（Design Test）覆盖设计方案脑图时，使用以下结构：

```json
{
  "title": "DT覆盖设计: <功能名称>",
  "filename": "dt-cover-<功能简称>",
  "topics": [
    {
      "title": "1. 测试对象信息",
      "labels": ["对象"],
      "children": [
        {
          "title": "1.1 背景",
          "children": [
            {"title": "所属模块/文件"},
            {"title": "代码改动量"},
            {"title": "解决痛点/需求来源"},
            {"title": "核心原理/技术方案"}
          ]
        },
        {
          "title": "1.2 测试重点",
          "children": [
            {"title": "核心功能正确性"},
            {"title": "重构一致性"},
            {"title": "接口变更影响"},
            {"title": "边界条件处理"}
          ]
        }
      ]
    },
    {
      "title": "2. 功能测试设计",
      "labels": ["功能"],
      "children": [
        {
          "title": "2.1 基本场景覆盖",
          "children": [
            {"title": "正常功能场景"},
            {"title": "脱糖/转换结构验证"}
          ]
        },
        {
          "title": "2.2 边界场景覆盖",
          "children": [
            {"title": "空/单/多参数组合"},
            {"title": "嵌套/链式调用"},
            {"title": "复合表达式"}
          ]
        },
        {
          "title": "2.3 重构正确性验证",
          "children": [
            {"title": "拆分后逻辑等价性"},
            {"title": "接口变更调用点"}
          ]
        },
        {
          "title": "2.4 框架集成测试",
          "children": [
            {"title": "Mock 模式集成"},
            {"title": "Spy 模式集成"},
            {"title": "模式切换一致性"}
          ]
        },
        {
          "title": "2.5 泛型场景",
          "children": [
            {"title": "泛型实例化场景"},
            {"title": "泛型类型检查"},
            {"title": "泛型类型转换"}
          ]
        },
        {
          "title": "2.6 错误场景",
          "children": [
            {"title": "降级处理"},
            {"title": "不支持类型处理"},
            {"title": "属性过滤"},
            {"title": "防重复处理"}
          ]
        }
      ]
    },
    {
      "title": "3. 性能测试设计",
      "labels": ["性能"],
      "children": [
        {
          "title": "3.1 编译性能",
          "children": [
            {"title": "编译时间增长"},
            {"title": "中间结构克隆开销"},
            {"title": "符号表影响"},
            {"title": "查找算法复杂度"}
          ]
        },
        {
          "title": "3.2 运行时性能",
          "children": [
            {"title": "生成代码调用开销"},
            {"title": "临时变量分配开销"},
            {"title": "节点创建影响"}
          ]
        }
      ]
    },
    {
      "title": "4. FUZZ 测试设计",
      "labels": ["FUZZ"],
      "children": [
        {
          "title": "4.1 输入 FUZZ",
          "children": [
            {"title": "随机生成函数声明"},
            {"title": "随机参数组合"},
            {"title": "随机嵌套深度"},
            {"title": "随机属性标记"}
          ]
        },
        {
          "title": "4.2 过程 FUZZ",
          "children": [
            {"title": "中间状态一致性"},
            {"title": "循环引用检测"},
            {"title": "命名唯一性"},
            {"title": "结构合法性"}
          ]
        },
        {
          "title": "4.3 边界 FUZZ",
          "children": [
            {"title": "极大数量参数"},
            {"title": "极深嵌套层级"},
            {"title": "极端泛型嵌套"}
          ]
        }
      ]
    },
    {
      "title": "5. 不涉及方面及理由",
      "labels": ["排除"],
      "children": [
        {
          "title": "<方面名称>",
          "note": "理由: ..."
        }
      ]
    },
    {
      "title": "6. 测试优先级建议",
      "labels": ["优先级"],
      "children": [
        {"title": "P0: 基本场景 + 边界场景"},
        {"title": "P1: 框架集成 + 特殊场景 + 性能"},
        {"title": "P2: FUZZ 测试"}
      ]
    }
  ]
}
```

## 注意事项
- JSON 中每个 `children` 元素必须有 `title` 字段，否则会报输入验证错误
- 复杂场景应先用 `note` 存放细节说明，而非放入过长的 `title`
- 生成完成后需将 `.xmind` 文件复制到用户期望的位置
