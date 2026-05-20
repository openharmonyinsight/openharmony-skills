# KeywordExtractor 关键词提取器

## 概述

KeywordExtractor 是知识库索引构建层的核心组件，负责从代码元素（类名、函数名）中提取可搜索的关键词。

## 功能特性

### 1. 驼峰命名拆分
- 将驼峰命名拆分为独立单词
- 示例：`TypeChecker` → `['type', 'checker']`
- 支持连续大写字母：`HTTPServer` → `['http', 'server']`

### 2. 中文分词
- 使用 jieba 库进行中文分词
- 支持中英文混合文本
- 优雅降级：如果 jieba 未安装，仍可处理英文

### 3. 英文单词提取
- 从文本中提取英文单词
- 自动过滤停用词（the, a, is 等）
- 过滤短词（长度 ≤ 2）

### 4. 类名关键词提取
- 提取完整类名（小写）
- 拆分驼峰命名
- 添加类型标识（class/struct）
- 支持中文类名分词

### 5. 函数名关键词提取
- 提取完整函数名（小写）
- 拆分驼峰命名
- 添加 'function' 标识
- 支持中文函数名分词

## 使用方法

### 基本用法

```python
from keyword_extractor import KeywordExtractor
from cpp_parser import ClassInfo, FunctionInfo

extractor = KeywordExtractor()

# 从类名提取关键词
cls = ClassInfo(name='TypeChecker', file='test.cpp', line=10)
keywords = extractor.extract_from_class(cls)
# 结果: ['typechecker', 'type', 'checker', 'class']

# 从函数名提取关键词
func = FunctionInfo(name='ParseLambda', file='test.cpp', line=100)
keywords = extractor.extract_from_function(func)
# 结果: ['parselambda', 'parse', 'lambda', 'function']

# 从任意文本提取关键词
keywords = extractor.extract_from_text('GenericInstantiator')
# 结果: ['genericinstantiator', 'generic', 'instantiator']
```

### 驼峰命名拆分

```python
words = extractor.split_camel_case('BuildLambdaClosure')
# 结果: ['build', 'lambda', 'closure']
```

### 中文分词

```python
# 需要先安装 jieba: pip3 install jieba
words = extractor.tokenize_chinese('类型检查器')
# 结果: ['类型', '检查器']
```

## 依赖

- Python 3.8+
- jieba >= 0.42.1（可选，用于中文分词）

安装依赖：
```bash
pip3 install -r requirements.txt
```

## 测试

运行单元测试：
```bash
python3 test_keyword_extractor.py
```

运行集成测试：
```bash
python3 test_integration.py
```

## 设计决策

### 为什么使用 jieba？
- 成熟的中文分词库
- 支持自定义词典
- 性能良好

### 为什么支持优雅降级？
- 即使 jieba 未安装，系统仍可处理英文代码
- 提高系统的健壮性
- 方便在不同环境中部署

### 停用词列表
- 过滤常见的无意义英文单词
- 减少索引大小
- 提高搜索相关性

## 与其他组件的集成

KeywordExtractor 在知识库生成流程中的位置：

```
FileScanner → CppParser → ModuleAnalyzer → KeywordExtractor → SearchIndexBuilder
```

1. **FileScanner** 扫描源码文件
2. **CppParser** 解析文件，提取类和函数
3. **ModuleAnalyzer** 构建模块树
4. **KeywordExtractor** 从类和函数提取关键词
5. **SearchIndexBuilder** 使用关键词构建搜索索引

## 未来改进

- [ ] 支持自定义停用词列表
- [ ] 支持同义词扩展
- [ ] 支持词干提取（stemming）
- [ ] 支持更多语言的分词
- [ ] 添加关键词权重计算

## 相关文件

- `keyword_extractor.py` - 主实现
- `test_keyword_extractor.py` - 单元测试
- `test_integration.py` - 集成测试
- `requirements.txt` - Python 依赖
