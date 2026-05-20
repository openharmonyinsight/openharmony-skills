# 枚举

## enum JsonKind

```cangjie
public enum JsonKind {
    | JsNull
    | JsBool
    | JsInt
    | JsFloat
    | JsString
    | JsArray
    | JsObject
}
```

功能：表示 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 的具体类型。

### JsArray

```cangjie
JsArray
```

功能：表示 `JSON` 类型中的数组类型。

### JsBool

```cangjie
JsBool
```

功能：表示 `true` 或者 `false` 类型。

### JsFloat

```cangjie
JsFloat
```

功能：表示值为浮点数的 `number` 类型。

### JsInt

```cangjie
JsInt
```

功能：表示值为整数的 `number` 类型。

### JsNull

```cangjie
JsNull
```

功能：表示 `null` 类型。

### JsObject

```cangjie
JsObject
```

功能：表示 `JSON` 类型中的对象类型。

### JsString

```cangjie
JsString
```

功能：表示 `string` 类型。
