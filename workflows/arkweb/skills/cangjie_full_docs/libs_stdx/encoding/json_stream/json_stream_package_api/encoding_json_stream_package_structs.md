# 结构体

## struct WriteConfig

```cangjie
public struct WriteConfig {
    public static let compact: WriteConfig
    public static let pretty: WriteConfig
}
```

功能：用于表示 [JsonWriter](./encoding_json_stream_package_classes.md#class-jsonwriter) 的序列化格式配置。

示例：

使用示例见 [WriteConfig 使用示例](../json_stream_samples/sample_json_writeconfig.md)。

### static let compact

```cangjie
public static let compact: WriteConfig
```

功能：提供紧凑的序列化格式。

> **说明：**
>
> compact 的各属性值为：
>
> - newline: ""，空字符串。
> - indent: ""，空字符串。
> - useSpaceAfterSeparators: false。
> - htmlSafe: false。
> - dateTimeFormat: DateTimeFormat.RFC3339。

类型：[WriteConfig](#struct-writeconfig)

示例：

```text
{"Name":"zhangsan","Age":18,"Scores":[88.8,99.9],"Class":{"Name":"Class A","Students Number":33}}
```

### static let pretty

```cangjie
public static let pretty: WriteConfig
```

功能：提供整洁的序列化格式。

> **说明：**
>
> pretty 的各属性值为：
>
> - newline: "\n"。
> - indent: "&emsp;&emsp;&emsp;&emsp;"，包含 4 个空格的字符串。
> - useSpaceAfterSeparators: true。
> - htmlSafe: false。
> - dateTimeFormat: DateTimeFormat.RFC3339。

类型：[WriteConfig](#struct-writeconfig)

示例：

```text
{
    "Name": "zhangsan",
    "Age": 18,
    "Scores": [
        88.8,
        99.9
    ],
    "Class": {
        "Name": "Class A",
        "Students Number": 33
    }
}
```

### prop dateTimeFormat

```cangjie
public mut prop dateTimeFormat: String
```

功能：用于序列化 DateTime 类型时的格式控制，功能与 DateTime 的 func toString(DateTimeFormat) 一致。

类型：String

### prop htmlSafe

```cangjie
public mut prop htmlSafe: Bool
```

功能：用于表示是否转义 HTML 字符 `<`、`>`、`&`、`=`和`'`。

该值为 true 时，会将 HTML 字符转义为对应的 Unicode 编码的字符串。

该选项只对 json value 中的字符串字面量有效。

类型：Bool

### prop indent

```cangjie
public mut prop indent: String
```

功能：用于表示序列化时每个缩进级别填入的缩进字符串。取值应匹配正则 `^[ \t]*$`。

当上述的换行起作用时，该值会作为换行后的填充符。

类型：String

异常：

- IllegalArgumentException - 设置的字符串包含 ' ' 或者 '\t' 以外的字符。

### prop newline

```cangjie
public mut prop newline: String
```

功能：用于表示序列化时填入的换行符。取值应匹配正则 `^[\r\n]*$` 。

当该值不为空字符串且合法时，JsonWriter 调用 startObject 和 startArray 操作、插入元素、以及它们的结束操作会产生新的换行。

当该值为空字符串时，不会触发换行。

类型：String

异常：

- IllegalArgumentException - 设置的字符串包含 '\r' 或者 '\n' 以外的字符。

### prop useSpaceAfterSeparators

```cangjie
public mut prop useSpaceAfterSeparators: Bool
```

功能：用于表示序列化时在 ':' 和 ',' 后是否加一个空格。

该值为 true 时，每插入一个 field name 或者 array 元素后会自动写入一个空格。

该选项只对 json Object 中的 field 以及 json Array 中的元素有效。

类型：Bool
