# 扫描核心算法规范

本文档定义扫描过程中两个核心算法的技术规范，供模型在执行规则扫描时直接实现。

---

## 算法一: it() / describe() 块范围提取

### 用途

确定源代码中每一行所属的 `it()` 块名称，用于填充 issue 的 `testcase` 字段。同时提取 `describe()` 块用于 R011 testsuite 去重。

### 输入

- `content`: 文件全部文本内容（字符串）
- `line_num`: 目标行号（1-based，用于 `find_testcase_for_line`）

### 输出

- `parse_it_blocks(content)` → `[{name, start, end}, ...]`
- `parse_describe_blocks(content)` → `[{name, start, end}, ...]`
- `find_testcase_for_line(it_blocks, line_num)` → `string | "-"`

### 算法: 解析 it() 块

#### 第1步: 定位 it() 声明行

逐行扫描，对每行 stripped 内容匹配以下正则：

```
it(?:\.only|\.skip|\.each)?\s*\(\s*['"](.+?)['"]\s*,
```

- 支持修饰符: `it()`, `it.only()`, `it.skip()`, `it.each()`
- 第一个捕获组为 testcase 名称
- 匹配成功后，记录 `name` 和当前行号 `start`

#### 第2步: 大括号状态机追踪块体范围

从 it() 声明行开始，逐字符扫描后续所有行，使用状态机计算块体结束位置。

**状态变量:**
- `brace_open`, `brace_close`: 大括号计数器
- `in_single`, `in_double`, `in_backtick`: 是否在字符串字面量内
- `found_body`: 是否已遇到第一个 `{`

**单字符处理逻辑（按优先级）:**

```
对每个字符 c:
  1. 如果 c == '\' 且当前在任意字符串内 → 跳过下一个字符（转义处理）
  2. 如果 c == '`' 且不在单/双引号内 → 切换 in_backtick
  3. 如果 c == "'" 且不在双引号/反引号内 → 切换 in_single
  4. 如果 c == '"' 且不在单引号/反引号内 → 切换 in_double
  5. 如果不在任何字符串内:
     - c == '{' → brace_open++, found_body = true
     - c == '}'
```

**终止条件:**

```
当 found_body && brace_close >= brace_open && brace_open > 0:
  块体结束行 = 当前行号
  记录 {name, start, end}
```

#### 第3步: 行号归属判定

对给定的 `line_num`，遍历所有 it() 块，找到满足 `start <= line_num <= end` 的块，返回其 `name`。未找到返回 `"-"`。

### describe() 块解析

算法与 it() 完全相同，仅正则中的 `it` 替换为 `describe`:

```
describe(?:\.only|\.skip|\.each)?\s*\(\s*['"](.+?)['"]\s*,
```

### 关键注意事项

1. **字符串内大括号不计入**: 这是本算法的核心设计点。模板字符串 `` `count: ${n}` `` 中的 `{` 和 `}` 必须被跳过，否则会错误截断块体范围。这是陷阱1和陷阱1b的根源（详见 TRAPS.md）。
2. **反引号优先级**: 反引号必须在单/双引号判定之前检查。反引号字符串内的 `'` 和 `"` 不作为字符串定界符。
3. **转义字符**: 字符串内的 `\` 后跟任意字符应跳过（包括 `\"`, `\'`, `\``），防止转义引号被误识别为字符串结束。
4. **块体可能跨多行**: 从 it() 声明行到匹配的 `}` 可能跨越数十行甚至数百行，必须逐行逐字符扫描。
5. **未闭合块体**: 如果文件结束时未找到匹配的 `}`，该 it() 块不记录（容错处理）。

### 影响规则

R004（缺少断言需判断是否在it()块内）, R015（Level参数需定位到具体it()块）, R016（testcase名称检测对象是it()参数）, R018（testcase重复需提取it()名称）, R019（.key重复需关联testcase）, R020（.id重复需关联testcase）

---

## 算法二: 子系统名称映射

### 用途

根据文件相对路径，映射到所属子系统名称，用于填充 issue 的 `subsystem` 字段。

### 输入

- `file_path`: 文件的相对路径（使用 `/` 分隔符，如 `arkui/ace_engine/test/test.ets`）
- `mapping_file`: 映射表文件路径（默认 `references/subsystem_mapping.md`）

### 输出

- 子系统名称字符串，未匹配到返回 `"-"`

### 映射表格式

映射表支持两种格式:

**格式1: Markdown 表格（默认格式）**

```
| 目录路径 | 子系统 |
|----------|--------|
| arkui/ace_engine | 方舟UI |
| multimedia/camera_framework | 多媒体 |
```

**格式2: 箭头分隔**

```
arkui/ace_engine -> 方舟UI
multimedia/camera_framework -> 多媒体
```

### 算法: 最长目录前缀匹配

#### 第1步: 加载映射表

解析映射文件，构建 `{目录路径 → 子系统名称}` 字典。跳过表头行（`目录路径`）。

#### 第2步: 按路径长度降序排序

将所有目录路径按键长度降序排列:

```
sorted_keys = sort(mapping.keys(), by=length, descending)
```

**必须降序排序**，确保最长匹配优先。例如同时存在 `arkui` 和 `arkui/ace_engine` 时，`arkui/ace_engine/test.ets` 应匹配到 `方舟UI` 而非 `arkui` 对应的子系统。

#### 第3步: 前缀匹配

```
对 file_path 中的每个 sorted_key:
  如果 file_path 以 sorted_key + "/" 开头:
    返回 mapping[sorted_key]

未匹配 → 返回 "-"
```

**注意**: 匹配时必须在目录路径后追加 `/`，防止 `arkui` 错误匹配 `arkui_xxx`。

### 关键注意事项

1. **路径分隔符统一**: Windows 反斜杠 `\` 需替换为 `/`。
2. **仅匹配目录前缀**: 匹配条件是 `file_path.startswith(dir_prefix + "/")`，不是简单的 `contains`。
3. **排序只做一次**: 映射表加载后排序结果可缓存，避免每次调用重新排序。
4. **映射表为空**: 如果映射文件不存在或内容为空，所有文件的子系统返回 `"-"`。
