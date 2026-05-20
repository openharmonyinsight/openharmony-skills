# SearchIndexBuilder - 搜索索引构建器

## 概述

SearchIndexBuilder 是知识库系统的核心组件，负责构建从关键词到代码元素的倒排索引。它整合了 KeywordExtractor、MarkdownParser 和 ModuleAnalyzer 的输出，生成可搜索的知识库索引。

## 主要功能

1. **倒排索引构建**: 从代码元素（类、函数、模块）提取关键词，构建关键词到代码位置的映射
2. **描述合并**: 将 AI 维护的 Markdown 描述合并到索引中
3. **同义词索引**: 为同义词创建索引条目，指向主关键词
4. **TF-IDF 权重计算**: 计算关键词的重要性权重，用于搜索结果排序
5. **JSON 序列化**: 将索引转换为 JSON 格式，便于存储和加载

## 核心类

### SearchIndex

搜索索引容器，存储所有关键词到索引条目的映射。

```python
class SearchIndex:
    def __init__(self):
        self.keywords: Dict[str, IndexEntry] = {}
    
    def add_entry(self, keyword: str, entry: IndexEntry):
        """添加索引条目"""
    
    def get_entry(self, keyword: str) -> IndexEntry:
        """获取索引条目"""
    
    def to_dict(self) -> Dict:
        """转换为字典格式（用于 JSON 序列化）"""
```

### IndexEntry

索引条目，包含关键词的所有相关信息。

```python
@dataclass
class IndexEntry:
    keyword: str                          # 关键词
    description: str                      # 中文描述
    description_en: str                   # 英文描述
    synonyms: List[str]                   # 同义词列表
    related: List[str]                    # 相关概念列表
    modules: List[str]                    # 相关模块列表
    classes: List[CodeLocation]           # 相关类列表
    functions: List[CodeLocation]         # 相关函数列表
    tfidf_score: float                    # TF-IDF 权重
```

### CodeLocation

代码位置信息。

```python
@dataclass
class CodeLocation:
    name: str    # 名称（类名或函数名）
    file: str    # 文件路径
    line: int    # 行号
```

### SearchIndexBuilder

搜索索引构建器，负责构建和维护索引。

```python
class SearchIndexBuilder:
    def build_index(self, module_tree: ModuleTree, 
                   descriptions: Dict[str, DescriptionEntry] = None) -> SearchIndex:
        """构建搜索索引"""
    
    def merge_descriptions(self, index: SearchIndex, 
                          descriptions: Dict[str, DescriptionEntry]) -> SearchIndex:
        """合并 Markdown 描述到索引"""
    
    def add_entry(self, keyword: str, entry: IndexEntry):
        """添加索引条目"""
```

## 使用示例

### 基本用法

```python
from search_index_builder import SearchIndexBuilder
from module_analyzer import ModuleTree
from markdown_parser import MarkdownParser

# 1. 构建模块树（从 ModuleAnalyzer 获取）
module_tree = ModuleTree()
# ... 添加模块 ...

# 2. 加载 Markdown 描述（可选）
parser = MarkdownParser()
descriptions = parser.load_all_descriptions("knowledge-base/descriptions/")

# 3. 构建索引
builder = SearchIndexBuilder()
index = builder.build_index(module_tree, descriptions)

# 4. 导出为 JSON
import json
index_dict = index.to_dict()
with open("search-index.json", "w", encoding="utf-8") as f:
    json.dump(index_dict, f, ensure_ascii=False, indent=2)
```

### 查询索引

```python
# 获取关键词的索引条目
lambda_entry = index.get_entry("lambda")

if lambda_entry:
    print(f"描述: {lambda_entry.description}")
    print(f"相关模块: {lambda_entry.modules}")
    print(f"相关类: {[cls.name for cls in lambda_entry.classes]}")
    print(f"相关函数: {[func.name for func in lambda_entry.functions]}")
```

### 添加自定义条目

```python
from search_index_builder import IndexEntry, CodeLocation

# 创建自定义条目
entry = IndexEntry(
    keyword="custom_feature",
    description="自定义特性描述",
    modules=["module1"],
    classes=[CodeLocation(name="CustomClass", file="custom.h", line=10)],
    functions=[CodeLocation(name="customFunc", file="custom.cpp", line=100)]
)

# 添加到索引
builder.add_entry("custom_feature", entry)
```

## 工作流程

### 1. 构建倒排索引

```
ModuleTree
    ↓
遍历所有模块
    ↓
提取关键词（使用 KeywordExtractor）
    ↓
构建映射：
  - keyword → modules
  - keyword → classes
  - keyword → functions
```

### 2. 创建索引条目

```
对每个关键词：
    ↓
创建 IndexEntry
    ↓
添加相关模块、类、函数
```

### 3. 合并 Markdown 描述

```
加载 Markdown 描述
    ↓
对每个描述：
    ↓
查找或创建索引条目
    ↓
合并描述、同义词、相关概念
    ↓
为同义词创建索引条目
```

### 4. 计算 TF-IDF 权重

```
统计总文档数（类 + 函数）
    ↓
对每个关键词：
    ↓
计算文档频率（包含该关键词的文档数）
    ↓
计算 IDF = log(总文档数 / 文档频率)
    ↓
计算 TF = 文档频率 / 总文档数
    ↓
TF-IDF = TF * IDF
```

## 输出格式

生成的 JSON 索引格式：

```json
{
  "keywords": {
    "lambda": {
      "description": "Lambda 表达式是仓颉语言中的匿名函数特性",
      "description_en": "Lambda expressions are anonymous function features",
      "synonyms": ["匿名函数", "anonymous function", "closure"],
      "related": ["function", "closure", "capture"],
      "modules": ["parse", "sema"],
      "classes": [
        {
          "name": "LambdaExpr",
          "file": "src/Parse/Lambda.h",
          "line": 45
        }
      ],
      "functions": [
        {
          "name": "ParseLambda",
          "file": "src/Parse/Lambda.cpp",
          "line": 100
        },
        {
          "name": "TypeCheckLambda",
          "file": "src/Sema/Lambda.cpp",
          "line": 234
        }
      ],
      "tfidf_score": 0.85
    }
  }
}
```

## TF-IDF 权重说明

TF-IDF (Term Frequency-Inverse Document Frequency) 用于衡量关键词的重要性：

- **TF (词频)**: 关键词在文档中出现的频率
- **IDF (逆文档频率)**: log(总文档数 / 包含该关键词的文档数)
- **TF-IDF**: TF × IDF

在我们的实现中：
- 每个代码元素（类或函数）视为一个文档
- 文档频率 = 包含该关键词的类数 + 函数数
- TF = 文档频率 / 总文档数
- IDF = log(总文档数 / 文档频率)

**权重解释**：
- 高 TF-IDF：关键词在少数文档中频繁出现（高度相关）
- 低 TF-IDF：关键词在很多文档中出现（通用词）

## 同义词处理

当合并 Markdown 描述时，系统会自动为同义词创建索引条目：

```python
# 主关键词
lambda_entry = {
    "keyword": "lambda",
    "synonyms": ["匿名函数", "anonymous function"],
    ...
}

# 自动创建同义词条目
synonym_entry = {
    "keyword": "匿名函数",
    "synonyms": ["lambda"],  # 指向主关键词
    ...  # 复制主关键词的其他信息
}
```

这样用户搜索 "匿名函数" 时也能找到 lambda 相关的信息。

## 性能优化

1. **倒排索引**: 使用字典存储关键词到代码元素的映射，查找时间 O(1)
2. **批量处理**: 一次性处理所有模块，避免重复遍历
3. **延迟计算**: TF-IDF 权重在索引构建完成后统一计算
4. **内存优化**: 使用 dataclass 减少内存占用

## 测试

运行测试：

```bash
python3 test_search_index_builder.py
```

测试覆盖：
- ✓ 基本索引构建
- ✓ Markdown 描述合并
- ✓ TF-IDF 权重计算
- ✓ JSON 序列化
- ✓ 添加自定义条目

## 依赖

- `module_analyzer.py`: 提供模块树
- `keyword_extractor.py`: 提取关键词
- `markdown_parser.py`: 解析 Markdown 描述
- `cpp_parser.py`: 提供代码元素数据结构

## 注意事项

1. **关键词规范化**: 所有关键词转换为小写，确保搜索不区分大小写
2. **同义词去重**: 同义词索引会自动去重，避免重复条目
3. **空描述处理**: 如果 Markdown 描述为空，使用空字符串而不是 None
4. **TF-IDF 边界情况**: 如果没有文档，TF-IDF 分数为 0

## 扩展性

### 添加新的代码元素类型

```python
# 在 IndexEntry 中添加新字段
@dataclass
class IndexEntry:
    ...
    enums: List[CodeLocation] = field(default_factory=list)  # 新增

# 在 SearchIndexBuilder 中添加处理逻辑
def _build_inverted_index(self, module_tree: ModuleTree):
    ...
    for enum_info in module.enums:
        enum_keywords = self.keyword_extractor.extract_from_enum(enum_info)
        for keyword in enum_keywords:
            self.keyword_to_enums[keyword].append(enum_info)
```

### 自定义 TF-IDF 计算

```python
class CustomSearchIndexBuilder(SearchIndexBuilder):
    def _calculate_tfidf(self, index: SearchIndex):
        # 自定义 TF-IDF 计算逻辑
        for keyword, entry in index.keywords.items():
            # 使用自定义公式
            entry.tfidf_score = custom_formula(entry)
```

## 相关文档

- [KeywordExtractor 文档](README_KEYWORD_EXTRACTOR.md)