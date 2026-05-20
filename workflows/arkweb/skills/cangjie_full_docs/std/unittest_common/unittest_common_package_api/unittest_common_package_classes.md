# 类

## class Configuration

```cangjie
public class Configuration <: ToString {
    public init()
}
```

功能：存储 `@Configure` 宏生成的 `unittest` 配置数据的对象。[Configuration](#class-configuration) 与 [HashMap](../../collection/collection_package_api/collection_package_class.md#class-hashmapk-v-where-k--hashable--equatablek) 类似，但它的键是 [KeyFor](./unittest_common_package_interfaces.md#interface-keyfor) 类型，值为任何给定类型。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### init()

```cangjie
public init()
```

功能：构造一个空的 Configuration 实例。

### func clone()

```cangjie
public func clone(): Configuration
```

功能：拷贝一份 Configuration 对象。

返回值：

- [Configuration](#class-configuration) - 拷贝的对象。

### func get\<T>(KeyFor\<T>)

```cangjie
public func get<T>(key: KeyFor<T>): ?T
```

功能：获取 key 对应的值。

T 为 泛型参数，用于在对象中查找对应类型的值。

参数：

- key: [KeyFor](./unittest_common_package_interfaces.md#interface-keyfor) - 配置项的键值。

返回值：

- ?T - 未找到时返回 None，找到对应类型及名称的值时返回 Some\<T>(v) 。

### func getByName\<T>(String)

```cangjie
public func getByName<T>(name: String): ?T
```

功能：获取 key 对应的值。

T 为 泛型参数，用于在对象中查找对应类型的值。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 键名称。

返回值：

- ?T - 未找到时返回 None，找到对应类型及名称的值时返回 Some\<T>(v) 。

### func remove\<T>(KeyFor\<T>)

```cangjie
public func remove<T>(key: KeyFor<T>): ?T
```

功能：删除对应键名称和类型的值。

参数：

- key: [KeyFor](./unittest_common_package_interfaces.md#interface-keyfor) - 配置项的键值。

返回值：

- ?T - 当存在该值时返回该值，当不存在时返回 None。

### func removeByName\<T>(String)

```cangjie
public func removeByName<T>(name: String): ?T
```

功能：删除对应键名称和类型的值。

参数：

- key: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 键名称。

返回值：

- ?T - 当存在该值时返回该值，当不存在时返回 None。

### func set\<T>(KeyFor\<T>, T)

```cangjie
public func set<T>(key: KeyFor<T>, value: T)
```

功能：给对应键名称和类型设置值。

参数：

- key: [KeyFor](./unittest_common_package_interfaces.md#interface-keyfor) - 配置项的键值。
- value: T - 键值。

### func setByName\<T>(String, T)

```cangjie
public func setByName<T>(name: String, value: T): Unit
```

功能：给对应键名称和类型设置值。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 键名称。
- value: T - 键值。

### func toString()

```cangjie
public func toString(): String
```

功能：该对象的字符化对象，当内部对象未实现 [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring) 接口时，输出 '\<not printable>' 。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串。

### static func merge(Configuration, Configuration)

```cangjie
public static func merge(parent: Configuration, child: Configuration): Configuration
```

功能：合并 child 到 parent 配置中。其中如有同名键值 child 覆盖 parent 。

参数：

- parent: [Configuration](#class-configuration) - 需要合并的配置
- child: [Configuration](#class-configuration) - 需要合并的配置

返回值：

- [Configuration](#class-configuration) - 合并完成的配置

## class ConfigurationKey

```cangjie
abstract sealed class ConfigurationKey <: Equatable<ConfigurationKey> & Hashable {}
```

功能：配置项的键值对象。提供判等及 hashCode 方法。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[ConfigurationKey](#class-configurationkey)>
- [Hashable](../../core/core_package_api/core_package_interfaces.md#interface-hashable)

### func hashCode()

```cangjie
public override func hashCode(): Int64
```

功能：获取 hashCode 值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - hashCode 值。

### let name

```cangjie
public let name: String
```

功能：配置键值的名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### operator func ==(ConfigurationKey)

```cangjie
public override operator func ==(that: ConfigurationKey): Bool
```

功能：判等。

参数：

- that: [ConfigurationKey](#class-configurationkey) - 被对比的数据

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否相等。

### operator func !=(that: ConfigurationKey)

```cangjie
public override operator func !=(that: ConfigurationKey): Bool
```

功能：判不等。

参数：

- that: [ConfigurationKey](#class-configurationkey) - 被对比的数据

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否不相等。

### extend ConfigurationKey

```cangjie
extend ConfigurationKey {
    static func create<T>(name: String): ConfigurationKey 
}
```

#### static func create\<T>(String)

功能：创建 [ConfigurationKey](#class-configurationkey)。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 配置键值的名称。

返回值：

- [ConfigurationKey](#class-configurationkey) - 创建的配置键值。

## class PrettyPrinter

```cangjie
public abstract class PrettyPrinter {
    public PrettyPrinter(let indentationSize!: UInt64 = 4, let startingIndent!: UInt64 = 0)
}
```

功能：拥有颜色和对齐、缩进控制的打印器。

### PrettyPrinter(UInt64,UInt64)

```cangjie
public PrettyPrinter(let indentationSize!: UInt64 = 4, let startingIndent!: UInt64 = 0)
```

功能：PrettyPrinter 构造器。

参数：

- indentationSize!: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 一个缩进的空格数，默认 4 格。
- startingIndent!: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 开头的缩进个数，默认 0 个缩进。

### prop isTopLevel

```cangjie
public prop isTopLevel: Bool
```

功能：获取是否在打印的缩进顶层。

类型：Bool 。

### func append(String)

```cangjie
public func append(text: String): PrettyPrinter
```

功能：增加一个字符串到打印器中。不支持多行字符串，对多行字符串不支持缩进。

参数：

- text: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 被增加的字符串。

返回值：

- [PrettyPrinter](#class-prettyprinter) - 打印器。

### func append\<PP>(PP)where PP <: PrettyPrintable

```cangjie
public func append<PP>(value: PP): PrettyPrinter where PP <: PrettyPrintable
```

功能：增加一个实现了 [PrettyPrintable](./unittest_common_package_interfaces.md#interface-prettyprintable) 的对象到打印器中。

参数：

- value: PP - 一个实现了 [PrettyPrintable](./unittest_common_package_interfaces.md#interface-prettyprintable) 的对象。

返回值：

- [PrettyPrinter](#class-prettyprinter) - 打印器。

### func appendCentered(String, UInt64)

```cangjie
public func appendCentered(text: String, space: UInt64): PrettyPrinter
```

功能：增加一个字符串到打印器中。居中对齐至指定字符数，不足的字符由空格补齐。不支持多行字符串，对多行字符串不支持缩进。

参数：

- text: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 被增加的字符串。
- space: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 对齐的字符数量。

返回值：

- [PrettyPrinter](#class-prettyprinter) - 打印器。

### func appendLeftAligned(String, UInt64)

```cangjie
public func appendLeftAligned(text: String, space: UInt64): PrettyPrinter
```

功能：增加一个字符串到打印器中。左对齐至指定字符数，不足的字符由空格补齐。不支持多行字符串，对多行字符串不支持缩进。

参数：

- text: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 被增加的字符串。
- space: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 对齐的字符数量。

返回值：

- [PrettyPrinter](#class-prettyprinter) - 打印器。

### func appendLine(String): PrettyPrinter

```cangjie
public func appendLine(text: String): PrettyPrinter
```

功能：增加一个字符串到打印器中，跟着一个换行符。

参数：

- text: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 被增加的字符串。

返回值：

- [PrettyPrinter](#class-prettyprinter) - 打印器。

### func appendLine\<PP>(PP) where PP <: PrettyPrintable

```cangjie
public func appendLine<PP>(value: PP): PrettyPrinter where PP <: PrettyPrintable
```

功能：增加一个实现了 [PrettyPrintable](./unittest_common_package_interfaces.md#interface-prettyprintable) 的对象到打印器中，跟着一个换行符。

参数：

- value: PP - 一个实现了 [PrettyPrintable](./unittest_common_package_interfaces.md#interface-prettyprintable) 的对象。

返回值：

- [PrettyPrinter](#class-prettyprinter) - 打印器。

### func appendRightAligned(String, UInt64)

```cangjie
public func appendRightAligned(text: String, space: UInt64): PrettyPrinter
```

功能：增加一个字符串到打印器中。右对齐至指定字符数。不支持多行字符串，对多行字符串不支持缩进。

参数：

- text: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 被增加的字符串。
- space: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 对齐的字符数量。

返回值：

- [PrettyPrinter](#class-prettyprinter) - 打印器。

### func colored(Color, () -> Unit)

```cangjie
public func colored(color: Color, body: () -> Unit): PrettyPrinter
```

功能：对闭包中给打印器增加的字符串指定颜色。
常见的用法如下：

```cangjie
pp.colored(RED) {
    pp.appendLine("1")
    pp.appendLine("2")
    pp.appendLine("3")
}
```

此时字符串 "1" "2" "3" 均被打印为红色。

参数：

- color: [Color](./unittest_common_package_enums.md#enum-color) - 指定打印的颜色。
- body: () -> Unit - 添加字符串的闭包。

返回值：

- [PrettyPrinter](#class-prettyprinter) - 打印器。

### func fillLimitedSpace(Int64, () -\> Unit)

```cangjie
public open func fillLimitedSpace(spaceSize: Int64, body: () -> Unit): c
```

功能：指定大小填充代码块。

参数：

- spaceSize: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)  - 所指定的大小。
- body: () -\> body - 填充的方式。

返回值：

- [PrettyPrinter](#class-prettyprinter) - 打印器。

### func colored(Color, String)

```cangjie
public func colored(color: Color, text: String): PrettyPrinter
```

功能：对给打印器增加的字符串指定颜色。

参数：

- color: [Color](./unittest_common_package_enums.md#enum-color) - 指定打印的颜色。
- text: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 添加的字符串。

返回值：

- [PrettyPrinter](#class-prettyprinter) - 打印器。

### func customOffset(UInt64, () -> Unit)

```cangjie
public func customOffset(symbols: UInt64, body: () -> Unit): PrettyPrinter
```

功能：对闭包中给打印器增加的字符串指定额外缩进的个数。
常见的用法如下：

```cangjie
pp.customOffset(5) {
    pp.appendLine("1")
    pp.appendLine("2")
    pp.appendLine("3")
}
```

此时字符串 "1" "2" "3" 均额外缩进 5 个字符。

参数：

- symbols: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 指定缩进个数。
- body: () -> Unit - 添加字符串的闭包。

返回值：

- [PrettyPrinter](#class-prettyprinter) - 打印器。

### func indent(() -> Unit)

```cangjie
public func indent(body: () -> Unit): PrettyPrinter
```

功能：对闭包中给打印器增加的字符串指定额外缩进一次。
常见的用法如下：

```cangjie
pp.indent {
    pp.appendLine("1")
    pp.appendLine("2")
    pp.appendLine("3")
}
```

此时字符串 "1" "2" "3" 均额外缩进一次。

参数：

- body: () -> Unit - 添加字符串的闭包。

返回值：

- [PrettyPrinter](#class-prettyprinter) - 打印器。

### func indent(UInt64, () -> Unit)

```cangjie
public func indent(indents: UInt64, body: () -> Unit): PrettyPrinter
```

功能：对闭包中给打印器增加的字符串指定额外缩进指定次数。
常见的用法如下：

```cangjie
pp.indent(2) {
    pp.appendLine("1")
    pp.appendLine("2")
    pp.appendLine("3")
}
```

此时字符串 "1" "2" "3" 均额外缩进 2 次。

参数：

- indents: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 指定额外缩进的次数。
- body: () -> Unit - 添加字符串的闭包。

返回值：

- [PrettyPrinter](#class-prettyprinter) - 打印器。

### func newLine()

```cangjie
public func newLine(): PrettyPrinter
```

功能：增加新行。

返回值：

- [PrettyPrinter](#class-prettyprinter) - 打印器。

### func put(String)

```cangjie
protected func put(s: String): Unit
```

功能：打印字符串。

参数：

- s: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 需打印的字符串。

### func putNewLine()

```cangjie
protected open func putNewLine(): Unit
```

功能：打印新行。

### func setColor(Color)

```cangjie
protected func setColor(color: Color): Unit
```

功能：设置颜色。

参数：

- color: [Color](./unittest_common_package_enums.md#enum-color) - 指定的颜色。

## class PrettyText

```cangjie
public class PrettyText <: PrettyPrinter & PrettyPrintable & ToString {
    public init()
    public init(string: String)
}
```

功能：存储打印的输出。主要用途是中间存储和传递这些值。

实现了 [PrettyPrinter](#class-prettyprinter)（可以打印到）和 [PrettyPrintable](./unittest_common_package_interfaces.md#interface-prettyprintable)（可以从中打印）的方法。

父类型：

- [PrettyPrinter](#class-prettyprinter)
- [PrettyPrintable](unittest_common_package_interfaces.md#interface-prettyprintable)
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### init()

```cangjie
public init()
```

功能：默认构造器，生成一个空的对象。

### init(String)

```cangjie
public init(string: String)
```

功能：构造器，生成一个以入参开头的文本构造器。

参数：

- string: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 希望放入打印文本开头的字符串。

### func isEmpty()

```cangjie
public func isEmpty(): Bool
```

功能：返回当前构造器是否为空，即未有值传入给构造器。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 未有内容传入时返回 `true` ，否则返回 `false` 。

### func pprint(PrettyPrinter)

```cangjie
public func pprint(to: PrettyPrinter): PrettyPrinter
```

功能：打印信息到打印器上。

参数：

- to: [PrettyPrinter](#class-prettyprinter) - 打印器。

返回值：

- [PrettyPrinter](#class-prettyprinter) - 打印器。

### func toString()

```cangjie
public func toString(): String
```

功能：打印文本到字符串上。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 打印文本的字符串。

### static func of\<PP>(PP)

```cangjie
public static func of<PP>(pp: PP): PrettyText where PP <: PrettyPrintable
```

功能：通过打印从 [PrettyPrintable](./unittest_common_package_interfaces.md#interface-prettyprintable) 创建 [PrettyText](#class-prettytext)。

参数：

- pp: PP  - 一个实现了 [PrettyPrintable](./unittest_common_package_interfaces.md#interface-prettyprintable) 的类型。

返回值：

- [PrettyText](#class-prettytext) - 打印文本对象。
