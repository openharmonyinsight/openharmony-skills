# MarkdownParser - Markdown 解析器

## 概述

MarkdownParser 负责解析 AI 维护的 Markdown 描述文件，提取概念描述、同义词、相关术语等信息。这些描述文件存储在 `knowledge-base/descriptions/` 目录下，由 AI 助手创建和维护。

## 功能

### 核心功能

1. **解析单个 Markdown 文件** (`parse_description_file`)
   - 解析 YAML front matter（元数据）
   - 提取概念名称（一级标题）
   - 提取中英文描述
   - 提取使用场景列表
   - 提取实现说明

2. **加载所有描述文件** (`load_all_descriptions`)
   - 遍历 descriptions/ 目录
   - 解析所有 .md 文件
   - 返回关键词到描述条目的映射

3. **格式验证** (`validate_format`)
   - 验证必需字段是否存在
   - 检查 YAML front matter 格式
   - 确保至少有一种语言的描述

## Markdown 文件格式

### 标准格式

```markdown
---
keyword: <关键词>
synonyms: [同义词1, 同义词2, ...]
related: [相关概念1, 相关概念2, ...]
category: <类别>
---

# <概念名称>

## 中文描述
<详细的中文描述>

## English Description
<详细的英文描述>

## 使用场景
- 场景1
- 场景2
- ...

## 相关实现
<实现细节说明>
```

### 必需字段

1. **YAML front matter 中的 `keyword`**: 主关键词，用于索引
2. **一级标题 `# <概念名称>`**: 概念的显示名称
3. **至少一种语言的描述**: `## 中文描述` 或 `## English Description`

### 可选字段

- `synonyms`: 同义词列表（YAML 数组格式）
- `related`: 相关概念列表（YAML 数组格式）
- `category`: 概念类别（如 language-feature, module, algorithm）
- `## 使用场景`: 使用场景列表（Markdown 列表格式）
- `## 相关实现`: 实现细节说明

## 使用示例

### 解析单个文件

```python
from markdown_parser import MarkdownParser

parser = MarkdownParser()
entry = parser.parse_description_file('knowledge-base/descriptions/lambda.md')

if entry:
    print(f"关键词: {entry.keyword}")
    print(f"概念名称: {entry.concept_name}")
    print(f"同义词: {entry.synonyms}")
    print(f"中文描述: {entry.description_zh}")
```

### 加载所有描述文件

```python
from markdown_parser import MarkdownParser

parser = MarkdownParser()
descriptions = parser.load_all_descriptions('knowledge-base/descriptions')

for keyword, entry in descriptions.items():
    print(f"{keyword}: {entry.concept_name}")
```

### 验证格式

```python
from markdown_parser import MarkdownParser

parser = MarkdownParser()

with open('test.md', 'r', encoding='utf-8') as f:
    content = f.read()

if parser.validate_format(content):
    print("格式有效")
else:
    print("格式无效")
```

## 数据结构

### DescriptionEntry

```python
@dataclass
class DescriptionEntry:
    keyword: str                    # 主关键词
    synonyms: List[str]             # 同义词列表
    related: List[str]              # 相关概念列表
    category: Optional[str]         # 类别
    concept_name: str               # 概念名称
    description_zh: Optional[str]   # 中文描述
    description_en: Optional[str]   # 英文描述
    use_cases: List[str]            # 使用场景
    implementation_notes: Optional[str]  # 实现说明
    file_path: str                  # 文件路径
```

## 错误处理

解析器会处理以下错误情况：

1. **缺少 YAML front matter**: 警告并返回 None
2. **缺少必需字段**: 警告并返回 None
3. **缺少概念名称**: 警告并返回 None
4. **缺少描述**: 警告并返回 None
5. **文件读取错误**: 打印错误信息并返回 None

所有错误都会输出清晰的警告信息，但不会中断整个加载过程。

## 测试

运行测试套件：

```bash
python3 test_markdown_parser.py
```

测试覆盖：
- 解析有效文件
- 只有中文描述
- 只有英文描述
- 缺少必需字段
- 格式验证
- 加载目录下所有文件
- 空列表处理

## 与其他组件的集成

MarkdownParser 的输出会被 SearchIndexBuilder 使用：

1. **generate_knowledge.py** 调用 `load_all_descriptions()` 加载所有描述
2. **SearchIndexBuilder** 调用 `merge_descriptions()` 将描述合并到搜索索引
3. 描述中的同义词会被添加到搜索索引，支持同义词搜索
4. 描述中的相关概念会被用于建立概念之间的关联

## 示例文件

参考 `knowledge-base/descriptions/lambda.md` 查看完整的示例文件。

## 注意事项

1. **编码**: 所有文件必须使用 UTF-8 编码
2. **YAML 格式**: front matter 使用简化的 YAML 解析，只支持基本的键值对和数组
3. **列表格式**: 使用场景必须使用 Markdown 列表格式（`-` 或 `*` 开头）
4. **章节标题**: 章节标题必须使用二级标题 `##`
5. **概念名称**: 必须使用一级标题 `#`

## 未来扩展

可能的扩展功能：

1. 支持更复杂的 YAML 格式（嵌套对象、多行字符串）
2. 支持更多章节类型（示例代码、常见问题等）
3. 支持 Markdown 内部链接验证
4. 支持自动生成描述模板
5. 支持描述版本控制和历史记录
