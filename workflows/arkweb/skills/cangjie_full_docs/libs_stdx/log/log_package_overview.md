# stdx.log

## 功能介绍

log 包提供了一个单一的日志 API，它抽象了实际的日志实现。

## API 列表

### 函数

| 函数名                                                       | 功能                 |
| ------------------------------------------------------------ | -------------------- |
| [getGlobalLogger(Array\<Attr>)](./log_package_api/log_package_funcs.md#func-getgloballoggerarrayattr) | 获取全局 Logger 对象。 |
| [setGlobalLogger(Logger)](./log_package_api/log_package_funcs.md#func-setgloballoggerlogger) | 设置全局 Logger 对象。 |

### 类型别名

|           类型别名          |           功能           |
| --------------------------- | ------------------------ |
| [Attr](./log_package_api/log_package_types.md#type-attr) | 日志消息的键值对类型，是 (String, [LogValue](./log_package_api/log_package_interfaces.md#interface-logvalue)) 的类型别名。 |

### 接口

|              接口名          |           功能           |
| --------------------------- | ------------------------ |
| [LogValue](./log_package_api/log_package_interfaces.md#interface-logvalue) | 为仓颉数据类型提供序列化到日志输出目标的接口。 |

### 类

|              类名          |           功能           |
| --------------------------- | ------------------------ |
| [Logger](./log_package_api/log_package_classes.md#class-logger) | 此抽象类提供基础的日志打印和管理功能。 |
| [LogRecord](./log_package_api/log_package_classes.md#class-logrecord) | 日志消息的“负载”。 |
| [LogWriter](./log_package_api/log_package_classes.md#class-logwriter) | [LogWriter](./log_package_api/log_package_classes.md#class-logwriter) 提供了将仓颉数据类型序列化到日志输出目标的能力。 |
| [NoopLogger](./log_package_api/log_package_classes.md#class-nooplogger) | [Logger](./log_package_api/log_package_classes.md#class-logger) 的 NO-OP（无操作）实现。 |

### 结构体

| 结构体名                                                     | 功能                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [LogLevel](./log_package_api/log_package_structs.md#struct-loglevel) | [LogLevel](./log_package_api/log_package_structs.md#struct-loglevel) 为日志级别结构体。 |

### 异常类

| 异常类名                                                     | 功能                      |
| ------------------------------------------------------------ | ------------------------- |
| [LogException](./log_package_api/log_package_exceptions.md#class-logexception) | 用于处理 log 相关的异常。 |
