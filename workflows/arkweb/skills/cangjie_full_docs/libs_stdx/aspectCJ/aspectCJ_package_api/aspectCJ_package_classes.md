# 类

## class InsertAtEntry

```cangjie
public class InsertAtEntry {
    public const init(packageName!: String, className!: String, methodName!: String, isStatic!: Bool, funcTypeStr!: String, recursive!: Bool)
}
```

功能：在注解所指定方法的入口，织入对被注解标注的函数的调用。注解所指定的方法和被注解标注的函数，需满足[规格限制](../aspectCJ_package_overview.md#规格和使用)。

### const init(String, String, String, Bool, String, Bool)

```cangjie
public const init(packageName!: String, className!: String, methodName!: String, isStatic!: Bool, funcTypeStr!: String, recursive!: Bool)
```

功能：创建 [InsertAtEntry](aspectCJ_package_classes.md#class-insertatentry) 对象。

参数：

- packageName: String - 被织入的函数的所属包名，如 "default", "std.core"；
- className: String - 如果被织入的函数是成员函数，则为函数所属类名；如果被织入的函数是全局函数，则为空；
- methodName: String - 被织入的函数名称，如 "foo"；
- isStatic: Bool - 被织入的函数是否为静态成员函数；
- funcTypeStr: String - 被织入的函数的类型字符串，不包括空格。对于自定义类型，类型定义所在的包名不可省略，且和类型名之间使用 `.` 分隔。不需要包括隐式的 this 形参的类型。如 "(Int64,std.core.Object)->Unit"；
- recursive: Bool - 当被织入的函数是成员函数时，表示是否对子类里的函数 override 版本也做织入；否则该字段应填 false。

## class InsertAtExit

```cangjie
public class InsertAtExit {
    public const init(packageName!: String, className!: String, methodName!: String, isStatic!: Bool, funcTypeStr!: String, recursive!: Bool)
}
```

功能：在注解所指定方法的退出点，织入对被注解标注的函数的调用。注解所指定的方法和被注解标注的函数，需满足[规格限制](../aspectCJ_package_overview.md#规格和使用)。

### const init(String, String, String, Bool, String, Bool)

```cangjie
public const init(packageName!: String, className!: String, methodName!: String, isStatic!: Bool, funcTypeStr!: String, recursive!: Bool)
```

功能：创建 [InsertAtExit](aspectCJ_package_classes.md#class-insertatexit) 对象。

参数：

- packageName: String - 被织入的函数的所属包名，如 "default", "std.core"；
- className: String - 如果被织入的函数是成员函数，则为函数所属类名；如果被织入的函数是全局函数，则为空；
- methodName: String - 被织入的函数名称，如 "foo"；
- isStatic: Bool - 被织入的函数是否为静态成员函数；
- funcTypeStr: String - 被织入的函数的类型字符串，不包括空格。对于自定义类型，类型定义所在的包名不可省略，且和类型名之间使用 `.` 分隔。不需要包括隐式的 this 形参的类型。如 "(Int64,std.core.Object)->Unit"；
- recursive: Bool - 当被织入的函数是成员函数时，表示是否对子类里的函数 override 版本也做织入；否则该字段应填 false。

## class ReplaceFuncBody

```cangjie
public class ReplaceFuncBody {
    public const init(packageName!: String, className!: String, methodName!: String, isStatic!: Bool, recursive!: Bool)
}
```

功能：将注解所指定方法的方法体，替换为对被注解标注的函数的调用。注解所指定的方法和被注解标注的函数，需满足[规格限制](../aspectCJ_package_overview.md#规格和使用)。

### const init(String, String, String, Bool, Bool)

```cangjie
public const init(packageName!: String, className!: String, methodName!: String, isStatic!: Bool, recursive!: Bool)
```

功能：创建 [ReplaceFuncBody](aspectCJ_package_classes.md#class-replacefuncbody) 对象。

参数：

- packageName: String - 被织入的函数的所属包名，如 "default", "std.core"；
- className: String - 如果被织入的函数是成员函数，则为函数所属类名；如果被织入的函数是全局函数，则为空；
- methodName: String - 被织入的函数名称，如 "foo"；
- isStatic: Bool - 被织入的函数是否为静态成员函数；
- recursive: Bool - 当被织入的函数是成员函数时，表示是否对子类里的函数 override 版本也做织入；否则该字段应填 false。
