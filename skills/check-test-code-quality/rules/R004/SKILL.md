---
rule: R004
type: 测试用例缺少断言
severity: Critical
complexity: 最复杂规则（L5）
scan_scope: .ets, .ts, .js
---

# R004: 测试用例缺少断言

## 规则概述

| 属性 | 值 |
|------|-----|
| 规则编号 | R004 |
| 问题类型 | 测试用例缺少断言 |
| 严重级别 | Critical |
| 复杂度 | L5（最复杂规则） |
| 扫描范围 | 所有源代码文件（`.ets`, `.ts`, `.js`） |

## 问题描述

测试用例（`it()`）中完全没有断言。断言是测试用例的核心，用于验证被测功能是否符合预期。没有断言的测试用例无法验证任何功能，等同于无效测试。

## 修复方法

在 `it()` 块中添加有效的断言方法，检查实际业务逻辑结果。

## Hypium 框架支持的断言方法

以下断言方法均视为有效断言：

```
assertClose           assertContain           assertEqual
assertFail            assertFalse             assertTrue
assertInstanceOf      assertLarger            assertLess
assertLargerOrEqual   assertLessOrEqual       assertNull
assertThrowError      assertUndefined         assertNaN
assertNegUnlimited    assertPosUnlimited      assertDeepEquals
expect(...)           (配合 .assert* 链式调用)
```

---

## 检测逻辑总览

```
┌─────────────────────────────────────────────────────────┐
│                    R004 扫描流程                         │
├─────────────────────────────────────────────────────────┤
│  1. 找到所有 it() 块                                    │
│  2. 提取函数体内容（字符串感知的大括号匹配）               │
│  3. 检查直接断言 → 有则跳过                              │
│  4. 收集所有函数定义（本文件 + 跨文件 import）            │
│  5. 递归检查间接断言（最大深度5层）                       │
│  6. try-catch 断言检测（两分支都必须有断言）              │
│  7. 辅助函数 try-catch 缺陷检测（Warning级别）            │
│  8. 生成具体修复建议                                     │
└─────────────────────────────────────────────────────────┘
```

---

## 核心检测步骤详解

### 步骤1：找到所有 it() 块

使用正则表达式匹配 `it()` 函数调用，提取测试用例名称、行号、列位置：

```python
def find_it_blocks(content):
    it_blocks = []
    lines = content.split('\n')
    for i, line in enumerate(lines):
        stripped = line.strip()
        # 匹配 it('name', ...) 或 it("name", ...) 模式
        m = re.match(r"it\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*(.*)", stripped)
        if not m:
            m = re.match(r"it\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*", stripped)
            if m:
                it_blocks.append({
                    'name': m.group(1),
                    'line': i + 1,
                    'col': m.end(),
                    'full_line': line,
                    'rest': stripped[m.end():],
                })
            continue
        it_blocks.append({
            'name': m.group(1),
            'line': i + 1,
            'col': m.start(),
            'full_line': line,
            'rest': m.group(2),
        })
    return it_blocks
```

### 步骤2：提取函数体内容（字符串感知的大括号匹配）

**⚠️ 陷阱 #1（CRITICAL）：字符串字面量中的大括号**

必须跳过字符串字面量内的 `{` 和 `}`，使用状态机解析。朴素的大括号计数曾导致 53,951 个误报。

```python
def count_braces_outside_strings(text, start_idx=0):
    """
    统计大括号数量，跳过字符串字面量和模板字符串。
    使用状态机追踪 in_single, in_double, in_backtick 状态。
    """
    open_count = 0
    close_count = 0
    in_single = False
    in_double = False
    in_backtick = False
    i = start_idx
    while i < len(text):
        ch = text[i]
        if ch == '\\' and (in_single or in_double or in_backtick):
            i += 2  # 跳过转义字符
            continue
        if not in_single and not in_double and not in_backtick:
            if ch == '{':
                open_count += 1
            elif ch == '}':
                close_count -= 1
        if ch == '`' and not in_single and not in_double:
            in_backtick = not in_backtick
        elif ch == "'" and not in_double and not in_backtick:
            in_single = not in_single
        elif ch == '"' and not in_single and not in_backtick:
            in_double = not in_double
        i += 1
    return open_count, close_count
```

```python
def find_matching_brace(content, start_idx, open_char='{', close_char='}'):
    """
    带字符串感知的大括号匹配。
    跳过单引号、双引号、反引号字符串中的大括号。
    """
    depth = 0
    i = start_idx
    while i < len(content):
        if content[i] == open_char:
            depth += 1
        elif content[i] == close_char:
            depth -= 1
            if depth == 0:
                return i
        elif content[i] == '"' or content[i] == "'":
            quote = content[i]
            j = i + 1
            while j < len(content):
                if content[j] == '\\':
                    j += 2
                    continue
                if content[j] == quote:
                    i = j
                    break
                j += 1
        elif content[i] == '`':
            j = i + 1
            while j < len(content):
                if content[j] == '\\':
                    j += 2
                    continue
                if content[j] == '`':
                    i = j
                    break
                j += 1
        i += 1
    return -1
 ```

**⚠️ 陷阱 #1b（CRITICAL）：反引号模板字符串中的撇号/引号干扰**

TypeScript/JavaScript的反引号模板字符串（`` `...` ``）中可能包含撇号或引号。如果状态机不追踪反引号状态，会将模板字符串内的`'`误识别为单引号字符串定界符，导致大括号匹配错误。

**触发条件**: it()块内使用反引号模板字符串，且字符串中包含`'`或`"`

**典型代码**:
```typescript
it('testGetPath', Level.LEVEL3, async (done: Function) => {
  try {
    let path = certManager.getCertificateStorePath(property);
    // 下面这行反引号模板字符串中包含 user's
    console.info(`Success to get user's path: ${path}`);
    // 如果没有 in_backtick 追踪:
    //   's path: ${path}' 被当成单引号字符串开始
    //   后续 } catch (err) { ... } 中的 } 被跳过
    //   it()函数体范围错误延伸，断言检测失效
    expect(path).assertEqual('/data/certificates/user_cacerts/100');
  } catch (err) {
    expect(null).assertFail();
  }
});
```

**影响**: 有断言的用例被误判为缺少断言（R004误报），或it()/describe()块范围错误（R018误报）。

**修复**: 在所有大括号匹配的状态机中增加`in_backtick`状态：
```python
# 在匹配单引号/双引号时，必须同时检查不在反引号字符串内
if ch == '`' and not in_single and not in_double:
    in_backtick = not in_backtick
elif ch == "'" and not in_double and not in_backtick:  # 必须加 not in_backtick
    in_single = not in_single
elif ch == '"' and not in_single and not in_backtick:   # 必须加 not in_backtick
    in_double = not in_double
```

**影响范围**: R004（it()块范围提取）, R018（describe块范围提取）, 以及任何使用大括号匹配解析代码结构的规则。

```python
def extract_block_content(content, start_line, block_start_col):
    """
    从 it() 所在行提取函数体内容。
    定位 => 箭头，然后提取 { } 块。
    """
    lines = content.split('\n')
    idx = start_line - 1
    if idx < 0 or idx >= len(lines):
        return "", start_line
    line = lines[idx]
    pos_in_line = block_start_col

    # 查找箭头 => 
    arrow_idx = -1
    for prefix in ['=>', '=> ']:
        pidx = line.find(prefix, pos_in_line)
        if pidx != -1:
            arrow_idx = pidx
            break
    if arrow_idx == -1:
        return "", start_line

    # 查找函数体起始大括号
    brace_idx = line.find('{', arrow_idx + 2)
    if brace_idx == -1:
        return "", start_line

    # 从当前行开始拼接完整文本，匹配大括号
    full_text = '\n'.join(lines[idx:])
    block_start = brace_idx
    block_end = find_matching_brace(full_text, block_start, '{', '}')
    if block_end == -1:
        return "", start_line

    block_content = full_text[block_start + 1:block_end]
    block_start_line = start_line + full_text[:block_start].count('\n')
    return block_content, block_start_line
```

### 步骤3：检查直接断言

```python
ASSERTION_PATTERNS = [
    re.compile(r'\bexpect\s*\('),
    re.compile(r'\bassertEqual\s*\('),
    re.compile(r'\bassertNotEqual\s*\('),
    re.compile(r'\bassertTrue\s*\('),
    re.compile(r'\bassertFalse\s*\('),
    re.compile(r'\bassertNull\s*\('),
    re.compile(r'\bassertNotNull\s*\('),
    re.compile(r'\bassertUndefined\s*\('),
    re.compile(r'\bassertDefined\s*\('),
    re.compile(r'\bassertFail\s*\('),
    re.compile(r'\bassertInstanceOf\s*\('),
    re.compile(r'\bassertThrow\s*\('),
    re.compile(r'\bassertContains\s*\('),
    re.compile(r'\bassertDeepEquals\s*\('),
    re.compile(r'\bassertStrictEquals\s*\('),
    re.compile(r'\bcheckResult\s*\('),
]


def has_assertion(text):
    if not text:
        return False
    for pattern in ASSERTION_PATTERNS:
        if pattern.search(text):
            return True
    return False
```

### 步骤4：收集所有函数定义

这是 R004 规则的核心复杂度所在。需要收集以下所有类型的函数定义：

| 函数类型 | 示例 | 正则模式 |
|---------|------|---------|
| 普通函数声明 | `function foo() {` | `(?:function\s+)` |
| async 函数声明 | `async function foo() {` | `(?:async\s+function\s+)` |
| static 方法 | `static foo() {` | `(?:static\s+)` |
| static async 方法 | `static async foo() {` | `(?:static\s+(?:async\s+)?)` |
| 非static async 方法 | `async foo() {` | `(?:async\s+)` |
| 箭头函数 | `let foo = () => {` | `(?:let\|const\|var)\s+(\w+)\s*(?::\s*[^=]+)?\s*=\s*(?:async\s*)?\(...\)\s*=>` |
| 跨行箭头函数 | 类型注解分多行 | 多行合并匹配 |
| 跨行函数声明 | 参数列表分多行 | `full_text` 方式查找 `{` |
| 类方法 | class 内部的方法 | `extract_class_methods()` |

```python
def collect_function_definitions(content, filepath):
    """
    收集文件中所有函数定义及其函数体。
    支持：普通函数、async函数、static方法、箭头函数、跨行定义。
    """
    funcs = {}
    lines = content.split('\n')

    for i, line in enumerate(lines):
        # 1. 普通函数 / async函数 / static方法
        m = re.search(
            r'(?:function\s+|static\s+(?:async\s+)?|async\s+function\s+)(\w+)\s*\(',
            line
        )
        if m:
            fname = m.group(1)
            # ⚠️ 关键：使用 full_text 方式查找 {，支持跨行参数声明
            full_text = '\n'.join(lines[i:])
            brace_idx = full_text.find('{', m.end() - m.start())
            if brace_idx == -1:
                continue
            block_end = find_matching_brace(full_text, brace_idx, '{', '}')
            if block_end == -1:
                continue
            body = full_text[brace_idx + 1:block_end]
            funcs[fname] = body
            continue

        # 2. 箭头函数（单行）
        m = re.search(
            r'(?:let|const|var)\s+(\w+)\s*(?::\s*[^=]+)?\s*=\s*(?:async\s*)?\([^)]*(?:\([^)]*\)[^)]*)*\)\s*(?:async\s*)?=>',
            line
        )
        if m:
            fname = m.group(1)
            rest = line[m.end() - 2:]
            full_text = '\n'.join(lines[i:])
            abs_pos = m.end() - 2
            brace_idx = full_text.find('{', abs_pos)
            if brace_idx == -1:
                continue
            block_end = find_matching_brace(full_text, brace_idx, '{', '}')
            if block_end == -1:
                continue
            body = full_text[brace_idx + 1:block_end]
            funcs[fname] = body
            continue

        # 3. 跨行箭头函数（类型注解导致 = 在下一行）
        m = re.search(r'(?:let|const|var)\s+(\w+)\s*:', line)
        if m and line.rstrip().endswith('='):
            fname = m.group(1)
            combined = line
            for j in range(i + 1, min(i + 5, len(lines))):
                combined += ' ' + lines[j].strip()
                # ⚠️ 使用 .+ 替代 [^=]+，兼容类型注解中的 =>
                m2 = re.search(
                    r'(?:let|const|var)\s+\w+\s*:\s*.+=\s*(?:async\s*)?\([^)]*(?:\([^)]*\)[^)]*)*\)\s*(?:async\s*)?=>',
                    combined
                )
                if m2:
                    full_text = '\n'.join(lines[i:])
                    abs_pos = combined.index('=>', m2.start()) + 2
                    brace_idx = full_text.find('{', abs_pos)
                    if brace_idx == -1:
                        break
                    block_end = find_matching_brace(full_text, brace_idx, '{', '}')
                    if block_end == -1:
                        break
                    body = full_text[brace_idx + 1:block_end]
                    funcs[fname] = body
                    break
                if '{' in lines[j]:
                    break

    return funcs
```

### 步骤4b：提取类方法

```python
def extract_class_methods(content):
    """
    提取 class 中所有方法的函数体。
    支持 static 方法、非static async 方法。
    """
    methods = {}
    lines = content.split('\n')
    in_class = False
    class_indent = 0

    for i, line in enumerate(lines):
        stripped = line.lstrip()

        # 识别 class 声明
        if re.match(r'(?:export\s+)?(?:default\s+)?class\s+\w+', stripped):
            in_class = True
            class_indent = len(line) - len(stripped)
            continue

        if in_class:
            current_indent = len(line) - len(stripped)
            # class 结束
            if stripped.startswith('}') and current_indent <= class_indent:
                in_class = False
                continue

            if current_indent > class_indent:
                full_text = '\n'.join(lines[i:])

                # static 方法（含 async）
                m = re.search(
                    r'static\s+(?:async\s+)?(\w+)\s*\([^)]*(?:\([^)]*\)[^)]*)*\)',
                    stripped
                )
                if m:
                    fname = m.group(1)
                    # ⚠️ 使用 full_text 方式查找 {，支持跨行参数
                    abs_start = m.start() + stripped.find(m.group(0))
                    brace_idx = full_text.find('{', abs_start)
                    if brace_idx != -1:
                        block_end = find_matching_brace(full_text, brace_idx, '{', '}')
                        if block_end != -1:
                            body = full_text[brace_idx + 1:block_end]
                            methods[fname] = body
                            # 递归收集内部函数
                            inner_funcs = collect_function_definitions(body, "")
                            for inner_name, inner_body in inner_funcs.items():
                                if inner_name not in methods:
                                    methods[inner_name] = inner_body
                    continue

                # ⚠️ 非static async 方法（关键修复）
                m = re.search(r'(?:async\s+)(\w+)\s*\(', stripped)
                if m:
                    fname = m.group(1)
                    abs_start = m.start() + stripped.find(m.group(0))
                    brace_idx = full_text.find('{', abs_start)
                    if brace_idx != -1:
                        block_end = find_matching_brace(full_text, brace_idx, '{', '}')
                        if block_end != -1:
                            body = full_text[brace_idx + 1:block_end]
                            methods[fname] = body
                            inner_funcs = collect_function_definitions(body, "")
                            for inner_name, inner_body in inner_funcs.items():
                                if inner_name not in methods:
                                    methods[inner_name] = inner_body

    return methods
```

### 步骤5：递归间接断言检测

**核心函数**：递归检查函数调用链中是否包含断言。

```python
MAX_RECURSION_DEPTH = 5


def check_function_has_assertion(body, local_funcs, all_known_funcs, visited=None, depth=0):
    """
    递归检查函数体中是否包含直接或间接断言。

    检查顺序（关键）：
    1. 直接断言检查
    2. 本地函数调用链
    3. 跨文件函数调用链
    4. try-catch 块检查（最后）

    ⚠️ visited 集合延迟标记：只在确定需要递归时才 add，防止污染。
    """
    if visited is None:
        visited = set()
    if depth > MAX_RECURSION_DEPTH:
        return False

    # 1. 直接断言
    if has_assertion(body):
        return True

    # 2. 本地函数调用链
    for fname, fbody in local_funcs.items():
        key = f"local:{fname}"
        if key in visited:
            continue
        # ⚠️ 延迟标记：先检查再标记
        if not (fname in body and fbody):
            continue
        visited.add(key)
        if check_function_has_assertion(
            fbody, local_funcs, all_known_funcs, visited, depth + 1
        ):
            return True

    # 3. 跨文件函数调用链
    for fname, fbody in all_known_funcs.items():
        key = f"known:{fname}"
        if key in visited:
            continue
        if fname in local_funcs:
            continue
        if not (fname in body and fbody):
            continue
        visited.add(key)
        if check_function_has_assertion(
            fbody, {}, all_known_funcs, visited, depth + 1
        ):
            return True

    # 4. try-catch 块检查（放在最后）
    try_blocks = find_try_catch_blocks(body)
    if try_blocks:
        for tb in try_blocks:
            if not has_assertion(tb['try_content']) and not has_assertion(tb['catch_content']):
                return False
            if has_assertion(tb['try_content']) and has_assertion(tb['catch_content']):
                return True
        return False

    return False
```

**visited 集合延迟标记的重要性**：

```
错误做法（会导致visited集合污染）：
  visited.add(key)           # ← 在检查之前就标记
  if fname in body and fbody:
      if check_function_has_assertion(fbody, ...):
          return True

正确做法（延迟标记）：
  if fname in body and fbody:  # ← 先检查是否需要递归
      visited.add(key)          # ← 确定需要时才标记
      if check_function_has_assertion(fbody, ...):
          return True
```

误报案例：`msSleep` 递归调用中遍历 `all_known_funcs` 时，如果将不在其 body 中的 `registerEvent` 也标记为 visited，导致回到上层后 `registerEvent` 被跳过。

### 步骤6：跨文件 import 解析

```python
IMPORT_CACHE = {}


def parse_imports(content, filepath):
    """
    解析 import 语句，返回 (named_imports, default_import_paths)。

    ⚠️ 必须使用 re.finditer 而非 re.search，支持多个 default import。
    """
    imports = {}
    default_imports = []

    # Named imports: import { foo, bar } from './utils'
    for m in re.finditer(r'import\s+\{([^}]+)\}\s+from\s+["\'](.+?)["\']', content):
        names = [n.strip() for n in m.group(1).split(',')]
        path = m.group(2)
        for name in names:
            imports[name] = path

    # ⚠️ Default imports: import Utils from './Utils'
    # 必须使用 finditer 捕获所有 default import
    for default_m in re.finditer(r'import\s+(\w+)\s+from\s+["\'](.+?)["\']', content):
        default_imports.append(default_m.group(2))

    return imports, default_imports


def resolve_import_file(import_path, current_filepath):
    """
    解析 import 路径为实际文件路径。
    支持相对路径 (./ 和 ../)。
    """
    if import_path.startswith('./') or import_path.startswith('../'):
        base_dir = os.path.dirname(current_filepath)
        resolved = os.path.normpath(os.path.join(base_dir, import_path))
        for ext in ['.test.ets', '.test.ts', '.ets', '.ts']:
            if os.path.exists(resolved + ext):
                return resolved + ext
        if os.path.exists(resolved):
            return resolved
    return None


def get_imported_functions(filepath):
    """
    从 import 的文件中提取所有函数定义。
    使用 IMPORT_CACHE 缓存，避免重复读取。
    """
    if filepath in IMPORT_CACHE:
        return IMPORT_CACHE[filepath]
    if not os.path.exists(filepath):
        return {}

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        return {}

    funcs = collect_function_definitions(content, filepath)
    methods = extract_class_methods(content)
    funcs.update(methods)

    IMPORT_CACHE[filepath] = funcs
    return funcs
```

**多 default import 支持的重要性**：

```
文件中可能同时存在：
  import router from '@ohos.router'    // 第一个 default import
  import Utils from './Utils'           // 第二个 default import

如果使用 re.search，只会捕获第一个 (router)，遗漏 Utils。
修复后使用 re.finditer，捕获所有 default import。
```

### 步骤7：Try-catch 断言检测

**核心原则**：如果 `it()` 块中存在 try-catch，则 try 和 catch 的每个分支都必须包含断言。

```python
def find_try_catch_blocks(body):
    """
    查找函数体中的所有 try-catch 块。

    ⚠️ 关键处理：
    - } catch { 同行模式：当 try 的 } 和 catch { 在同一行时，
      大括号计数会导致互相抵消。必须优先检查此模式。
    """
    try_blocks = []
    lines = body.split('\n')
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if re.match(r'try\s*\{', stripped):
            try_start = i
            brace_count = stripped.count('{') - stripped.count('}')
            j = i + 1
            try_end_line = -1
            while j < len(lines) and brace_count > 0:
                line_j = lines[j].strip()
                # ⚠️ 优先检查 } catch { 同行模式
                if re.match(r'\}\s*catch\s*(?:\([^)]*\))?\s*\{', line_j):
                    try_end_line = j
                    break
                open_count = line_j.count('{')
                close_count = line_j.count('}')
                brace_count += open_count - close_count
                if brace_count == 0:
                    try_end_line = j
                    break
                j += 1

            if try_end_line == -1:
                i = j + 1
                continue

            try_content_end = try_end_line + 1

            # 查找 catch 块
            catch_start = -1
            catch_end = -1

            # 同行 } catch { 模式
            close_catch_m = re.match(
                r'\}\s*catch\s*(?:\([^)]*\))?\s*\{', lines[try_end_line].strip()
            )
            if close_catch_m:
                catch_start = try_end_line
                catch_brace_count = 1
                k = catch_start + 1
                while k < len(lines) and catch_brace_count > 0:
                    catch_brace_count += lines[k].count('{') - lines[k].count('}')
                    k += 1
                catch_end = k
            else:
                # 异行 catch 模式
                scan_j = try_end_line + 1
                while scan_j < len(lines):
                    catch_m = re.match(
                        r'\}\s*catch\s*(?:\([^)]*\))?\s*\{', lines[scan_j].strip()
                    )
                    if catch_m:
                        catch_start = scan_j
                        catch_brace_count = 1
                        k = catch_start + 1
                        while k < len(lines) and catch_brace_count > 0:
                            catch_brace_count += lines[k].count('{') - lines[k].count('}')
                            k += 1
                        catch_end = k
                        break
                    elif re.match(r'\}\s*finally\s*\{', lines[scan_j].strip()):
                        break
                    elif lines[scan_j].strip() == '}':
                        break
                    scan_j += 1

            try_content = '\n'.join(lines[try_start:try_content_end])
            catch_content = ''
            if catch_start != -1 and catch_end != -1:
                catch_content = '\n'.join(lines[catch_start:catch_end])

            try_blocks.append({
                'try_content': try_content,
                'catch_content': catch_content,
                'try_line': try_start,
                'catch_line': catch_start if catch_start != -1 else -1,
            })
            i = max(catch_end if catch_end > 0 else try_content_end, i + 1)
        else:
            i += 1
    return try_blocks
```

### 步骤7b：有效断言检测（过滤注释断言）

```python
def has_effective_assertion(text):
    """
    检查文本中是否包含有效（未注释）的断言。
    过滤以 // 开头的行后再检查断言模式。
    """
    if not text:
        return False
    lines = text.split('\n')
    effective_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('//'):
            continue
        effective_lines.append(line)
    effective_text = '\n'.join(effective_lines)
    for pattern in ASSERTION_PATTERNS:
        if pattern.search(effective_text):
            return True
    return False
```

### 步骤7c：Try-catch 修复建议生成

```python
def analyze_try_catch_suggestion(body, body_start_line, local_funcs, all_known_funcs):
    """
    分析 try-catch 块的断言情况，生成具体修复建议。

    ⚠️ 关键：在生成建议前，先检查整个 body 是否通过函数调用链获得断言覆盖。
    如果 body 有间接断言（如 Utils.registerEvent()），则不应报告 try-catch 缺失。
    """
    try_blocks = find_try_catch_blocks(body)
    if not try_blocks:
        return None

    suggestions = []
    for tb in try_blocks:
        try_has = has_effective_assertion(tb['try_content']) or check_function_has_assertion(
            tb['try_content'], local_funcs, all_known_funcs
        )
        catch_has = False
        if tb['catch_content']:
            catch_has = has_effective_assertion(tb['catch_content']) or check_function_has_assertion(
                tb['catch_content'], local_funcs, all_known_funcs
            )

        if not try_has and not catch_has:
            try_line = body_start_line + tb['try_line']
            catch_line = body_start_line + tb['catch_line'] if tb['catch_line'] != -1 else 0
            if catch_line:
                suggestions.append(
                    f"测试用例缺少断言。检测到try-catch结构，try块（第{try_line}行）和catch块"
                    f"（第{catch_line}行）都缺少断言。请确保try和catch的每个分支都包含断言方法。"
                )
            else:
                suggestions.append(
                    f"测试用例缺少断言。检测到try-catch结构，try块（第{try_line}行）缺少断言。"
                    f"请确保try和catch的每个分支都包含断言方法。"
                )
        elif not try_has:
            try_line = body_start_line + tb['try_line']
            suggestions.append(
                f"测试用例缺少断言。检测到try-catch结构，try块（第{try_line}行）缺少断言。"
                f"请确保try和catch的每个分支都包含断言方法。"
            )
        elif not catch_has and tb['catch_content']:
            catch_line = body_start_line + tb['catch_line']
            suggestions.append(
                f"测试用例缺少断言。检测到try-catch结构，catch块（第{catch_line}行）缺少断言。"
                f"请确保try和catch的每个分支都包含断言方法。"
            )

    if suggestions:
        # ⚠️ 关键：检查 body 是否通过函数调用链获得断言
        body_has_assertion_via_func = check_function_has_assertion(
            body, local_funcs, all_known_funcs
        )
        if body_has_assertion_via_func:
            return None  # 有间接断言，不报告
        return '; '.join(suggestions)
    return None
```

---

## 辅助函数 Try-catch 缺陷检测（Warning 级别）

当 `it()` 通过调用辅助函数获得断言覆盖时，进一步检测这些辅助函数内部的 try-catch 断言缺陷。

```python
def find_try_catch_gaps_in_func_body(body, func_name, func_start_line,
                                      local_funcs, all_known_funcs,
                                      visited=None, depth=0):
    """
    检测函数体中的 try-catch 断言缺陷。
    返回缺陷列表，每个缺陷包含函数名、绝对行号、缺陷类型。
    """
    if visited is None:
        visited = set()
    if depth > MAX_RECURSION_DEPTH:
        return []

    gaps = []
    try_blocks = find_try_catch_blocks(body)

    commented_assertion_re = re.compile(
        r'^\s*//\s*(expect\s*\(|assertEqual\s*\(|assertNotEqual\s*\(|'
        r'assertTrue\s*\(|assertFalse\s*\(|assertNull\s*\(|'
        r'assertNotNull\s*\(|assertFail\s*\()'
    )

    for tb in try_blocks:
        # try 块缺少断言
        try_has = has_effective_assertion(tb['try_content'])
        if not try_has:
            abs_try_line = func_start_line + tb['try_line']
            gaps.append({
                'func_name': func_name,
                'abs_try_line': abs_try_line,
                'gap_type': 'try_missing',
            })

        # 注释掉的断言
        for tl_idx, tl in enumerate(tb['try_content'].split('\n')):
            if commented_assertion_re.match(tl):
                abs_comment_line = func_start_line + tb['try_line'] + tl_idx
                gaps.append({
                    'func_name': func_name,
                    'abs_comment_line': abs_comment_line,
                    'gap_type': 'commented_assertion',
                })

        # catch 块缺少断言
        if tb['catch_content'] and not has_effective_assertion(tb['catch_content']):
            abs_catch_line = func_start_line + tb['catch_line']
            gaps.append({
                'func_name': func_name,
                'abs_catch_line': abs_catch_line,
                'gap_type': 'catch_missing',
            })

    return gaps


def find_try_catch_gaps_in_called_functions(body, local_funcs, all_known_funcs,
                                              filepath='', visited=None, depth=0):
    """
    在被调用的函数中递归查找 try-catch 断言缺陷。
    """
    if visited is None:
        visited = set()
    if depth > MAX_RECURSION_DEPTH:
        return []

    all_gaps = []

    for fname, fbody in local_funcs.items():
        key = f"local_tc:{fname}"
        if key in visited:
            continue
        if not (fname in body and fbody):
            continue
        visited.add(key)
        func_start = resolve_func_source_line(fname, local_funcs, all_known_funcs, filepath)
        gaps = find_try_catch_gaps_in_func_body(
            fbody, fname, func_start, local_funcs, all_known_funcs, visited, depth + 1
        )
        all_gaps.extend(gaps)
        sub_gaps = find_try_catch_gaps_in_called_functions(
            fbody, local_funcs, all_known_funcs, filepath, visited, depth + 1
        )
        all_gaps.extend(sub_gaps)

    for fname, fbody in all_known_funcs.items():
        key = f"known_tc:{fname}"
        if key in visited:
            continue
        if fname in local_funcs:
            continue
        if not (fname in body and fbody):
            continue
        visited.add(key)
        func_start = resolve_func_source_line(fname, local_funcs, all_known_funcs, filepath)
        gaps = find_try_catch_gaps_in_func_body(
            fbody, fname, func_start, {}, all_known_funcs, visited, depth + 1
        )
        all_gaps.extend(gaps)
        sub_gaps = find_try_catch_gaps_in_called_functions(
            fbody, {}, all_known_funcs, filepath, visited, depth + 1
        )
        all_gaps.extend(sub_gaps)

    return all_gaps
```

**去重规则**：同一文件中，每个唯一的 `(function_name, defect_line)` 组合只报告一次。

---

## 事件驱动测试模式

部分测试用例采用事件驱动模式，必须正确识别，避免误报。

```
模式：
  emitEvent()       → 纯工具方法（events_emitter.emit），不含断言（设计如此）
  registerEvent()   → 通过回调函数包含断言（如 expect(backData?.data?.ACTION).assertEqual(expected)）

识别方式：
  registerEvent 的回调参数（如 done: () => void）中包含断言
  extract_class_methods 会提取 registerEvent 的函数体
  函数体中包含回调函数定义，回调函数中有断言
```

---

## 主扫描流程

```python
def scan_file(filepath, base_dir):
    """
    扫描单个测试文件，检测 R004 问题。
    """
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        return issues

    # 快速过滤：文件中没有 it() 则跳过
    if not re.search(r'\bit\s*\(', content):
        return issues

    lines = content.split('\n')

    # 收集本地函数定义
    local_funcs = collect_function_definitions(content, filepath)
    class_methods = extract_class_methods(content)
    local_funcs.update(class_methods)

    # 解析 imports 并收集跨文件函数
    imports, default_imports = parse_imports(content, filepath)
    imported_funcs = {}

    # Named imports
    for name, import_path in imports.items():
        resolved = resolve_import_file(import_path, filepath)
        if resolved:
            funcs = get_imported_functions(resolved)
            imported_funcs.update(funcs)

    # ⚠️ Default imports（使用 finditer 支持多个）
    for import_path in default_imports:
        resolved = resolve_import_file(import_path, filepath)
        if resolved:
            funcs = get_imported_functions(resolved)
            imported_funcs.update(funcs)

    rel_path = os.path.relpath(filepath, base_dir)
    reported_gap_keys = set()

    # 遍历所有 it() 块
    it_blocks = find_it_blocks(content)
    for it in it_blocks:
        body, body_start_line = extract_block_content(
            content, it['line'], it['col']
        )
        if not body:
            continue

        # 快速检查：直接断言
        if has_assertion(body):
            continue

        # try-catch 断言分析
        try_suggestion = analyze_try_catch_suggestion(
            body, body_start_line, local_funcs, imported_funcs
        )
        if try_suggestion:
            issues.append({
                'rule': 'R004',
                'type': '测试用例缺少断言',
                'severity': 'Critical',
                'file': rel_path,
                'line': it['line'],
                'snippet': it['full_line'].strip()[:100],
                'suggestion': f"路径: {rel_path}, 行号: {it['line']}, 问题描述: {try_suggestion}",
                'testcase': it['name'],
            })
            continue

        # 间接断言检查（函数调用链）
        if check_function_has_assertion(body, local_funcs, imported_funcs):
            # 有间接断言，检查辅助函数的 try-catch 缺陷
            tc_gaps = find_try_catch_gaps_in_called_functions(
                body, local_funcs, imported_funcs, filepath
            )
            if tc_gaps:
                gap_parts = []
                gap_keys_for_this_it = set()
                for gap in tc_gaps:
                    gap_key = (
                        gap['func_name'],
                        gap.get('abs_try_line', 0),
                        gap.get('abs_catch_line', 0),
                        gap.get('abs_comment_line', 0),
                    )
                    if gap_key in reported_gap_keys:
                        continue
                    reported_gap_keys.add(gap_key)
                    gap_keys_for_this_it.add(gap_key)
                    if gap['gap_type'] == 'try_missing':
                        gap_parts.append(
                            f"函数 {gap['func_name']} 的try块（第{gap['abs_try_line']}行）缺少有效断言"
                        )
                    elif gap['gap_type'] == 'catch_missing':
                        gap_parts.append(
                            f"函数 {gap['func_name']} 的catch块（第{gap['abs_catch_line']}行）缺少断言"
                        )
                    elif gap['gap_type'] == 'commented_assertion':
                        gap_parts.append(
                            f"函数 {gap['func_name']} 的第{gap['abs_comment_line']}行存在注释掉的断言"
                        )
                if gap_parts:
                    suggestion_text = (
                        f"路径: {rel_path}, 行号: {it['line']}, "
                        f"问题描述: 调用的辅助函数存在try-catch断言缺陷。"
                        + '；'.join(gap_parts)
                        + "。请确保所有分支都包含断言方法。"
                    )
                    issues.append({
                        'rule': 'R004',
                        'type': '辅助函数try-catch断言缺陷',
                        'severity': 'Warning',
                        'file': rel_path,
                        'line': it['line'],
                        'snippet': it['full_line'].strip()[:100],
                        'suggestion': suggestion_text,
                        'testcase': it['name'],
                    })
            continue

        # 完全没有断言
        issues.append({
            'rule': 'R004',
            'type': '测试用例缺少断言',
            'severity': 'Critical',
            'file': rel_path,
            'line': it['line'],
            'snippet': it['full_line'].strip()[:100],
            'suggestion': (
                f"路径: {rel_path}, 行号: {it['line']}, "
                f"问题描述: 测试用例缺少断言。请在it()块中添加expect或assert*断言方法，验证测试结果。"
            ),
            'testcase': it['name'],
        })

    return issues
```

---

## 修复建议格式规范

### 普通（无 try-catch）

```
测试用例缺少断言。请在it()块中添加expect或assert*断言方法，验证测试结果。
```

### Try-catch 相关（必须明确指出分支和行号）

| 场景 | 建议格式 |
|------|---------|
| try 块缺少 | `测试用例缺少断言。检测到try-catch结构，try块（第X行）缺少断言。请确保try和catch的每个分支都包含断言方法。` |
| catch 块缺少 | `测试用例缺少断言。检测到try-catch结构，catch块（第Y行）缺少断言。请确保try和catch的每个分支都包含断言方法。` |
| 两者都缺少 | `测试用例缺少断言。检测到try-catch结构，try块（第X行）和catch块（第Y行）都缺少断言。请确保try和catch的每个分支都包含断言方法。` |
| 辅助函数缺陷 | `调用的辅助函数存在try-catch断言缺陷。函数 {name} 的try块（第X行）缺少有效断言。请确保所有分支都包含断言方法。` |

---

## 问题报告数据结构

```python
{
    'rule': 'R004',
    'type': '测试用例缺少断言',        # 或 '辅助函数try-catch断言缺陷'
    'severity': 'Critical',            # 或 'Warning'（辅助函数缺陷）
    'file': 'rel/path.test.ets',
    'line': 25,
    'snippet': "it('testName', ...",
    'suggestion': '路径: ..., 行号: ..., 问题描述: ...',
    'testcase': 'testName',
}
```

---

## 关键修复历史

| 日期 | 修复内容 | 影响 |
|------|---------|------|
| 2026-03-25 | 跨文件 import 解析 | 支持跨文件函数引用 |
| 2026-03-27 | 多 default import 支持 | 修复 re.search → re.finditer |
| 2026-03-27 | visited 集合延迟标记 | 防止 visited 集合污染 |
| 2026-03-27 | try-catch 与跨文件函数优先级 | 先检查跨文件，最后检查 try-catch |
| 2026-03-27 | 多行箭头函数支持 | 类型注解跨行时的函数体提取 |
| 2026-03-27 | 多行函数声明支持 | 参数列表跨行时的函数体提取 |
| 2026-03-27 | 非static 类方法支持 | async 类方法的函数体收集 |
| 2026-03-27 | `} catch {` 同行模式 | switch 语句中的 try-catch |
| 2026-03-27 | 注释断言识别 | has_effective_assertion() |
| 2026-03-27 | 辅助函数 try-catch 缺陷检测 | Warning 级别辅助问题 |

---

## 扫描结果参考

| 子系统 | 扫描文件数 | 发现问题数 | 扫描时间 |
|--------|-----------|-----------|----------|
| web | 1,576 | 50 | ~2分钟 |
| arkui | 17,362 | 148 | ~5分钟 |
| ability | 957 | 68 | ~30秒 |
| communication | 175 | 6 | ~15秒 |

误报改进（web目录）：
- v1: ~8,000 → v2: 4,590 → v3旧版: 835 → **v3新版: 50**（总体减少 99.4%）

---

## 错误/正确示例

> 来源: 规则内置示例（原 docs/EXAMPLES.md，已迁移）

### 修复建议格式示例

**重要**: 修复建议必须明确指出哪个分支缺少断言，以及具体的行号，让用户清楚知道问题所在。

**示例1：try块缺少断言**

**代码**:
```typescript
it('systemAppTest_0400', Level.LEVEL0, async (done: Function) => {
  console.info('systemAppTest_0400 START');
  try {
    app.requestFullWindow({      // 第89行：try块开始
      duration: 2000
    });
    // ❌ try块没有断言
    done();
  } catch (err) {
    console.log("systemAppTest_0400 error: " + err);
    expect(err.code).assertEqual(401);  // ✓ catch块有断言
    done();
  }
});
```

**修复建议（正确格式）**:
```
测试用例缺少断言。检测到try-catch结构，try块（第89行）缺少断言。
请确保try和catch的每个分支都包含断言方法。

修复建议：
1. 在try块中添加断言，验证requestFullWindow调用成功
2. 示例：expect(result).toBeDefined() 或 expect(true).assertTrue()
```

**示例2：catch块缺少断言**

**代码**:
```typescript
it('systemAppTest_0500', Level.LEVEL0, async (done: Function) => {
  console.info('systemAppTest_0500 START');
  try {
    let result = await someAsyncFunction();
    expect(result).assertEqual('success');  // ✓ try块有断言
    done();
  } catch (err) {                // 第95行：catch块开始
    console.log("systemAppTest_0500 error: " + err);
    // ❌ catch块没有断言
    done();
  }
});
```

**修复建议（正确格式）**:
```
测试用例缺少断言。检测到try-catch结构，catch块（第95行）缺少断言。
请确保try和catch的每个分支都包含断言方法。

修复建议：
1. 在catch块中添加断言，验证错误处理逻辑
2. 示例：expect(err.code).assertEqual(401) 或 expect(err.message).toBeDefined()
```

**示例3：try和catch块都缺少断言**

**代码**:
```typescript
it('systemAppTest_0600', Level.LEVEL0, async (done: Function) => {
  console.info('systemAppTest_0600 START');
  try {                           // 第101行：try块开始
    await someAsyncFunction();
    // ❌ try块没有断言
    done();
  } catch (err) {                 // 第105行：catch块开始
    console.log("systemAppTest_0600 error: " + err);
    // ❌ catch块没有断言
    done();
  }
});
```

**修复建议（正确格式）**:
```
测试用例缺少断言。检测到try-catch结构，try块（第101行）和catch块（第105行）都缺少断言。
请确保try和catch的每个分支都包含断言方法。

修复建议：
1. 在try块中添加断言，验证正常流程
   示例：expect(result).toBeDefined() 或 expect(true).assertTrue()
2. 在catch块中添加断言，验证错误处理
   示例：expect(err.code).toBeDefined() 或 expect(err.message).toContain('error')
```

**示例4：finally块缺少断言**

**代码**:
```typescript
it('systemAppTest_0700', Level.LEVEL0, async (done: Function) => {
  try {
    let result = await someAsyncFunction();
    expect(result).assertEqual('success');  // ✓ try块有断言
  } catch (err) {
    expect(err.code).assertEqual(401);      // ✓ catch块有断言
  } finally {                               // 第112行：finally块开始
    let cleanupResult = cleanup();
    // ❌ finally块有业务逻辑但没有断言
    done();
  }
});
```

**修复建议（正确格式）**:
```
测试用例缺少断言。检测到try-catch-finally结构，finally块（第112行）包含业务逻辑但缺少断言。
请确保try、catch和finally的每个分支都包含断言方法。

修复建议：
1. finally块中调用了cleanup()函数，应该验证清理结果
   示例：expect(cleanupResult).assertEqual('success')
2. 如果finally块只包含done()等清理语句，可以不需要断言
```

**示例5：无try-catch结构的用例**

**代码**:
```typescript
it('systemAppTest_0800', Level.LEVEL0, async (done: Function) => {
  console.info('systemAppTest_0800 START');
  let result = await someAsyncFunction();
  // ❌ 没有断言
  done();
});
```

**修复建议（正确格式）**:
```
测试用例缺少断言。请在it()块中添加expect或assert*断言方法，验证测试结果。

修复建议：
1. 添加断言验证someAsyncFunction的返回值
   示例：expect(result).toBeDefined() 或 expect(result).assertEqual('expected')
2. 确保测试用例验证了关键业务逻辑
```

**Excel报告格式要求**:

| 列序 | 列名 | 示例内容 |
|------|------|---------|
| 1 | 问题ID | R004 |
| 2 | 问题类型 | 测试用例缺少断言 |
| 3 | 严重级别 | Critical |
| 4 | 文件路径 | web/DFX/log_dotting/entry/src/ohosTest/ets/test/WebInitTest.test.ets |
| 5 | 行号 | 87 |
| 6 | 代码片段 | it('systemAppTest_0400', ...) 缺少断言 |
| 7 | 修复建议 | 测试用例缺少断言。检测到try-catch结构，try块（第89行）和catch块（第93行）都缺少断言。请确保try和catch的每个分支都包含断言方法。 |

### 辅助函数try-catch断言缺陷检测示例

**场景**: `it()`通过调用辅助函数获得断言覆盖（不触发R004 Critical），但辅助函数内部存在try-catch断言缺陷。

**示例1：辅助函数catch块缺少断言（Warning级别）**

**测试文件** (OhAVRecorderNDKMp3Test.test.ets):
```typescript
it('testOhAvRecorder_mp3_success_0010', Level.LEVEL0, async (done: Function) => {
    let fileName: string = avRecorderNdkTestBase.resourceMP3Name();
    fdObject = await avRecorderNdkTestBase.getFd(fileName);
    fdPath = "fd://" + fdObject.fdNumber;
    let config: ESObject = { fdNumber: fdObject.fdNumber, ... };
    let mySteps: Array<string> = [
        avRecorderNdkTestBase.CREATE_PREPARE_RECORDER_EVENT,
        avRecorderNdkTestBase.PREPARE_RECORDER_EVENT,
        avRecorderNdkTestBase.START_RECORDER_EVENT,
        avRecorderNdkTestBase.STOP_RECORDER_EVENT,
        avRecorderNdkTestBase.RELEASE_RECORDER_EVENT,
        avRecorderNdkTestBase.END_EVENT
    ];
    await avRecorderNdkTestBase.toNextStep(config, fdPath, mySteps, done);
    // ✓ toNextStep内部有expect()，R004 Critical不触发
});
```

**辅助函数** (AVRecorderNdkTestBase.ets):
```typescript
async toNextStep(config: ESObject, fdNumber: string,
    steps: Array<string>, done: Function) {
    try {
        switch (currentSteps) {
            case this.CREATE_PREPARE_RECORDER_EVENT:
                this.result = await testNapi.createPrepareAVRecorder();
                expect(this.result).assertEqual(0);  // ✓ 有效断言
                this.toNextStep(config, fdNumber, steps, done);
                break;
        }
    } catch (error) {                    // 第248行
        console.log('toNextStep error', error);  // ❌ catch块无断言
        done();
    }
}
```

**扫描结果（Warning级别）**:
```
[R004] OhAVRecorderNDKMp3Test.test.ets:91
代码: it('testOhAvRecorder_mp3_success_0010', ...)
建议: 调用的辅助函数存在try-catch断言缺陷。
      函数 toNextStep 的catch块（第248行）缺少断言。
      请确保所有分支都包含断言方法。
```

**示例2：辅助函数中注释掉的断言（Warning级别）**

**辅助函数** (AVRecorderNdkTestBase.ets):
```typescript
async toNextStep(config: ESObject, fdNumber: string,
    steps: Array<string>, done: Function) {
    try {
        switch (currentSteps) {
            case this.PREPARE_CAMERA_EVENT:
                this.previewId = await AppStorage.get('testsurfaceId');
                this.result = await testNapi.prepareCamera(this.previewId, ...);
                // expect(this.result).assertEqual(6);  // ❌ 第118行：注释掉的断言
                this.toNextStep(config, fdNumber, steps, done);
                break;
        }
    } catch (error) { ... }
}
```

**扫描结果（Warning级别）**:
```
[R004] OhAVRecorderNDKMp3Test.test.ets:91
建议: 调用的辅助函数存在try-catch断言缺陷。
      函数 toNextStep 的第118行存在注释掉的断言；
      函数 toNextStep 的catch块（第248行）缺少断言。
      请确保所有分支都包含断言方法。
```

**示例3：`} catch {` 同行模式（switch + try-catch）**

**修复前（catch块未被识别）**:
```typescript
try {
    switch (mode) {
        case 'A': doA(); break;
        default: break;
    }                         // switch的}
} catch (error) {             // try的} + catch的{ 在同一行
    console.log(error);       // ❌ 旧版扫描器无法检测此catch块
}
```

**修复后（catch块被正确识别）**:
- 扫描器优先检查`\}\s*catch\s*`模式，遇到时直接标记try结束和catch开始
- catch块中的断言缺陷被正确检测并报告

---

## 实现细节

> 来源: 规则内置实现细节（原 docs/IMPLEMENTATION_DETAILS.md，已迁移）

### 误报案例分析

**典型误报案例**：
- **文件**: `arkui/ace_ets_module_noui/ace_ets_module_global/ace_ets_module_global_api11/entry/src/main/ets/test/BasicTest/BasicJsunit.test.ets`
- **误报**: 扫描报告显示第33行 `it('testBasic01', ...)` 缺少断言
- **实际情况**: 断言通过函数封装调用链存在，不应报告为问题

**完整代码结构**:
```typescript
import { describe, beforeAll, beforeEach, afterEach, afterAll, it, Level, expect } from "@ohos/hypium";

// 第16行：封装函数定义
function callbackTest(callback: Callback<void>): void {
  callback();  // 第17行：调用回调函数
}

export default function basicJsunit() {
  describe('basicTest', () => {
    // 第21-24行：回调函数定义（包含断言）
    let callback: Callback<void> = (data: ESObject) => {
      console.log(data);
      expect(true).assertTrue();  // 第23行：断言存在
    }
    
    it('testBasic01', Level.LEVEL0, async (done: Function) => {
      console.info('[testBasic01] START');
      callbackTest(callback);  // 第35行：调用封装函数 -> callback -> expect()
      console.info('[testBasic01] END');
      done();
    });
  });
}
```

**调用链分析**:
```
it('testBasic01', ...)  // 第33行
  └─> callbackTest(callback)  // 第35行
       └─> callback()  // 第17行（在callbackTest函数定义内）
            └─> expect(true).assertTrue()  // 第23行（在callback函数定义内）
```

**误报原因**:
- 静态分析工具只检查了 `it()` 回调的直接作用域
- 未追踪通过函数封装调用的断言
- 未分析函数调用链和回调函数的执行路径

**正确检测逻辑**:
1. 收集文件中所有函数定义（包括箭头函数、函数表达式）
2. 当 `it()` 块中调用某个函数时，递归检查该函数体
3. 如果函数接受回调参数，追踪回调函数的定义
4. 检查回调函数体内是否包含断言
5. 最大递归深度限制为5层，防止无限循环

### has_business_logic 工具函数

```python
def has_business_logic(code):
    """
    判断代码是否包含业务逻辑（排除只有done()或console.log的情况）
    """
    stripped = code.strip()
    
    if re.match(r'^\s*done\s*\(\s*\)\s*;?\s*$', stripped):
        return False
    
    if re.match(r'^\s*console\.\w+\([^)]*\)\s*;?\s*$', stripped):
        return False
    
    return True
```

---

## 技术挑战与解决方案

> 来源: 规则内置升级指南（原 docs/V3_UPGRADE_GUIDE.md，已迁移）

### R004专用扫描脚本

```
/home/xianf/copy/xts_acts/scan_r004_v3_generic.py
```

**特性**:
- 支持跨文件函数引用检测
- 支持try-catch断言检测
- 支持函数封装断言检测
- 支持辅助函数try-catch断言缺陷检测（Warning级别）
- 支持注释掉断言识别
- 支持`} catch {`同行模式（switch + try-catch）
- 通用版本，可扫描任意目录
- 误报率低（web目录误报减少99.4%）

### R004扫描结果统计

**R004问题分类（2026-03-27最新）**:
- **Critical**: 2,442个（测试用例缺少断言）
- **Warning**: 939个（辅助函数try-catch断言缺陷，新增）
- **总计**: 3,381个

**Warning问题Top函数**（按出现次数排序）:

| 辅助函数 | 出现次数 | 典型缺陷 |
|---------|---------|---------|
| waitAndClickComponent | 2,662 | catch块缺少断言 |
| ExpectTrue | 1,292 | try/catch块缺少断言 |
| emitEvent | 895 | try/catch块缺少断言 |
| ExpectFail | 526 | try/catch块缺少断言 |
| callBack | 517 | try/catch块缺少断言 |
| toNextStep | 89 | catch块缺少断言、注释断言 |
