# 函数

## func getGlobalLogger(Array\<Attr>)

```cangjie
public func getGlobalLogger(attrs: Array<Attr>): Logger
```

功能：获取 [Logger](log_package_classes.md#class-logger) 对象。

> **说明：**
>
> 如果未传入 attrs 参数，那么获取的是同一个 [Logger](log_package_classes.md#class-logger) 对象，传入了 attrs 参数，则创建一个包含指定的属性的  [Logger](log_package_classes.md#class-logger) 对象副本。

参数：

- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对属性，获取的 [Logger](log_package_classes.md#class-logger) 对象会包含这些属性。

返回值：

- [Logger](log_package_classes.md#class-logger) - [Logger](log_package_classes.md#class-logger) 类的对象实例。

## func setGlobalLogger(Logger)

```cangjie
public func setGlobalLogger(logger: Logger): Unit
```

功能：设置全局 [Logger](log_package_classes.md#class-logger) 对象。

> **注意：**
>
> - 此函数在程序的生命周期中只应该被调用一次。对 setGlobalLogger 的调用完成之前发生的任何日志事件都将被忽略。
> - 此函数通常不需要手动调用。日志实现提供者应提供包含了调用本方法的的初始化方法。

参数：

- logger: [Logger](log_package_classes.md#class-logger) - 实现了 [Logger](log_package_classes.md#class-logger) 类的对象实例。
