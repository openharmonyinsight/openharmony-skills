# 日志打印示例

下面是使用 [JsonLogger](../logger_package_api/logger_package_classes.md#class-jsonlogger) 日志打印示例代码：

<!-- compile -->

```cangjie
import std.time.*
import std.io.{OutputStream, ByteBuffer, BufferedOutputStream}
import std.env.*
import std.fs.*
import std.collection.{HashMap, ArrayList}
import stdx.encoding.json.stream.*
import stdx.log.*
import stdx.logger.*

main() {
    let o = ByteBuffer()
    let bo = BufferedOutputStream<OutputStream>(getStdOut())
    let tl = JsonLogger(bo)
    tl.level = LogLevel.TRACE
    setGlobalLogger(tl)
    let logger = getGlobalLogger([("name", "main")])
    let futs = ArrayList<Future<Unit>>()

    for (_ in 0..1) {
        let f = spawn {
            =>
            logger.info("abc", ("age", 2))
            let user = User()
            // 记录诊断日志，如果 DEBUG 级别未开启，直接返回，几乎无 cost
            logger.debug("Logging in user ${user.name} with birthday ${user.birthdayCalendar}")
            // 普通记录信息日志
            logger.info("Hello, World!", ("k1", [[1, 4], [2, 5], [3]]), ("password", "v22222"))

            // lazy 方式记录耗时日志数据
            logger.log(LogLevel.ERROR, "long-running operation msg", ("k1", 100), ("k2", user.birthdayCalendar),
                ("oper", ToStringWrapper({=> "Some long-running operation returned"})))

            logger.log(LogLevel.ERROR, "long-running operation msg", ("sourcePackage", @sourcePackage()),
                ("sourceFile", @sourceFile()), ("sourceLine", @sourceLine()), ("birthdayCalendar", user.birthdayCalendar),
                ("oper", ToStringWrapper({=> "Some long-running operation returned"})))

            let m = HashMap<String, String>()
            m.add("k1", "1\n")
            m.add("k2", "2")
            m.add("k3", "3")
            logger.trace({=> "Some long-running operation returned"}, ("m1", m))
            let m2 = HashMap<String, LogValue>()
            m2.add("g1", m)
            m2.add("k1", [["1", "4 s"], ["2", "5"], ["3"]])

            // 如果 TRACE 级别没有开启，那么 lambda 表达式不会被执行
            logger.trace({=> "Some long-running operation returned"}, ("m2", m2))
        }
        futs.add(f)
    }

    for (f in futs) {
        f.get()
    }

    logger.close()
}

public class User {
    public prop name: String {
        get() {
            "foo"
        }
    }
    public prop birthdayCalendar: DateTime {
        get() {
            DateTime.now()
        }
    }
}

public class ToStringWrapper <: ToString & LogValue {
    let _fn: () -> String
    public init(fn: () -> String) {
        _fn = fn
    }
    public func toString(): String {
        return _fn()
    }
    public func writeTo(w: LogWriter): Unit {
        w.writeValue(_fn())
    }
}
```

运行结果如下：

```text
{"time":"2024-07-18T07:57:45Z","level":"INFO","msg":"abc","name":"main","age":2}
{"time":"2024-07-18T07:57:45Z","level":"DEBUG","msg":"Logging in user foo with birthday 2024-07-18T07:57:45.9912185Z","name":"main"}
{"time":"2024-07-18T07:57:45Z","level":"INFO","msg":"Hello, World!","name":"main","k1":[[1,4],[2,5],[3]],"password":"v22222"}
{"time":"2024-07-18T07:57:45Z","level":"ERROR","msg":"long-running operation msg","name":"main","k1":100,"k2":"2024-07-18T07:57:45Z","oper":"Some long-running operation returned"}
{"time":"2024-07-18T07:57:45Z","level":"ERROR","msg":"long-running operation msg","name":"main","sourcePackage":"mylog","sourceFile":"main.cj","sourceLine":52,"birthdayCalendar":"2024-07-18T07:57:45Z","oper":"Some long-running operation returned"}
{"time":"2024-07-18T07:57:45Z","level":"TRACE","msg":"Some long-running operation returned","name":"main","m1":{"k1":"1\n","k2":"2","k3":"3"}}
{"time":"2024-07-18T07:57:45Z","level":"TRACE","msg":"Some long-running operation returned","name":"main","m2":{"g1":{"k1":"1\n","k2":"2","k3":"3"},"k1":[["1","4 s"],["2","5"],["3"]]}}
```

下面是使用 [SimpleLogger](../logger_package_api/logger_package_classes.md#class-simplelogger) 日志打印示例代码：

<!-- run -->

```cangjie
import std.time.*
import std.io.{OutputStream, ByteBuffer, BufferedOutputStream}
import std.env.*
import std.fs.*
import std.collection.{HashMap, ArrayList}
import stdx.log.*
import stdx.logger.*

main() {
    let o = ByteBuffer()
    let bo = BufferedOutputStream<OutputStream>(getStdOut())
    let tl = SimpleLogger(bo)
    tl.level = LogLevel.TRACE
    setGlobalLogger(tl)
    let logger = getGlobalLogger([("name", "main")])
    let futs = ArrayList<Future<Unit>>()

    // let f = File("log/a.log", Append)
    // let h = TextHandler(f)
    for (_ in 0..1) {
        let f = spawn {
            =>
            logger.info("abc", ("age", 2))
            let user = User()
            // 记录诊断日志，如果 DEBUG 级别未开启，直接返回，几乎无 cost
            logger.debug("Logging in user ${user.name} with birthday ${user.birthdayCalendar}")
            // 普通记录信息日志
            logger.info("Hello, World!", ("k1", [[1, 4], [2, 5], [3]]), ("password", "v22222"))

            // lazy 方式记录耗时日志数据
            logger.log(LogLevel.ERROR, "long-running operation msg", ("k1", 100), ("k2", user.birthdayCalendar),
                ("oper", ToStringWrapper({=> "Some long-running operation returned"})))

            logger.log(LogLevel.ERROR, "long-running operation msg", ("sourcePackage", @sourcePackage()),
                ("sourceFile", @sourceFile()), ("sourceLine", @sourceLine()), ("birthdayCalendar", user.birthdayCalendar),
                ("oper", ToStringWrapper({=> "Some long-running operation returned"})))

            let m = HashMap<String, String>()
            m.add("k1", "1\n")
            m.add("k2", "2")
            m.add("k3", "3")
            logger.trace({=> "Some long-running operation returned"}, ("m1", m))
            let m2 = HashMap<String, LogValue>()
            m2.add("g1", m)
            m2.add("k1", [["1", "4 s"], ["2", "5"], ["3"]])

            // 如果 TRACE 级别没有开启，那么 lambda 表达式不会被执行
            logger.trace({=> "Some long-running operation returned"}, ("m2", m2))
        }
        futs.add(f)
    }

    for (f in futs) {
        f.get()
    }

    logger.close()
}

public class User {
    public prop name: String {
        get() {
            "foo"
        }
    }
    public prop birthdayCalendar: DateTime {
        get() {
            DateTime.now()
        }
    }
}

public class ToStringWrapper <: ToString & LogValue {
    let _fn: () -> String
    public init(fn: () -> String) {
        _fn = fn
    }
    public func toString(): String {
        return _fn()
    }
    public func writeTo(w: LogWriter): Unit {
        w.writeValue(_fn())
    }
}
```

运行结果如下：

```text
2025-04-15T15:06:54.7371418+08:00 INFO abc name="main" age=2
2025-04-15T15:06:54.737251+08:00 DEBUG Logging in user foo with birthday 2025-04-15T15:06:54.7372416+08:00 name="main"
2025-04-15T15:06:54.7376041+08:00 INFO Hello, World! name="main" k1=[[1,4],[2,5],[3]] password="v22222"
2025-04-15T15:06:54.7379054+08:00 ERROR long-running operation msg name="main" k1=100 k2=2025-04-15T15:06:54.7379047+08:00 oper="Some long-running operation returned"
2025-04-15T15:06:54.7381296+08:00 ERROR long-running operation msg name="main" sourcePackage="mylog" sourceFile="main.cj" sourceLine=37 birthdayCalendar=2025-04-15T15:06:54.7381291+08:00 oper="Some long-running operation returned"
2025-04-15T15:06:54.7385818+08:00 TRACE Some long-running operation returned name="main" m1={k1:"1\n",k2:"2",k3:"3"}
2025-04-15T15:06:54.7387716+08:00 TRACE Some long-running operation returned name="main" m2={g1:{k1:"1\n",k2:"2",k3:"3"},k1:[["1","4 s"],["2","5"],["3"]]}
```

下面是使用 [TextLogger](../logger_package_api/logger_package_classes.md#class-textlogger) 日志打印示例代码：

<!-- compile -->

```cangjie
import std.time.*
import std.io.{OutputStream, ByteBuffer, BufferedOutputStream}
import std.env.*
import std.fs.*
import std.collection.{HashMap, ArrayList}
import stdx.log.*
import stdx.logger.*

main() {
    let o = ByteBuffer()
    let bo = BufferedOutputStream<OutputStream>(getStdOut())
    let tl = TextLogger(bo)
    tl.level = LogLevel.TRACE
    setGlobalLogger(tl)
    let logger = getGlobalLogger([("name", "main")])
    let futs = ArrayList<Future<Unit>>()

    // let f = File("log/a.log", Append)
    // let h = TextHandler(f)
    for (_ in 0..1) {
        let f = spawn {
            =>
            logger.info("abc", ("age", 2))
            let user = User()
            // 记录诊断日志，如果 DEBUG 级别未开启，直接返回，几乎无 cost
            logger.debug("Logging in user ${user.name} with birthday ${user.birthdayCalendar}")
            // 普通记录信息日志
            logger.info("Hello, World!", ("k1", [[1, 4], [2, 5], [3]]), ("password", "v22222"))

            // lazy 方式记录耗时日志数据
            logger.log(LogLevel.ERROR, "long-running operation msg", ("k1", 100), ("k2", user.birthdayCalendar),
                ("oper", ToStringWrapper({=> "Some long-running operation returned"})))

            logger.log(LogLevel.ERROR, "long-running operation msg", ("sourcePackage", @sourcePackage()),
                ("sourceFile", @sourceFile()), ("sourceLine", @sourceLine()), ("birthdayCalendar", user.birthdayCalendar),
                ("oper", ToStringWrapper({=> "Some long-running operation returned"})))

            let m = HashMap<String, String>()
            m.add("k1", "1\n")
            m.add("k2", "2")
            m.add("k3", "3")
            logger.trace({=> "Some long-running operation returned"}, ("m1", m))
            let m2 = HashMap<String, LogValue>()
            m2.add("g1", m)
            m2.add("k1", [["1", "4 s"], ["2", "5"], ["3"]])

            // 如果 TRACE 级别没有开启，那么 lambda 表达式不会被执行
            logger.trace({=> "Some long-running operation returned"}, ("m2", m2))
        }
        futs.add(f)
    }

    for (f in futs) {
        f.get()
    }

    logger.close()
}

public class User {
    public prop name: String {
        get() {
            "foo"
        }
    }
    public prop birthdayCalendar: DateTime {
        get() {
            DateTime.now()
        }
    }
}

public class ToStringWrapper <: ToString & LogValue {
    let _fn: () -> String
    public init(fn: () -> String) {
        _fn = fn
    }
    public func toString(): String {
        return _fn()
    }
    public func writeTo(w: LogWriter): Unit {
        w.writeValue(_fn())
    }
}
```

运行结果如下：

```text
time=2025-04-15T15:18:09.2186361+08:00 level="INFO" msg="abc" name="main" age=2
time=2025-04-15T15:18:09.2187444+08:00 level="DEBUG" msg="Logging in user foo with birthday 2025-04-15T15:18:09.2187408+08:00" name="main"
time=2025-04-15T15:18:09.2191009+08:00 level="INFO" msg="Hello, World!" name="main" k1=[[1,4],[2,5],[3]] password="v22222"
time=2025-04-15T15:18:09.2193242+08:00 level="ERROR" msg="long-running operation msg" name="main" k1=100 k2=2025-04-15T15:18:09.2193236+08:00 oper="Some long-running operation returned"    
time=2025-04-15T15:18:09.2194668+08:00 level="ERROR" msg="long-running operation msg" name="main" sourcePackage="mylog" sourceFile="main.cj" sourceLine=37 birthdayCalendar=2025-04-15T15:18:09.2194663+08:00 oper="Some long-running operation returned"
time=2025-04-15T15:18:09.2197682+08:00 level="TRACE" msg="Some long-running operation returned" name="main" m1={k1:"1\n",k2:"2",k3:"3"}
time=2025-04-15T15:18:09.2200024+08:00 level="TRACE" msg="Some long-running operation returned" name="main" m2={g1:{k1:"1\n",k2:"2",k3:"3"},k1:[["1","4 s"],["2","5"],["3"]]}
```