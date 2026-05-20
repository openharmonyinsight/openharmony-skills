# 类

## class Form

```cangjie
public class Form {
    public init()
    public init(queryComponent: String)
}
```

功能：[Form](url_package_classes.md#class-form) 以 key-value 键值对形式存储 http 请求的表单信息，通常为请求 [URL](url_package_classes.md#class-url) 中的 query 部分。

同一个 key 可以对应多个 value，value 以数组形式存储。`&` 符号分隔多个键值对；`=` 分隔的左侧作为 key 值，右侧作为 value 值（没有 `=` 或者 value 为空，均是允许的）。使用示例见 [Form 的构造使用](../url_samples/form.md)。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [Form](url_package_classes.md#class-form) 实例。

### init(String)

```cangjie
public init(queryComponent: String)
```

功能：根据 [URL](url_package_classes.md#class-url) 编码的查询字符串，即 [URL](url_package_classes.md#class-url) 实例的 query 部分构造 [Form](url_package_classes.md#class-form) 实例。

解析 [URL](url_package_classes.md#class-url) 编码的查询字符串，得到若干键值对，并将其添加到新构造的 [Form](url_package_classes.md#class-form) 实例中。

参数：

- queryComponent: String - [URL](url_package_classes.md#class-url) 的 query 组件部分的字符串，但是不包括组件前面的 `?` 符号。

异常：

- IllegalArgumentException - 当[URL](url_package_classes.md#class-url) 字符串中包含不符合 utf8 编码规则的字节时，抛出异常。
- [UrlSyntaxException](url_package_exceptions.md#class-urlsyntaxexception) - 当 [URL](url_package_classes.md#class-url) 字符串中包含非法转义字符时，抛出异常。

### func add(String, String)

```cangjie
public func add(key: String, value: String): Unit
```

功能：新增 key-value 映射，如果 key 已存在，则将 value 添加到原来 value 数组的最后面。

参数：

- key: String - 指定键，可以是新增的。
- value: String - 将该值添加到指定键对应的值数组中。

### func clone()

```cangjie
public func clone(): Form
```

功能：克隆 [Form](url_package_classes.md#class-form)。

返回值：

- [Form](url_package_classes.md#class-form) - 克隆得到的新 [Form](url_package_classes.md#class-form) 实例。

### func get(String)

```cangjie
public func get(key: String): Option<String>
```

功能：根据 key 获取第一个对应的 value 值。

举例：

- 当 query 组件部分是 `a=b` 时，`form.get("a")`获得 `Some(b)`。
- 当 query 组件部分是 `a=` 时，`form.get("a")`获得 `Some()`。
- 当 query 组件部分是 `a` 时，`form.get("a")`获得 `Some()`。
- 当 query 组件部分是 `a` 时，`form.get("c")`获得 `None`。

参数：

- key: String - 指定键。

返回值：

- Option\<String> - 根据指定键获取的第一个值，用 Option\<String> 类型表示。

### func getAll(String)

```cangjie
public func getAll(key: String): ArrayList<String>
```

功能：根据指定的键（key）获取该键（key）对应的所有 value 值。

参数：

- key: String - 用户指定的键（key），用于获取对应的 value 值。

返回值：

- ArrayList\<String> - 根据指定键（key）获取的全部 value 值对应的数组。当指定键（key）不存在时，返回空数组。

### func isEmpty()

```cangjie
public func isEmpty(): Bool
```

功能：判断 [Form](url_package_classes.md#class-form) 是否为空。

返回值：

- Bool - 如果为空，则返回 true；否则，返回 false。

### func remove(String)

```cangjie
public func remove(key: String): Unit
```

功能：删除 key 及其对应 value。

参数：

- key: String - 需要删除的键。

### func set(String, String)

```cangjie
public func set(key: String, value: String): Unit
```

功能：重置指定 key 对应的 value。

参数：

- key: String - 指定键。
- value: String - 将指定键的值设置为 value。

### func toEncodeString()

```cangjie
public func toEncodeString(): String
```

功能：对表单中的键值对进行编码，编码采用百分号编码。

未保留字符不会被编码，空格将编码为 '+'。

> **说明：**
>
> RFC 3986 协议中对未保留字符定义如下： unreserved = ALPHA / DIGIT / "-" / "." / "_" / "~"

返回值：

- String - 编码后的字符串。

## class URL

```cangjie
public class URL <: ToString {
    public init(scheme!: String, hostName!: String, path!: String)
}
```

功能：该类提供解析 [URL](url_package_classes.md#class-url) 的函数以及其他相关函数。

字符串中被百分号`%`编码的内容会被解码，保存在相应的组件之中，而初始值保存在相应的 `raw` 属性之中。[URL](url_package_classes.md#class-url) 中的用户名和密码部分（如果存在的话）也会按照 RFC 3986 协议的说明被解析。

> **注意：**
>
> RFC 3986 明确说明在任何场景下，明文保存用户信息存在被泄露风险，所以建议不要在 URL 中明文保存用户信息。

父类型：

- ToString

### prop fragment

```cangjie
public prop fragment: ?String
```

功能：获取解码后的锚点组件，用字符串表示。

类型：?String

### prop host

```cangjie
public prop host: String
```

功能：获取解码后的主机名和端口部分，用字符串表示。

类型：String

### prop hostName

```cangjie
public prop hostName: String
```

功能：获取解码后的主机名，用字符串表示。

类型：String

### prop opaque

```cangjie
public prop opaque: String
```

功能：获取 [URL](url_package_classes.md#class-url) 中未被解析的部分，用字符串表示。

类型：String

示例：

```cangjie
import stdx.encoding.url.*

main () {
    let url = URL.parse("https:\\\\/example.com/foo/bar") // '\' 不是协议规定的分割符，无法被解析。
    println("url.scheme=${url.scheme}")
    println("url.host=${url.host}")
    println("url.opaque=${url.opaque}")
}
```

运行结果：

```text
url.scheme=https
url.host=
url.opaque=\\/example.com/foo/bar
```

### prop path

```cangjie
public prop path: String
```

功能：获取解码后的路径，用字符串表示。

类型：String

### prop port

```cangjie
public prop port: String
```

功能：获取端口号，用字符串表示，空字符串表示无端口号。

类型：String

### prop query

```cangjie
public prop query: ?String
```

功能：获取解码后的查询组件，用字符串表示。

类型：?String

### prop queryForm

```cangjie
public prop queryForm: Form
```

功能：获取解码后的查询组件，用 [Form](url_package_classes.md#class-form) 实例表示。

类型：[Form](url_package_classes.md#class-form)

### prop rawFragment

```cangjie
public prop rawFragment: ?String
```

功能：获取解码前的锚点组件，用字符串表示。

类型：?String

### prop rawPath

```cangjie
public prop rawPath: String
```

功能：获取解码前的路径，用字符串表示。

类型：String

### prop rawQuery

```cangjie
public prop rawQuery: ?String
```

功能：获取解码前的查询组件，用字符串表示。

类型：?String

### prop rawUserInfo

```cangjie
public prop rawUserInfo: UserInfo
```

功能：获取解码前的用户名和密码信息，用 [UserInfo](url_package_classes.md#class-userinfo) 实例表示。

类型：[UserInfo](url_package_classes.md#class-userinfo)

### prop scheme

```cangjie
public prop scheme: String
```

功能：获取 [URL](url_package_classes.md#class-url) 中协议部分，用字符串表示。

类型：String

### prop userInfo

```cangjie
public prop userInfo: UserInfo
```

功能：获取解码后的用户名和密码信息，用 [UserInfo](url_package_classes.md#class-userinfo) 实例表示。

类型：[UserInfo](url_package_classes.md#class-userinfo)

### init(String, String, String)

```cangjie
public init(scheme!: String, hostName!: String, path!: String)
```

功能：构造一个 [URL](url_package_classes.md#class-url) 实例。

构造实例时需要满足要求：

- 拥有主机名 hostName 时，需要有协议 scheme。
- 不能只存在协议 scheme。
- 存在协议和路径的情况下，路径 path 必须是绝对路径。

参数：

- scheme!: String - 协议类型。
- hostName!: String - 不包含端口号的主机名。
- path!: String - 请求资源的路径。

异常：

- [UrlSyntaxException](url_package_exceptions.md#class-urlsyntaxexception) - 当构造实例不满足要求时，抛出异常。

### static func mergePaths(String, String)

```cangjie
public static func mergePaths(basePath: String, refPath: String): String
```

功能：合并两个路径。

合并规则：将引用路径 refPath 追加到基础路径 basePath 的最后一段。如果 refPath 是绝对路径，结果就是 refPath 原本的值。如果 refPath 不是绝对路径，则将自身拼接至 basePath 最后一个 `/` 后，所有结果最终都会进行标准化（路径中的`.`字符，`..`字符，以及多个连续的 `/` 字符都会被优化）。具体行为可以参照下面示例。更详细行为参考 RFC 3986 协议。

如需合并 URL 请使用 [resolveURL](#func-resolveurlurl)。

例如：

- `/a/b/c` 合并 `/d` 输出 `/d`。
- `/a/b/c` 合并 `d` 输出 `/a/b/d`。
- `/a/b/` 合并 `d/e/../f` 输出 `/a/b/d/f`。
- `/a/b/c/` 合并 `./../../g` 输出 `/a/g`。

参数：

- basePath: String - 基础路径。
- refPath: String - 引用路径。

返回值：

- String - 合并且标准化后的路径。

### static func parse(String)

```cangjie
public static func parse(rawUrl: String): URL
```

功能：将原始 URL 字符串解析成 [URL](url_package_classes.md#class-url) 对象。

这个函数会将 [URL](url_package_classes.md#class-url) 按照组件分解，然后分别进行解码并存储在相应的组件属性中，而 rawXXX (此处泛指前缀是 raw 的 URL 属性)属性部分存储的是原始值，不做编解码处理。

使用示例请参见[URL 解析函数 parse 的使用](./../url_samples/url_parse.md)。

> **注意：**
>
> 该函数可以解析 URL 中的用户名和密码（如果存在），这是符合 RFC 3986 协议的解析功能的，但是 RFC 3986 也明确指出，任何场景下，明文保存用户信息存在被泄露风险，所以建议不要在 URL 中明文保存用户信息。

参数：

- rawUrl: String - [URL](url_package_classes.md#class-url) 字符串。

返回值：

- [URL](url_package_classes.md#class-url) - 解析字符串得到的 [URL](url_package_classes.md#class-url) 实例。

异常：

- [UrlSyntaxException](url_package_exceptions.md#class-urlsyntaxexception) - 当 [URL](url_package_classes.md#class-url) 字符串中包含非法字符时，抛出异常。
- IllegalArgumentException - 当被编码的字符不符合 `UTF-8` 的字节序列规则时，抛出异常。

### func isAbsoluteURL()

```cangjie
public func isAbsoluteURL(): Bool
```

功能：判断 [URL](url_package_classes.md#class-url) 是否为绝对 [URL](url_package_classes.md#class-url)（scheme 存在时，[URL](url_package_classes.md#class-url) 是绝对 [URL](url_package_classes.md#class-url)）。

返回值：

- Bool - scheme 存在时返回 true，不存在时返回 false。

### func replace(Option\<String>, Option\<String>, Option\<String>, Option\<String>, Option\<String>, Option\<String>, Option\<String>)

```cangjie
public func replace(scheme!: Option<String> = None, userInfo!: Option<String> = None,
 hostName!: Option<String> = None, port!: Option<String> = None, path!: Option<String> = None, 
 query!: Option<String> = None, fragment!: Option<String> = None): URL
```

功能：替换 [URL](url_package_classes.md#class-url) 对象的各组件，并且返回一个新的 [URL](url_package_classes.md#class-url) 对象。

替换时需要满足以下要求：

- 方案 scheme 为空时，主机名必须为空。
- 主机名为空时，用户信息或端口号必须为空。
- 方案 scheme 不为空时，主机名和路径不能同时为空。
- 方案 scheme 不为空时，路径必须是绝对路径。
- 任意组件均为合法字符。

参数：

- scheme!: Option\<String> - 协议组件。
- userInfo!: Option\<String> - 用户信息。
- hostName!: Option\<String> - 主机名。
- port!: Option\<String> - 端口号。
- path!: Option\<String> - 资源路径。
- query!: Option\<String> - 查询组件。
- fragment!: Option\<String> - 锚点组件。

返回值：

- [URL](url_package_classes.md#class-url) - 新的 [URL](url_package_classes.md#class-url) 对象。

异常：

- [UrlSyntaxException](url_package_exceptions.md#class-urlsyntaxexception) - 不满足替换要求时，抛出异常。

### func resolveURL(URL)

```cangjie
public func resolveURL(ref: URL): URL
```

功能：以当前 [URL](url_package_classes.md#class-url) 实例为基础 [URL](url_package_classes.md#class-url)，以传入的 [URL](url_package_classes.md#class-url) 为参考 [URL](url_package_classes.md#class-url)，根据 RFC 3986 协议生成一个新的 [URL](url_package_classes.md#class-url) 实例。

例如：<http://a/b/c/d;p?q> 为基础 [URL](url_package_classes.md#class-url)，以下 = 左边为参考 [URL](url_package_classes.md#class-url)，右边为生成的新 [URL](url_package_classes.md#class-url)：

- "g"      =  "<http://a/b/c/g>"
- "/g"     =  "<http://a/g>"
- "g?y"    =  "<http://a/b/c/g?y>"
- "g?y#s"  =  "<http://a/b/c/g?y#s>"
- "../"    =  "<http://a/b/>"

更多详细的 URL 生成规则，请参见 RFC 3968 协议。

参数：

- ref: [URL](url_package_classes.md#class-url) - 参考 [URL](url_package_classes.md#class-url) 对象。

返回值：

- [URL](url_package_classes.md#class-url) - 新的 [URL](url_package_classes.md#class-url) 实例。

### func toString()

```cangjie
public func toString(): String
```

功能：获取当前 [URL](url_package_classes.md#class-url) 实例的字符串值。

会把 hostName 编码，其余部分取 rawXXX (此处泛指前缀是 raw 的 URL 属性)属性值，按照 URL 组件构成顺序进行拼接而获得该函数返回值。

返回值：

- String - 当前 [URL](url_package_classes.md#class-url) 实例的字符串值。

## class UserInfo

```cangjie
public class UserInfo <: ToString {
    public init()
    public init(userName: String)
    public init(userName: String, passWord: String)
    public init(userName: String, passWord: Option<String>)
}
```

功能：[UserInfo](url_package_classes.md#class-userinfo) 表示 URL 中用户名和密码信息。

> **注意：**
>
> RFC 3986 明确指出，任何场景下，明文保存用户信息存在被泄露风险，所以建议不要在 URL 中明文保存用户信息。

父类型：

- ToString

### init()

```cangjie
public init()
```

功能：创建 [UserInfo](url_package_classes.md#class-userinfo) 实例。

### init(String)

```cangjie
public init(userName: String)
```

功能：根据用户名创建 [UserInfo](url_package_classes.md#class-userinfo) 实例。

参数：

- userName: String - 用户名。

### init(String, Option\<String>)

```cangjie
public init(userName: String, passWord: Option<String>)
```

功能：根据用户名和密码创建 [UserInfo](url_package_classes.md#class-userinfo) 实例。
参数：

- userName: String - 用户名。
- passWord: Option\<String> - 密码，用 Option\<String> 类型表示。

### init(String, String)

```cangjie
public init(userName: String, passWord: String)
```

功能：根据用户名和密码创建 [UserInfo](url_package_classes.md#class-userinfo) 实例。
参数：

- userName: String - 用户名。
- passWord: String - 密码。

### func password()

```cangjie
public func password(): Option<String>
```

功能：获取密码信息。

> **注意：**
>
> RFC 3986 明确指出，任何场景下，明文保存用户信息存在被泄露风险，所以建议不要在 URL 中明文保存用户信息。

返回值：

- Option\<String> - 将密码以 Option\<String> 形式返回。

### func toString()

```cangjie
public func toString(): String
```

功能：将当前 [UserInfo](url_package_classes.md#class-userinfo) 实例转换为字符串。

返回值：

- String - 当前 [UserInfo](url_package_classes.md#class-userinfo) 实例的字符串表示。

### func username()

```cangjie
public func username(): String
```

功能：获取用户名信息。

返回值：

- String - 字符串类型的用户名。
