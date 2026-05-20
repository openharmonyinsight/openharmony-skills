# Evolution - 项目重难点记录

## 项目: MyApplication6
### 初始日期: 2025-02-24

## 重难点记录

### 2. Entry/Component/State 未声明
**日期**: 02-24
**现象**: `error: undeclared identifier 'Entry'`
**原因**:
1. 缺少 `ohos.arkui.state_macro_manage` 包的导入
2. 使用了 ArrayList 导致编译提前失败
**解决方案**:
1. 添加正确的导入语句
2. 按照标准格式导入
**正确语法**:
```cangjie
import ohos.arkui.state_macro_manage.Entry
import ohos.arkui.state_macro_manage.Component
import ohos.arkui.state_macro_manage.State

// 或者使用通配符
import ohos.arkui.state_macro_manage.*
```

### 3. Array 字面量初始化语法
**日期**: 02-24
**现象**: Array 初始化语法报错
**原因**: 不是标准的字面量格式
**解决方案**: 使用方括号 `[]` 包围元素
**正确语法**:
```cangjie
// 使用方括号字面量
var stockData: Array<StockData> = [
    StockData("01-15", 100.0, 0.0),
    StockData("01-16", 102.5, 2.5)
]

// 或者使用构造函数
let a = Array<Int64>(3, repeat: 0)
```

**参考文档**:
- Array 类型: `./scripts/hm-docs/syntax/source_zh_cn/basic_data_type/array.md`
- State 导入: `./scripts/hm-docs/ui-dev/arkui-cj/cj-animation-smoothing.md`

### 4. UI组件中不能使用普通for循环
**日期**: 02-24
**现象**: `error: does not meet UI component` 在 `for (datum in this.stockData)` 处
**原因**: 在 ArkUI 的 `build` 函数中，不能使用普通的 `for` 循环来生成 UI 组件。必须使用 `ForEach` UI 组件
**解决方案**: 使用 `ForEach` 组件替代 for 循环
**正确语法**:
```cangjie
// 错误 - 普通for循环不能在UI中使用
Row {
    for (datum in this.stockData) {
        Text(datum.date)
    }
}

// 正确 - 使用ForEach组件
Row {
    ForEach(this.stockData, itemGeneratorFunc: { datum: StockData, _: Int64 =>
        Text(datum.date)
    })
}
```

**ForEach 语法**:
- 参数1: 要遍历的数据源（Array）
- `itemGeneratorFunc`: lambda 函数，接收 `item`（元素）和 `index`（索引）两个参数
- 不需要 import，属于 `kit.ArkUI.*`

**参考文档**:
- ForEach: `./scripts/hm-docs/ui-dev/arkui-cj/cj-layout-development-create-list.md`

### 5. Int64 转 Float64 方法名错误
**日期**: 02-24
**现象**: `error: undeclared identifier 'toFloat64'`
**原因**: Int64 类型没有 `toFloat64()` 方法，应该使用 `toFloat()`
**解决方案**: 使用 `toFloat()` 代替 `toFloat64()`
**正确语法**:
```cangjie
// 错误
let x: Float64 = i.toFloat64() * xStep

// 正确
let x: Float64 = i.toFloat * xStep
let xStep: Float64 = width / (data.size - 1).toFloat
```

### 6. flex 属性不存在
**日期**: 02-24
**现象**: `error: 'flex' is not a member of class 'Column'`
**原因**: ArkUI 中没有 `.flex()` 方法，应该使用 `.layoutWeight()`
**解决方案**: 使用 `.layoutWeight()` 代替 `.flex()`
**正确语法**:
```cangjie
// 错误
Column().flex(1)

// 正确
Column().layoutWeight(1)
```

**参考文档**:
- layoutWeight: `./scripts/hm-docs/ui-dev/arkui-cj/cj-layout-development-linear.md`

### 7. Float64 与 Int64 比较类型不匹配
**日期**: 02-24
**现象**: `error: invalid binary operator '>=' on type 'Float64' and 'Int64'`
**原因**: 仓颉中 Float64 和 Int64 不能直接比较，需要类型转换
**解决方案**: 使用浮点数字面量进行比较
**正确语法**:
```cangjie
// 错误
if (datum.change >= 0) { ... }

// 正确
if (datum.change >= 0.0) { ... }
```

### 8. Color.LightGray 不存在
**日期**: 02-24
**现象**: `error: 'LightGray' is not a member of class 'Color'`
**原因**: Color 类型没有 LightGray 属性
**解决方案**: 使用十六进制颜色值替代
**正确语法**:
```cangjie
// 错误
.backgroundColor(Color.LightGray)

// 正确 - 使用十六进制颜色
.backgroundColor(0xF5F5F5)
```

### 9. Color.Gray200 不存在
**日期**: 02-24
**现象**: `error: 'Gray200' is not a member of class 'Color'`
**原因**: Color 类型不支持 Material Design 的颜色命名（如 Gray200）
**解决方案**: 使用十六进制颜色值替代（Gray200 ≈ 0xEEEEEE）
**正确语法**:
```cangjie
// 错误
.backgroundColor(Color.Gray200)

// 正确 - 使用十六进制颜色
.backgroundColor(0xEEEEEE)
```

### 10. Float64 与 Int64 乘法类型不匹配
**日期**: 02-24
**现象**: `error: invalid binary operator '*' on type 'Float64' and 'Int64'`
**原因**: 仓颉中 Float64 和 Int64 不能直接进行算术运算
**解决方案**: 使用浮点数字面量进行计算
**正确语法**:
```cangjie
// 错误
let step: Float64 = (maxPrice - minPrice) / 4.0
return (minPrice + step * 3).toString()

// 正确
let step: Float64 = (maxPrice - minPrice) / 4.0
return (minPrice + step * 3.0).toString()
```

### 11. divider() 方法缺少参数
**日期**: 02-24
**现象**: `error: missing argument for parameter list '(Enum-Option<Class-ListDividerOptions>)'`
**原因**: List 的 divider() 方法需要提供 ListDividerOptions 参数，不能无参调用
**解决方案**: 移除 divider() 调用或提供正确参数
**正确语法**:
```cangjie
// 错误
List() { ... }.divider()

// 正确 - 移除或提供参数
List() { ... }
// 或
List() { ... }.divider(strokeWidth: 1, color: 0xFFE0E0E0)
```

### 12. Path 折线图不可见（布局问题）
**日期**: 02-24
**现象**: Path 组件虽然有 `.layoutWeight(1)` 但折线图不可见
**原因**: 父组件 Row 设置了固定高度，导致 Path 使用 `.layoutWeight(1)` 时无法获得实际渲染高度
**解决方案**: 为 Path 设置具体的高度，或重新设计布局结构使用固定高度
**正确语法**:
```cangjie
// 错误 - layoutWeight 在固定高度的父组件中无效
Row {
    Column { ... }  // 固定高度 300
}
Path()
    .width(100.percent)
    .layoutWeight(1)  // 父组件固定高度，无法生效

// 正确 - 设置具体高度
Path()
    .width(100.percent)
    .height(220.px)
    .stroke(Color.Red)
    .strokeWidth(2)
```

---

## 项目: MyApplication8 (计算器应用)
### 初始日期: 2025-02-25

## 重难点记录

### 13. .onClick 事件语法格式错误
**日期**: 02-25
**现象**: `}) does not meet UI component` 在 Button 的链式调用中
**原因**: ArkUI 宏处理器要求 `.onClick` 必须使用多行格式，不能使用单行闭包
**解决方案**: 改为多行格式，使用类型推导而非显式类型注解
**正确语法**:
```cangjie
// 错误 - 单行格式 + 显式类型注解
Button("AC")
    .width(70.vp)
    .height(70.vp)
    ..onClick({ evt: ClickEvent => this.onButtonClicked("AC") })

// 正确 - 多行格式 + 类型推导
Button("AC")
    .width(70.vp)
    .height(70.vp)
    .onClick ({
        evt => this.onButtonClicked("AC")
    })
```

**关键点**:
1. 必须使用 `.onClick` 而不是 `..onClick`
2. 闭包参数使用类型推导 `evt =>` 而不是 `evt: ClickEvent =>`
3. 必须写成多行格式，单行会触发宏处理错误

### 14. 类型转换方法不存在
**日期**: 02-25
**现象**: `error: undeclared identifier 'toUInt32'`, `error: undeclared identifier 'toInt64'`
**原因**: 仓颉语言中类型转换使用 `T(e)` 语法，而不是 `e.toT()` 方法调用
**解决方案**: 使用类型构造函数进行转换
**正确语法**:
```cangjie
// 错误
let charValue = ch.toUInt32()
let intPart = absValue.toInt64()

// 正确
let charValue = UInt32(ch)
let intPart = Int64(absValue)
```

**支持的数值类型转换**:
- `Int64(e)`, `Int32(e)`, `Int16(e)`, `Int8(e)`
- `UInt64(e)`, `UInt32(e)`, `UInt16(e)`, `UInt8(e)`
- `Float64(e)`, `Float32(e)`, `Float16(e)`

**Rune 转换**:
```cangjie
let x: Rune = 'a'
let r1 = UInt32(x)  // Rune 到 UInt32
let r2 = Rune(65)   // Int64 到 Rune
```

### 15. String 下标返回 Byte 类型
**日期**: 02-25
**现象**: `error: invalid binary operator '==' on type 'UInt8' and 'Rune'`
**原因**: `String[Int64]` 下标访问返回 `UInt8` 类型（字节），不能直接与 `Rune` 类型字面量比较
**解决方案**: 使用 ASCII 码值或 String 方法比较
**正确语法**:
```cangjie
// 错误 - 类型不匹配
if (s[0] == r'-') { ... }
if (ch == r'.') { ... }

// 正确方案1 - 使用 ASCII 码值
if (s[0] == 45u8) { ... }  // '-' 的 ASCII 码是 45
if (ch == 46u8) { ... }     // '.' 的 ASCII 码是 46

// 正确方案2 - 使用 String 方法
if (s.startsWith("-")) { ... }
```

**常用 ASCII 码值**:
- `'-'` = 45u8
- `'.'` = 46u8
- `'0'` ~ `'9'` = 48u8 ~ 57u8

### 16. String.isEmpty 不是属性
**日期**: 02-25
**现象**: `error: expected 'Bool', found '() -> Bool'`
**原因**: String 类型没有 `isEmpty` 属性，是方法调用但通常用 `.size == 0` 代替
**解决方案**: 使用 `.size` 属性判断
**正确语法**:
```cangjie
// 错误
if (this.calcOperator.isEmpty) { ... }

// 正确
if (this.calcOperator.size == 0) { ... }
```

### 17. .padding 不支持对象语法
**日期**: 02-25
**现象**: `error: expected type name after ':', found literal '10'`
**原因**: ArkUI 的 `.padding()` 方法不支持 `{top: 10}` 这种对象语法
**解决方案**: 使用简单的 `.padding(20)` 或使用布局组合来实现不同的边距
**正确语法**:
```cangjie
// 错误 - 对象语法不支持
Text("Hello")
    .padding({top: 10, left: 20})

// 正确 - 使用统一边距
Text("Hello")
    .padding(20)

// 正确 - 使用外层容器实现不同边距
Row() {
    Column() {
        Text("历史")
        Text("结果")
    }
    .padding(20)
}
.justifyContent(FlexAlign.Center)
```

### 18. .height(100.percent) 导致子元素占满全部空间
**日期**: 02-25
**现象**: 显示区设置 `.height(100.percent)` 后，按钮区无法显示
**原因**: 子元素使用固定百分比高度会占据外层容器的全部空间，无法与兄弟元素共存
**解决方案**: 使用 `.layoutWeight()` 替代 `.height()` 进行灵活布局比例分配
**正确语法**:
```cangjie
// 错误 - 子元素使用 height(100.percent) 会占满全屏
Column() {
    Text("显示")
        .height(100.percent)  // 占满全部空间
    Column() { ... }         // 按钮区无法显示
}

// 正确 - 使用 layoutWeight 分配比例
Column() {
    Text("显示")
        .layoutWeight(2)     // 占约 28% (2/7)
    Column() { ... }
        .layoutWeight(5)     // 占约 71% (5/7)
}
```

**layoutWeight 说明**:
- 在 flex 布局（Column/Row）中分配剩余空间
- 数值越大，分配的空间越多
- 所有子元素 layoutWeight 之和决定各自占比

---

## 项目: MyApplication12 (聊天界面应用)
### 初始日期: 2026-02-27

## 重难点记录

### 19. @Component 的 build 方法只能编写 UI 组件语法
**日期**: 02-27
**现象**: `error: Only UI component syntax can be written in build method`
**原因**: ArkUI 的 `@Component` 宏要求 `build` 方法只能编写 UI 组件语法，不能包含 let 变量声明等
**解决方案**: 为不同场景创建独立的组件，或在外层计算后传入
**正确语法**:
```cangjie
// 错误 - build 中不能声明 let
@Component
class MessageBubble {
    func build() {
        let color = if ...  // 错误
        Text(...).backgroundColor(color)
    }
}

// 正确 - 创建两个组件
@Component
class MyMessageBubble {
    func build() {
        Text(...).backgroundColor(0x0A59F7)
    }
}
```

### 20. 不支持三元运算符
**日期**: 02-27
**现象**: `error: expected operator or end of expression, found ':'`
**原因**: 仓颉语言不支持 `condition ? v1 : v2` 三元运算符
**解决方案**: 使用 `if` 表达式或创建独立组件
**正确语法**:
```cangjie
// 正确 - 使用 if 表达式
.backgroundColor(if (message.isMine) { 0x0A59F7 } else { 0xFFFFFF })

// 或在 ForEach 中使用条件渲染
ListItem() {
    if (message.isMine) {
        MyMessageBubble(message: message)
    } else {
        OtherMessageBubble(message: message)
    }
}
```

### 21. Text 组件没有 maxWidth 方法
**日期**: 02-27
**现象**: `error: 'maxWidth' is not a member of class 'Text'`
**原因**: Text 组件不支持 `.maxWidth()` 方法
**解决方案**: 移除 maxWidth，让文本自然显示

### 22. 使用 spawn + sleep 实现延迟操作
**日期**: 02-27
**现象**: `error: undeclared identifier 'Timer'`
**原因**: 仓颉语言没有 JS 风格的 Timer API
**解决方案**: 使用 `spawn` 创建新线程 + `sleep()` 实现延迟
**正确语法**:
```cangjie
spawn {
    sleep(800 * Duration.millisecond)
    // 延迟后的操作
}
```

---

## 项目: MyApplication12 (AI Chat)
### 构建日期: 2026-03-02

### 1. stdx net 网络模块配置
**问题描述**: 需要使用HTTP请求与AI服务通信
**解决方案**: 
1. 解压stdx包到 `cjnative/stdx/linux_ohos_x86_64_cjnative/dynamic/stdx`
2. 在cjpm.toml中添加path-option
**正确配置**:
```toml
[target.x86_64-linux-ohos.bin-dependencies]
path-option = ["${X86_64_OHOS_LIBS}", "${X86_64_OHOS_MACRO_LIBS}", "${X86_64_OHOS_KIT_LIBS}", "C:/czc/MyApplication12/cjnative/stdx/linux_ohos_x86_64_cjnative/dynamic/stdx"]
```

### 2. List组件命名冲突
**问题描述**: `error: ambiguous use of 'List'`
**原因**: std.collection.List 和 kit.ArkUI.List 命名冲突
**解决方案**: 简化聊天UI，使用Scroll + Column代替List，避免命名冲突

### 3. @Component 中不能定义 init 构造函数
**问题描述**: `error: init constructor is not allowed in @Component class`
**解决方案**: 使用 @Prop 装饰器传递参数，不要定义 init 构造函数

### 4. String 拼接语法
**问题描述**: String += 操作报错
**解决方案**: 使用 `this.messages = this.messages + "text"` 而非 `this.messages += "text"`

### 5. HttpRequestBuilder 初始化问题
**问题描述**: stdx net 的 HttpRequestBuilder 调用方式不正确，API文档不完整
**解决方案**: 暂时简化实现，不使用实际网络请求，仅保留UI框架

### 6. stdx net HTTP API 错误用法
**日期**: 03-02
**问题描述**: chat_service.cj 编译错误
**错误详情**:
- `defer` 关键字不存在
- `response.statusCode` 属性不存在，应该是 `response.status`
- `JsonValue("string")` 构造函数语法错误
- `JsonArray.append()` 方法不存在，应该用 `add()`
- `JsonObject.toJson()` 方法不存在
- `.method("POST")` 错误，应该用 `.post()`
- `.addHeaders()` 错误，应该直接用 `.header()`

**解决方案**: 参考 AIChatLiteCzh 项目重写
**正确语法**:
```cangjie
// Client 创建
var config = TlsClientConfig()
config.verifyMode = CertificateVerifyMode.TrustAll
let client = ClientBuilder()
    .tlsConfig(config)
    .readTimeout(Duration.Max)
    .build()

// 请求构建
let request = HttpRequestBuilder()
    .url(url)
    .header('Authorization', 'Bearer ${key}')
    .header('Content-Type', 'application/json')
    .body(requestBody)
    .post()
    .build()

// 响应处理
if (response.status != 200) { ... }

// JSON 解析
let jsonVal = JsonValue.fromStr(bodyStr)
let jsonObj = jsonVal.asObject()
let content = jsonObj.getFields()['choices'].asArray()[0].asObject().getFields()['message'].asObject().getFields()['content'].asString().getValue()

// JSON 构建（使用字符串插值）
let requestBody = '''
{ "model":"${model}",
  "messages":[{"role":"user","content":"${userInput}"}],
  "stream":false }
'''
```

---

## 项目: MyApplication13 (聊天应用优化)
### 构建日期: 2026-03-03

## 重难点记录

### 23. stdx.encoding.json 依赖配置
**日期**: 03-03
**问题描述**: 在 cjpm.toml 中没有正确配置 stdx 依赖路径，导致编译错误
**解决方案**: 在 cjpm.toml 的 [target.x86_64-linux-ohos.bin-dependencies] path-option 中添加 stdx 路径
**正确配置**:
```toml
[target.x86_64-linux-ohos.bin-dependencies]
  path-option = ["${X86_64_OHOS_LIBS}", "${X86_64_OHOS_MACRO_LIBS}", "${X86_64_OHOS_KIT_LIBS}", "C:/czc/MyApplication13/cjnative/stdx/linux_ohos_x86_64_cjnative/dynamic/stdx"]
```

### 24. for-in 循环不支持动态表达式
**日期**: 03-03
**现象**: `error: cannot convert an integer literal to type '() -> Int64'`
**原因**: `for (i in 0..jsonArray.size)` 中 `jsonArray.size` 是方法调用，Range 不支持动态表达式
**解决方案**: 先将 size 的结果赋值给变量，然后在循环中使用
**正确语法**:
```cangjie
// 错误
for (i in 0..jsonArray.size) { ... }

// 正确
let count = jsonArray.size()
for (i in 0..count) { ... }
```

### 25. ##"..."## 单行字符串不支持中文标点
**日期**: 03-03
**现象**: `error: unterminated single-line string`
**原因**: ##"..."## 格式用于单行字符串，但字符串内的中文标点（如逗号）导致解析错误
**解决方案**: 使用 '''...''' 多行字符串格式
**正确语法**:
```cangjie
// 错误
let json = ##"{"name": "张三", "message": "你好!"}"##

// 正确
let json = '''{"name": "张三", "message": "你好!"}'''
```

### 26. 多行字符串必须以换行符开头
**日期**: 03-03
**现象**: `error: multi-line string must start with newline character`
**原因': '''...''' 格式要求 ''' 后必须换行
**解决方案**: 在 ''' 之后立即换行
**正确语法**:
```cangjie
// 错误
let s = '''abc'''

// 正确
let s = '''
abc
'''
```

### 27. JsonArray.size 是方法而非属性
**日期**: 03-03
**现象**: `error: mismatched types, expected 'Int64', found '() -> Int64'`
**原因**: JsonArray 的 size 是方法，需要显式调用
**解决方案**: 使用 `jsonArray.size()` 而非 `jsonArray.size`
**正确语法**:
```cangjie
// 错误
let count = jsonArray.size

// 正确
let count = jsonArray.size()
```

### 28. Array 不支持 + 操作符和 .append 方法
**日期**: 03-03
**现象**: `error: invalid binary operator '+' on type 'Struct-Array<Class-ChatItem>'`
**原因**: Array 是值类型，不支持直接连接操作和 append 方法
**解决方案**: 使用 ArrayList 动态添加元素，然后用 toArray() 转换
**正确语法**:
```cangjie
// 错误
var arr: Array<ChatItem> = []
arr = arr + [item]

// 正确
import std.collection.*
var list = ArrayList<ChatItem>()
list.add(item)
return list.toArray()
```

### 29. import 语句不能放在函数体内
**日期**: 03-03
**现象**: `error: expected expression or declaration, found keyword 'import'`
**原因**: import 语句必须在包的顶层，不能放在函数内部
**解决方案**: 将 import 语句移到文件顶部
**正确语法**:
```cangjie
// 错误
func loadData() {
    import std.collection.*
    ...
}

// 正确
import std.collection.*
import stdx.encoding.json.*

func loadData() {
    ...
}
```

### 30. 按钮样式优化
**日期**: 03-03
**问题描述**: 返回按钮需要更清晰的样式
**解决方案**: 使用带有圆角和背景色的按钮，添加合适的 padding
**正确语法**:
```cangjie
Button(ButtonOptions(shape: ButtonType.Normal, stateEffect: true)) {
    Text("← 返回")
        .fontSize(18)
}
.backgroundColor(0xFFF0F0F0)
.borderRadius(5)
.padding(left: 10, right: 10)
.onClick({
    evt =>
        this.showDetail = false
})
```

### 31. 聊天消息布局调整
**日期**: 03-03
**问题描述**: 我方消息应该在右侧，对方消息应该在左侧
**解决方案**: 根据 isSelf 属性调整 Row 内元素顺序
**正确语法**:
```cangjie
if (message.isSelf) {
    Row() {
    }
    .layoutWeight(1)  // 左侧空白
    Text("👤")       // 图标在右侧
    Column() {
        Text(message.content)
        Text(message.time)
    }
    .margin(left: 10, right: 10)
} else {
    Text("👤")       // 图标在左侧
    Column() {
        Text(message.content)
        Text(message.time)
    }
    .margin(right: 10)
    Row() {
    }
    .layoutWeight(1)  // 右侧空白
}
```

---

## 项目: MyApplication13 (微信风格聊天应用)
### 构建日期: 2026-03-03

## 重难点记录

### 32. Tabs 底部导航栏实现
**日期**: 03-03
**问题描述**: 需要实现微信风格的底部导航栏（聊天、通讯录、发现、我）
**解决方案**: 使用 Tabs 组件，设置 barPosition 为 BarPosition.End，使用 TabContent 包裹各个页面
**正确语法**:
```cangjie
Tabs(barPosition: BarPosition.End) {
    TabContent() {
        Column() {
            // 聊天列表内容
        }
    }
    .tabBar("聊天")
    
    TabContent() {
        Column() {
            Text("通讯录（暂未实现）")
        }
    }
    .tabBar("通讯录")
    
    // 其他 TabContent...
}
.width(100.percent)
.height(100.percent)
```

### 33. 搜索栏实现
**日期**: 03-03
**问题描述**: 需要在主界面顶部实现浅灰色搜索栏
**解决方案**: 使用 Row + Text 实现，设置浅灰色背景和圆角
**正确语法**:
```cangjie
Row() {
    Row() {
        Text("🔍")
            .fontSize(16)
            .fontColor(0xFF999999)
        Text("搜索")
            .fontSize(16)
            .fontColor(0xFF999999)
    }
    .width(100.percent)
    .height(36)
    .backgroundColor(0xFFF5F5F5)
    .borderRadius(8)
    .padding(left: 12)
    
    Button() {
        Text("+")
            .fontSize(24)
    }
    .backgroundColor(Color.Transparent)
}
.padding(8)
```

### 34. 聊天列表滚动实现
**日期**: 03-03
**问题描述**: 聊天列表需要支持滚动
**解决方案**: 使用 Scroll 组件包裹聊天列表 Column
**正确语法**:
```cangjie
Scroll() {
    Column() {
        ForEach(chatData, ...) {
            // 聊天列表项
        }
    }
}
.layoutWeight(1)
```

### 35. TextInput 输入框实现
**日期**: 03-03
**问题描述**: 聊天窗口底部需要实现文本输入框
**解决方案**: 使用 TextInput 组件，设置 placeholder 提示
**正确语法**:
```cangjie
Row() {
    Button() { Text("🎤") }
    TextInput(placeholder: "请输入消息...")
        .layoutWeight(1)
        .height(40)
        .backgroundColor(0xFFFFFFFF)
        .borderRadius(6)
    Button() { Text("😊") }
    Button() { Text("⊕") }
}
.height(60)
.padding(8)
```

### 36. 聊天气泡样式优化
**日期**: 03-03
**问题描述**: 需要实现微信风格的聊天气泡（白色/浅绿色）
**解决方案**: 使用 Column 包裹消息文本和时间，设置不同的背景色
**正确语法**:
```cangjie
if (message.isSelf) {
    // 我方消息 - 浅绿色
    Column() {
        Text(message.content)
            .padding(12)
            .backgroundColor(0xFF95EC69)
            .borderRadius(6)
        Text(message.time)
            .fontSize(11)
            .fontColor(0xFF999999)
    }
    .margin(left: 8)
} else {
    // 对方消息 - 白色
    Column() {
        Text(message.content)
            .padding(12)
            .backgroundColor(0xFFFFFFFF)
            .borderRadius(6)
        Text(message.time)
            .fontSize(11)
            .fontColor(0xFF999999)
    }
    .margin(right: 8)
}
```

### 37. 极简浅色风格配色
**日期**: 03-03
**问题描述**: 需要实现微信风格的极简浅色主题
**解决方案**: 使用十六进制颜色值配置浅灰色背景
**正确语法**:
```cangjie
backgroundColor(0xFFEDEDED)  // 页面背景
backgroundColor(0xFFF5F5F5)  // 搜索栏背景
backgroundColor(0xFFFFFFFA)  // 列表项背景
fontColor(0xFF000000)         // 黑色文字
fontColor(0xFF999999)         // 灰色辅助文字
```

### 38. 在条件分支中无法使用 @r 加载图片资源
**日期**: 03-03
**问题描述**: 在 ForEach 中根据条件动态加载不同图片时，编译错误 `undeclared identifier '__GenerateResource__'`
**原因**: ArkUI 资源系统在编译时生成资源引用代码，如果在 if-else 条件分支中使用 @r，宏处理器无法正确生成资源引用
**解决方案**: 
- 方案1：使用 emoji 替代图片（适用于快速原型开发）
- 方案2：将所有图片组件在顶层一次性声明，通过布局技巧控制显示（不推荐，代码复杂）
- 方案3：创建独立的 @Component 组件渲染图片（较为复杂）

**错误示例**:
```cangjie
ForEach(items, ...) {
    if (item.type == "icon1") {
        Image(@r(app.media.icon1))  // ❌ 错误：__GenerateResource__ 未声明
    } else if (item.type == "icon2") {
        Image(@r(app.media.icon2))  // ❌ 错误
    }
}
```

**正确方案（使用 emoji）**:
```cangjie
ForEach(items, ...) {
    Text(item.emoji)  // ✅ 使用 emoji 字符替代图片
        .fontSize(48)
}
```

### 39. 正确的图片资源加载方式
**日期**: 03-03
**问题描述**: 需要在ForEach中使用图片资源替代emoji
**解决方案**: 在数据模型中存储AppResource，在组件初始化时使用@r加载资源，在UI中直接使用

**关键步骤**:
1. 必须显式导入@r宏
2. 在@Component类中定义资源变量
3. 数据模型中存储AppResource
4. 通过函数传递资源进行初始化

**正确语法**:
```cangjie
// 1. 导入必要的宏
import ohos.arkui.state_macro_manage.r
import ohos.resource.*

// 2. 在EntryView组件中定义资源变量
@Entry
@Component
class EntryView {
    private let icon1: AppResource = @r(app.media.starticon1)
    private let icon2: AppResource = @r(app.media.starticon2)
    
    // 3. 在组件定义时就初始化数据（不能在build方法中用let声明变量）
    private let chatData: Array<ChatItem> = 
        loadChatData(@r(app.media.starticon1), @r(app.media.starticon2), ...)
    
    func build() {
        ForEach(this.chatData, ...) {
            Image(item.iconResource)  // 4. 直接使用存储的AppResource
                .width(48)
                .height(48)
        }
    }
}

// 5. 数据模型添加iconResource字段
public class ChatItem {
    var iconResource: AppResource
    public init(..., iconResource: AppResource) {
        this.iconResource = iconResource
    }
}

// 6. 在普通函数中接收AppResource参数（函数中不能用@r）
public func loadChatData(icon1: AppResource, icon2: AppResource, ...): Array<ChatItem> {
    var list = ArrayList<ChatItem>()
    list.add(ChatItem(..., icon1))  // 使用传入的资源
    return list.toArray()
}
```

**重要限制**:
- @r只能在@Component类中使用，不能在普通函数中使用
- build方法中不能使用let声明变量，必须在类属性中定义
- 即使是在独立组件内部，if-expr中使用@r也会报错（见Evolution.md #38）

---## 开发总结
