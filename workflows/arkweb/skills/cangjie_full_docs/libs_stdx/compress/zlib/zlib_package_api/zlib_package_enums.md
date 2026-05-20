# 枚举

## enum CompressLevel

```cangjie
public enum CompressLevel {
    | BestCompression
    | BestSpeed
    | DefaultCompression
}
```

功能：压缩等级。

压缩等级决定了压缩率和压缩速度，目前支持三种压缩等级，压缩率由小到大，压缩速度由快到慢依次为：BestSpeed、DefaultCompression、BestCompression。

### BestCompression

```cangjie
BestCompression
```

功能：构造一个压缩率优先的压缩等级枚举实例，表示压缩率最高，压缩速度相对降低。

### BestSpeed

```cangjie
BestSpeed
```

功能：构造一个压缩速度优先的压缩等级枚举实例，表示压缩速度最快，压缩率相对较低。

### DefaultCompression

```cangjie
DefaultCompression
```

功能：构造一个压缩等级枚举实例，表示默认压缩等级。

## enum WrapType

```cangjie
public enum WrapType {
    | DeflateFormat
    | GzipFormat
}
```

功能：压缩数据格式。

目前支持 DeflateFormat 和 GzipFormat 两种格式。

### DeflateFormat

```cangjie
DeflateFormat
```

功能：构造一个表示 `Deflate` 压缩数据格式的枚举实例。

### GzipFormat

```cangjie
GzipFormat
```

功能：构造一个表示 `Gzip` 压缩数据格式的枚举实例。
