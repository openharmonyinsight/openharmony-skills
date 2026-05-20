# 枚举

## enum SeekPosition

```cangjie
public enum SeekPosition {
    | Begin(Int64)
    | Current(Int64)
    | End(Int64)
}
```

功能：该枚举类型表示光标在文件中的位置。

### Begin(Int64)

```cangjie
Begin(Int64)
```

功能：表示从起点开始移动指定的长度。

### Current(Int64)

```cangjie
Current(Int64)
```

功能：表示从当前位置开始移动指定的长度。

### End(Int64)

```cangjie
End(Int64)
```

功能：表示从末尾开始移动指定的长度。
